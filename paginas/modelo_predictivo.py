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
    st.markdown("<h2 style='text-align: center;'>Modelo Predictivo</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Cargar los datos
    df = pd.read_excel('data/data.xlsx')

    st.write("""
    Comencemos visualizando algunos gráficos estadísticos referentes a la actividad pesquera de la zona
    """)

    # Código para preprocesamiento aquí...

    # Mostrar la imagen si la opción es "Especie"
    if opcion == "Especie":
        especie_seleccionada = seleccion
        ruta_imagen = f"resources/{especie_seleccionada}.png"
        
        try:
            st.image(ruta_imagen, caption=f"Especie: {especie_seleccionada}", use_column_width=True)
        except FileNotFoundError:
            st.error(f"No se encontró la imagen para la especie: {especie_seleccionada}")

    # Procesar los datos
    X, y = procesar_datos(df_normalized, seleccion, es_embarcacion=(opcion == "Embarcación"))

    if X is not None and y is not None:
        if len(X) > 1:
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
            modelo_rf, train_errors, val_errors = entrenar_modelo_con_curvas(X_train, y_train, X_val, y_val)

            # Colocar el nombre del modelo en azul
            st.markdown('<h3 style="color:blue;">Modelo de Entrenamiento: Random Forest</h3>', unsafe_allow_html=True)

            st.subheader(f'Curvas de Entrenamiento y Validación - {seleccion} ({opcion})')

            # Interpretación del gráfico en rojo
            st.markdown("""
            <p style="color:red;">
            Estas curvas muestran cómo de bien nuestro modelo está aprendiendo a predecir el volumen de captura. Si el error de validación es cercano al error de entrenamiento, significa que el modelo es bastante preciso y no se está sobreajustando a los datos de entrenamiento.
            </p>
            """, unsafe_allow_html=True)

            # Código del gráfico aquí...

            # Importancia de características
            st.subheader(f'Importancia de Características - {seleccion} ({opcion})')

            # Interpretación en rojo
            st.markdown("""
            <p style="color:red;">
            La importancia de características nos ayuda a entender cuáles variables son más influyentes en la predicción del volumen de captura. Estas son como los ingredientes principales de una receta, donde algunos tienen un mayor impacto en el resultado final.
            </p>
            """, unsafe_allow_html=True)

            # Código para importancia de características...

            # Valores reales vs predichos
            st.subheader(f'Valores Reales vs Predichos - {seleccion} ({opcion})')

            # Interpretación en rojo
            st.markdown("""
            <p style="color:red;">
            Este gráfico compara nuestras predicciones con los valores reales observados. Si los puntos se alinean bien con la línea diagonal, significa que nuestro modelo está haciendo un buen trabajo prediciendo el volumen de captura.
            </p>
            """, unsafe_allow_html=True)

            # Código para el gráfico de valores reales vs predichos...

            # Métricas del modelo
            st.subheader('Métricas del Modelo')

            # Interpretación en rojo
            st.markdown("""
            <p style="color:red;">
            Aquí se muestran algunas métricas clave que nos indican cuán bien está funcionando nuestro modelo:
            - **MSE (Error Cuadrático Medio):** Indica qué tan lejos están, en promedio, nuestras predicciones de los valores reales.
            - **MAE (Error Absoluto Medio):** Muestra el promedio de las diferencias absolutas entre las predicciones y los valores reales.
            - **R2 (Coeficiente de Determinación):** Nos dice qué tan bien las variables explican la variabilidad del resultado.
            </p>
            """, unsafe_allow_html=True)

            # Mostrar las métricas
            mse = mean_squared_error(y_val, y_val_pred)
            mae = mean_absolute_error(y_val, y_val_pred)
            r2 = r2_score(y_val, y_val_pred)

            st.write(f"MSE (Error Cuadrático Medio): {mse:.4f}")
            st.write(f"MAE (Error Absoluto Medio): {mae:.4f}")
            st.write(f"R2 (Coeficiente de Determinación): {r2:.4f}")
            
        else:
            st.error("No hay suficientes datos para dividir en conjuntos de entrenamiento y validación.")


# Función para categorizar la hora en intervalos de 2 horas considerando A.M. y P.M.
def categorize_hour(hour):
    period = "A.M." if hour < 12 else "P.M."
    hour_12 = hour % 12
    hour_12 = 12 if hour_12 == 0 else hour_12
    start_hour = hour_12
    end_hour = (hour_12 + 2) % 12
    end_hour = 12 if end_hour == 0 else end_hour
    return f"{start_hour:02d} - {end_hour:02d} {period}"

def procesar_datos(df, seleccion, es_embarcacion=True):
    if es_embarcacion:
        df_seleccion = df[df['Embarcacion'] == seleccion]
    else:
        df_seleccion = df[df['Especie'] == seleccion]
    
    if df_seleccion.empty:
        st.error(f"No se encontraron datos para la {'embarcación' if es_embarcacion else 'especie'}: {seleccion}")
        return None, None
    
    df_seleccion = pd.get_dummies(df_seleccion, columns=['Modelo_Motor', 'Origen', 'Aparejo', 'Hora_Faena', 'Precio_Float', 'Talla_Float', 'Mes_Float'], drop_first=True)
    X = df_seleccion.drop(columns=['Embarcacion', 'Especie', 'Volumen_Kg', 'Talla_cm', 'Precio_Kg', 'Venta', 'Ganancia', 'Origen_Latitud', 'Origen_Longuitud', 'HFloat_Venta', 'HFloat_Faena', 'Mes_Faena', 'Marca_Motor'])
    y = df_seleccion['Volumen_Kg'].fillna(0)
    
    return X.apply(pd.to_numeric, errors='coerce').fillna(0), y

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