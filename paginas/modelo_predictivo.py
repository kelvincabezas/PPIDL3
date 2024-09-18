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
    st.markdown("<h2 style='text-align: center;'>Página de análisis exploratorio de datos (EDA)</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if 'subpagina_eda' not in st.session_state:
        st.markdown("<h4 style='text-align: center;'>En esta sección de nuestro proyecto, te ofrecemos la oportunidad de explorar un análisis detallado de los datos a través de diversos gráficos y visualizaciones. Este espacio está diseñado para que puedas entender mejor y analizar de forma intuitiva la información que hemos recopilado.</h4>", unsafe_allow_html=True)
        st.image('resources/EDA.jpg')

    # Cargar los datos
    df = pd.read_excel('data/data.xlsx')

    st.write("""
    Comencemos visualizando algunos gráficos estadisticos referentes a la actividad pesquera de la zona
    """)

    

    # Crear el gráfico interactivo con Plotly
    st.subheader('Distribución de ganancias por Fecha de Faena')
    fig = px.line(df_agrupado, 
                x='Inicio_Faena', 
                y='Ganancia', 
                title='Distribución de Ganancias por Fecha de Faena',
                labels={'Inicio_Faena': 'Fecha de Faena', 'Ganancia': 'Ganancia'},
                markers=True)

    # Personalizar el gráfico
    fig.update_layout(xaxis_title='Fecha de Faena', yaxis_title='Ganancia', xaxis_tickformat='%Y-%m-%d')

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Agrupar las ganancias por fecha de faena
    df_agrupado = df.groupby('Inicio_Faena')['Costo_Combustible'].sum().reset_index()

    # Crear el gráfico interactivo con Plotly
    st.subheader('Distribución de Costo Combustible por Fecha de Faena')
    fig = px.line(df_agrupado, 
                x='Inicio_Faena', 
                y='Costo_Combustible', 
                title='Distribución de Costo Combustible por Fecha de Faena',
                labels={'Inicio_Faena': 'Fecha de Faena', 'Costo_Combustible': 'Costo_Combustible'},
                markers=True)

    # Personalizar el gráfico
    fig.update_layout(xaxis_title='Fecha de Faena', yaxis_title='Costo Combustible', xaxis_tickformat='%Y-%m-%d')

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Convertir la columna 'Inicio_Faena' y 'Fecha_Venta' a datetime
    df['Inicio_Faena'] = pd.to_datetime(df['Inicio_Faena'], format='%d %m %Y %H:%M')
    df['Inicio_Venta'] = pd.to_datetime(df['Inicio_Venta'], format='%d %m %Y %H:%M')

    # Transformar las columnas 'Inicio_Faena' y 'Inicio_Venta' en valores flotantes (hora + minutos/60)
    df['HFloat_Faena'] = df['Inicio_Faena'].dt.hour + df['Inicio_Faena'].dt.minute / 60
    df['HFloat_Venta'] = df['Inicio_Venta'].dt.hour + df['Inicio_Venta'].dt.minute / 60

    # Función para categorizar la hora en intervalos de 2 horas considerando A.M. y P.M.
    def categorize_hour(hour):
        period = "A.M." if hour < 12 else "P.M."
        hour_12 = hour % 12
        hour_12 = 12 if hour_12 == 0 else hour_12
        start_hour = hour_12
        end_hour = (hour_12 + 2) % 12
        end_hour = 12 if end_hour == 0 else end_hour
        return f"{start_hour:02d} - {end_hour:02d} {period}"

    # Aplicar la función para categorizar las horas en 'Inicio_Faena' y 'Inicio_Venta'
    df['Hora_Faena'] = df['Inicio_Faena'].dt.hour.apply(categorize_hour)

    # Extraer el mes de las columnas 'Inicio_Faena' y 'Inicio_Venta'
    df['Mes_Faena'] = df['Inicio_Faena'].dt.month

    # Crear un diccionario para mapear los números de los meses a nombres abreviados
    meses = {
        1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR', 5: 'MAY', 6: 'JUN',
        7: 'JUL', 8: 'AGO', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC'
    }

    # Crear una nueva columna 'Mes_Faena' basada en el mes de 'Inicio_Faena' y usar el diccionario de mapeo
    df['Mes_Float'] = df['Inicio_Faena'].dt.month.map(meses)

    # Definir los límites de los rangos
    bins_precio = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    # Definir las etiquetas correspondientes para cada rango
    labels_precio = ["S/ (0 - 5)", "S/ (5 - 10)", "S/ (10 - 15)", "S/ (15 - 20)", "S/ (20 - 25)",
            "S/ (25 - 30)", "S/ (30 - 35)", "S/ (35 - 40)", "S/ (40 - 45)", "S/ (45 - 50)", "S/ (50 - 55)"]

    # Crear la nueva columna 'Precio_Float'
    df['Precio_Float'] = pd.cut(df['Precio_Kg'], bins=bins_precio, labels=labels_precio, right=False)

    # Definir los límites de los rangos
    bins_talla = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    # Definir las etiquetas correspondientes para cada rango
    labels_talla = ["(10 - 20) cm", "(20 - 30) cm", "(30 - 40) cm", "(40 - 50) cm",
                    "(50 - 60) cm", "(60 - 70) cm", "(70 - 80) cm", "(80 - 90) cm", "(90 - 100) cm",
                    "(100 - 110) cm", "(110 - 120) cm", "(120 - 130) cm", "(130 - 140) cm", "(140 - 150) cm"]

    # Crear la nueva columna 'Talla_Float'
    df['Talla_Float'] = pd.cut(df['Talla_cm'], bins=bins_talla, labels=labels_talla, right=False)

    # Crear un nuevo DataFrame eliminando las columnas datatime
    df_ = df.drop(columns=['Inicio_Faena', 'Inicio_Venta'])

    # Crear una tabla de frecuencias ponderada
    hist_data = df_.groupby('HFloat_Faena').apply(lambda x: (x['Volumen_Kg'] * len(x)).sum())
    hist_data = hist_data.reset_index(name='Volumen_Total')

    # Graficar la distribución de las faenas por hora del día
    st.subheader('Distribución de las faenas por Hora del Día')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_, x='HFloat_Faena', weights='Volumen_Kg', bins=24, kde=True)
    ax.set_xlabel('Hora del Día')
    ax.set_ylabel('Distribución de las faenas')
    ax.set_title('Distribución de las faenas por Hora del Día')
    st.pyplot(fig)

    # Graficar la distribución de las ventas por hora del día
    st.subheader('Distribución de las Ventas por Hora del Día')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_, x='HFloat_Venta', weights='Venta', bins=24, kde=True)
    ax.set_xlabel('Hora del Día')
    ax.set_ylabel('Distribución de las Ventas')
    ax.set_title('Distribución de las Ventas por Hora del Día')
    st.pyplot(fig)

    # Seleccionamos las columnas numéricas
    numeric_columns = df_.select_dtypes(include=['int64', 'float64', 'int32']).columns

    # Crear el escalador
    scaler = MinMaxScaler()

    # Aplicar la normalización
    df_normalized = df_.copy()
    df_normalized[numeric_columns] = scaler.fit_transform(df_[numeric_columns])

    st.write("### Datos normalizados")
    st.write(df_normalized.head())

    # Calcular y graficar la matriz de correlación
    st.subheader('Matriz de Correlación')

    # Seleccionar las columnas para la matriz de correlación
    selected_columns = ['Caballos_Motor', 'Millas_Recorridas', 'Volumen_Kg', 'Precio_Kg', 
                        'Talla_cm', 'Venta', 'Costo_Combustible', 'Ganancia', 
                        'HFloat_Faena', 'HFloat_Venta', 'Origen_Latitud', 'Origen_Longuitud', 'Mes_Faena']

    # Calcular la matriz de correlación
    correlation_matrix = df_normalized[selected_columns].corr()

    # Crear el gráfico interactivo con Plotly
    fig = px.imshow(correlation_matrix,
                    labels={'x': 'Variables', 'y': 'Variables', 'color': 'Correlación'},
                    x=correlation_matrix.columns,
                    y=correlation_matrix.columns,
                    color_continuous_scale='Magma',
                    aspect='auto')

    # Personalizar el diseño del gráfico
    fig.update_layout(
        title='Matriz de Correlación entre Variables',
        coloraxis_showscale=True,
        xaxis={'side': 'bottom'},
        yaxis={'side': 'left'}
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Descargar la matriz de correlación
    st.subheader('Descargar Matriz de Correlación')
    csv = correlation_matrix.to_csv(index=True)
    st.download_button(label="Descargar Matriz de Correlación como CSV",
                    data=csv,
                    file_name='matriz_correlacion.csv',
                    mime='text/csv')

    # Seleccionar la opción (especie o embarcación)
    opcion = st.selectbox("Seleccionar el enfoque", ["Embarcación", "Especie"], key="enfoque_selectbox")

    # Clave única para cada selección
    if opcion == "Embarcación":
        seleccion = st.selectbox("Seleccionar la embarcación", df_normalized['Embarcacion'].unique(), key="embarcacion_selectbox")
    else:
        seleccion = st.selectbox("Seleccionar la especie", df_normalized['Especie'].unique(), key="especie_selectbox")

    # Mostrar la imagen si la opción es "Especie"
    if opcion == "Especie":
        especie_seleccionada = seleccion
        ruta_imagen = f"resources/{especie_seleccionada}.png"
        
        try:
            st.image(ruta_imagen, caption=f"Especie: {especie_seleccionada}", use_column_width=True)
        except FileNotFoundError:
            st.error(f"No se encontró la imagen para la especie: {especie_seleccionada}")

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

    # Procesar los datos
    X, y = procesar_datos(df_normalized, seleccion, es_embarcacion=(opcion == "Embarcación"))

    if X is not None and y is not None:
        if len(X) > 1:
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
            modelo_rf, train_errors, val_errors = entrenar_modelo_con_curvas(X_train, y_train, X_val, y_val)

            # Curvas de entrenamiento y validación
            st.subheader(f'Curvas de Entrenamiento y Validación - {seleccion} ({opcion})')
            st.markdown("""
            Estas curvas muestran cómo de bien nuestro modelo está aprendiendo a predecir el volumen de captura. Si el error de validación es cercano al error de entrenamiento, significa que el modelo es bastante preciso y no se está sobreajustando a los datos de entrenamiento.
            """)

            fig = go.Figure()

            # Añadir líneas para los errores de entrenamiento y validación
            fig.add_trace(go.Scatter(x=list(range(1, len(train_errors) + 1)), y=train_errors, mode='lines', name='Error de Entrenamiento'))
            fig.add_trace(go.Scatter(x=list(range(1, len(val_errors) + 1)), y=val_errors, mode='lines', name='Error de Validación'))

            fig.update_layout(
                xaxis_title='Número de Árboles',
                yaxis_title='Error Cuadrático Medio',
                title='Curvas de Entrenamiento y Validación',
                template='plotly_dark'
            )

            st.plotly_chart(fig)

            # Importancia de características
            st.subheader(f'Importancia de Características - {seleccion} ({opcion})')
            st.markdown("""
            La importancia de características nos ayuda a entender cuáles variables son más influyentes en la predicción del volumen de captura. Estas son como los ingredientes principales de una receta, donde algunos tienen un mayor impacto en el resultado final.
            """)

            importances = modelo_rf.feature_importances_
            indices = X_train.columns
            feature_importances = pd.Series(importances, index=indices).sort_values(ascending=False)
            
            # Mostrar la característica más influyente
            caracteristica_principal = feature_importances.idxmax()
            st.markdown(f"**La característica más influyente es:** `{caracteristica_principal}`, lo que indica que esta variable tiene el mayor impacto en la predicción del volumen de captura.")

            if 'Hora_Venta' in feature_importances.index:
                feature_importances = feature_importances.drop('Hora_Venta')

            fig = go.Figure()

            # Añadir las barras de importancia
            fig.add_trace(go.Bar(x=feature_importances.index, y=feature_importances.values, marker_color='magenta'))

            fig.update_layout(
                xaxis_title='Características',
                yaxis_title='Importancia',
                title=f'Importancia de Características - {seleccion} ({opcion})',
                template='plotly_dark'
            )

            st.plotly_chart(fig)

            # Valores reales vs predichos
            st.subheader(f'Valores Reales vs Predichos - {seleccion} ({opcion})')
            st.markdown("""
            Este gráfico compara nuestras predicciones con los valores reales observados. Si los puntos se alinean bien con la línea diagonal, significa que nuestro modelo está haciendo un buen trabajo prediciendo el volumen de captura.
            """)

            y_val_pred = modelo_rf.predict(X_val)

            fig = go.Figure()

            # Añadir puntos para valores reales vs predichos
            fig.add_trace(go.Scatter(x=y_val, y=y_val_pred, mode='markers', name='Valores Reales vs Predichos', marker=dict(color='cyan', opacity=0.5)))

            # Añadir línea de referencia
            fig.add_trace(go.Scatter(x=[y_val.min(), y_val.max()], y=[y_val.min(), y_val.max()], mode='lines', name='Línea de Referencia', line=dict(color='red', dash='dash')))

            fig.update_layout(
                xaxis_title='Valores Reales',
                yaxis_title='Valores Predichos',
                title=f'Valores Reales vs Predichos - {seleccion} ({opcion})',
                template='plotly_dark'
            )

            st.plotly_chart(fig)

            # Mostrar métricas del modelo
            st.subheader('Métricas del Modelo')
            st.markdown("""
            Aquí se muestran algunas métricas clave que nos indican cuán bien está funcionando nuestro modelo:
            - **MSE (Error Cuadrático Medio):** Indica qué tan lejos están, en promedio, nuestras predicciones de los valores reales.
            - **MAE (Error Absoluto Medio):** Muestra el promedio de las diferencias absolutas entre las predicciones y los valores reales.
            - **R2 (Coeficiente de Determinación):** Nos dice qué tan bien las variables explican la variabilidad del resultado.
            """)

            mse = mean_squared_error(y_val, y_val_pred)
            mae = mean_absolute_error(y_val, y_val_pred)
            r2 = r2_score(y_val, y_val_pred)

            st.write(f"MSE (Error Cuadrático Medio): {mse:.4f}")
            st.write(f"MAE (Error Absoluto Medio): {mae:.4f}")
            st.write(f"R2 (Coeficiente de Determinación): {r2:.4f}")
            
        else:
            st.error("No hay suficientes datos para dividir en conjuntos de entrenamiento y validación.")

