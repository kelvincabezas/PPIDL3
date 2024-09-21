# paginas/eda.py
import streamlit as st
import pandas as pd  
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import folium
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from streamlit_folium import folium_static

def display():
    st.markdown("<h2 style='text-align: center;'>Modelo Predictivo Mejorado</h2>", unsafe_allow_html=True)
    st.markdown("---")
 
    # Cargar los datos
    df = pd.read_excel('data/data.xlsx')

    st.write("Visualización de gráficos estadísticos referentes a la actividad pesquera.")

    # Crear el escalador
    scaler = MinMaxScaler()

    # Convertir las columnas de fecha a datetime
    df['Inicio_Faena'] = pd.to_datetime(df['Inicio_Faena'], format='%Y-%m-%d %H:%M:%S')
    df['Inicio_Venta'] = pd.to_datetime(df['Inicio_Venta'], format='%Y-%m-%d %H:%M:%S')

    # Nueva columna: Tiempo entre Faena y Venta (en minutos)
    df['Tiempo_Faena_Venta'] = (df['Inicio_Venta'] - df['Inicio_Faena']).dt.total_seconds() / 60

    # Variables temporales: Día de la semana y Mes
    df['Dia_Semana'] = df['Inicio_Faena'].dt.day_name()
    df['Mes'] = df['Inicio_Faena'].dt.month

    # Bins y etiquetas para el precio
    bins_precio = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    labels_precio = ["S/ (0 - 5)", "S/ (5 - 10)", "S/ (10 - 15)", "S/ (15 - 20)", "S/ (20 - 25)",
            "S/ (25 - 30)", "S/ (30 - 35)", "S/ (35 - 40)", "S/ (40 - 45)", "S/ (45 - 50)", "S/ (50 - 55)"]
    df['Precio_Float'] = pd.cut(df['Precio_Kg'], bins=bins_precio, labels=labels_precio, right=False)

    # Bins y etiquetas para la talla
    bins_talla = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    labels_talla = ["(10 - 20) cm", "(20 - 30) cm", "(30 - 40) cm", "(40 - 50) cm",
                    "(50 - 60) cm", "(60 - 70) cm", "(70 - 80) cm", "(80 - 90) cm", "(90 - 100) cm",
                    "(100 - 110) cm", "(110 - 120) cm", "(120 - 130) cm", "(130 - 140) cm", "(140 - 150) cm"]
    df['Talla_Float'] = pd.cut(df['Talla_cm'], bins=bins_talla, labels=labels_talla, right=False)

    # Normalización de las columnas numéricas
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    df_normalized = df.copy()
    df_normalized[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Seleccionar la opción (especie o embarcación)
    opcion = st.selectbox("Seleccionar el enfoque", ["Embarcación", "Especie"], key="enfoque_selectbox")

    # Selección del valor
    if opcion == "Embarcación":
        seleccion = st.selectbox("Seleccionar la embarcación", df_normalized['Embarcacion'].unique(), key="embarcacion_selectbox")
    else:
        seleccion = st.selectbox("Seleccionar la especie", df_normalized['Especie'].unique(), key="especie_selectbox")

    # Procesar los datos
    X, y = procesar_datos(df_normalized, seleccion, es_embarcacion=(opcion == "Embarcación"))

    if X is not None and y is not None:
        if len(X) > 1:
            # División del dataset en entrenamiento y validación
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
            modelo_rf, train_errors, val_errors = entrenar_modelo_con_curvas(X_train, y_train, X_val, y_val)

            # Mostrar curvas de error
            mostrar_curvas(train_errors, val_errors, seleccion, opcion)

            # Importancia de características
            mostrar_importancia(modelo_rf, X_train.columns, seleccion, opcion)

            # Valores reales vs predichos
            mostrar_valores_reales_vs_predichos(modelo_rf, X_val, y_val, seleccion, opcion)

            # Mostrar métricas del modelo
            mostrar_metricas(modelo_rf, X_val, y_val)
        else:
            st.error("No hay suficientes datos para dividir en conjuntos de entrenamiento y validación.")

# Función para procesar los datos
def procesar_datos(df, seleccion, es_embarcacion=True):
    if es_embarcacion:
        df_seleccion = df[df['Embarcacion'] == seleccion]
    else:
        df_seleccion = df[df['Especie'] == seleccion]

    if df_seleccion.empty:
        st.error(f"No se encontraron datos para la {'embarcación' if es_embarcacion else 'especie'}: {seleccion}")
        return None, None

    # Verificar qué columnas están presentes antes de aplicar get_dummies
    columnas_categoricas = ['Modelo_Motor', 'Origen', 'Aparejo', 'Hora_Faena', 'Precio_Float', 'Talla_Float', 'Mes_Float']
    
    # Crear una lista de columnas que sí existan en el DataFrame
    columnas_existentes = [col for col in columnas_categoricas if col in df_seleccion.columns]
    
    if columnas_existentes:
        df_seleccion = pd.get_dummies(df_seleccion, columns=columnas_existentes, drop_first=True)

    # Continuar con el procesamiento de las otras columnas
    X = df_seleccion.drop(columns=['Embarcacion', 'Especie', 'Volumen_Kg', 'Talla_cm', 'Precio_Kg', 'Venta', 'Ganancia', 
                                   'Origen_Latitud', 'Origen_Longuitud', 'HFloat_Venta', 'HFloat_Faena', 'Mes_Faena', 
                                   'Marca_Motor'], errors='ignore')
    y = df_seleccion['Volumen_Kg'].fillna(0)
    
    return X.apply(pd.to_numeric, errors='coerce').fillna(0), y

# Función para entrenar el modelo
def entrenar_modelo_con_curvas(X_train, y_train, X_val, y_val, n_estimators=100):
    train_errors = []
    val_errors = []
    modelo = RandomForestRegressor(warm_start=True, random_state=42)
    
    for i in range(1, n_estimators + 1):
        modelo.set_params(n_estimators=i)
        modelo.fit(X_train, y_train)
        
        train_errors.append(mean_squared_error(y_train, modelo.predict(X_train)))
        val_errors.append(mean_squared_error(y_val, modelo.predict(X_val)))
    
    return modelo, train_errors, val_errors

# Función para mostrar las curvas de entrenamiento y validación
def mostrar_curvas(train_errors, val_errors, seleccion, opcion):
    st.subheader(f'Curvas de Entrenamiento y Validación - {seleccion} ({opcion})')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, len(train_errors) + 1)), y=train_errors, mode='lines', name='Error de Entrenamiento'))
    fig.add_trace(go.Scatter(x=list(range(1, len(val_errors) + 1)), y=val_errors, mode='lines', name='Error de Validación'))
    fig.update_layout(xaxis_title='Número de Árboles', yaxis_title='Error Cuadrático Medio', title='Curvas de Entrenamiento y Validación', template='plotly_dark')

    st.plotly_chart(fig)

# Función para mostrar la importancia de características
def mostrar_importancia(modelo, columnas, seleccion, opcion):
    st.subheader(f'Importancia de Características - {seleccion} ({opcion})')
    importances = modelo.feature_importances_
    feature_importances = pd.Series(importances, index=columnas).sort_values(ascending=False)
    
    fig = go.Figure(go.Bar(x=feature_importances.index, y=feature_importances.values, marker_color='magenta'))
    fig.update_layout(xaxis_title='Características', yaxis_title='Importancia', title=f'Importancia de Características - {seleccion} ({opcion})', template='plotly_dark')
    st.plotly_chart(fig)

# Función para mostrar valores reales vs predichos
def mostrar_valores_reales_vs_predichos(modelo, X_val, y_val, seleccion, opcion):
    y_pred = modelo.predict(X_val)
    
    st.subheader(f'Valores Reales vs Predichos - {seleccion} ({opcion})')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_val, y=y_pred, mode='markers', marker=dict(color='magenta')))
    fig.update_layout(xaxis_title='Valor Real', yaxis_title='Valor Predicho', title=f'Valores Reales vs Predichos - {seleccion} ({opcion})', template='plotly_dark')
    st.plotly_chart(fig)

# Función para mostrar las métricas del modelo
def mostrar_metricas(modelo, X_val, y_val):
    y_pred = modelo.predict(X_val)
    
    # Calcular métricas
    mae = mean_absolute_error(y_val, y_pred)
    mse = mean_squared_error(y_val, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_val, y_pred)
    
    # Mostrar métricas en Streamlit
    st.subheader('Métricas del Modelo')
    st.write(f"**Error Medio Absoluto (MAE)**: {mae:.2f}")
    st.write(f"**Error Cuadrático Medio (MSE)**: {mse:.2f}")
    st.write(f"**Raíz del Error Cuadrático Medio (RMSE)**: {rmse:.2f}")
    st.write(f"**Coeficiente de Determinación (R²)**: {r2:.2f}")