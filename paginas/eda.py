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

    # Agrupar por especie y aparejo, sumando los kilos
    df_agrupado_kilos = df.groupby(['Especie', 'Aparejo'])['Volumen_Kg'].sum().unstack()

    # Ordenar los datos por la suma total de kilos para cada especie (de menor a mayor)
    df_agrupado_kilos = df_agrupado_kilos.loc[df_agrupado_kilos.sum(axis=1).sort_values().index]

    # Seleccionar el tipo de gráfico para los kilos
    opcion_kilos = st.radio("Selecciona el tipo de gráfico para visualizar la distribución de la captura", ('Escala Normal', 'Escala Logarítmica'), key='kilos')

    # Crear el gráfico interactivo con Plotly
    if opcion_kilos == 'Escala Normal':
        st.subheader('Captura total por especie')
        fig = px.bar(df_agrupado_kilos, 
                    title='Captura total por especie',
                    labels={'value': 'Kilos', 'index': 'Especie'},
                    text_auto=True)
        fig.update_layout(yaxis_title='Kilos', xaxis_title='Especie', xaxis_tickangle=-45)
    else:
        st.subheader('Captura total por especie (Escala Logarítmica)')
        fig = px.bar(df_agrupado_kilos, 
                    title='Captura total por especie (Escala Logarítmica)',
                    labels={'value': 'Kilos', 'index': 'Especie'},
                    log_y=True,
                    text_auto=True)
        fig.update_layout(yaxis_title='Kilos (Logarítmico)', xaxis_title='Especie', xaxis_tickangle=-45)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Agrupar los datos por 'Especie' y sumar las ganancias
    ventas_por_especie = df.groupby('Especie')['Ganancia'].sum().sort_values()

    # Convertir el resultado en un DataFrame para Plotly
    df_ventas = ventas_por_especie.reset_index()
    df_ventas.columns = ['Especie', 'Ganancia']

    # Seleccionar el tipo de gráfico para las ganancias
    opcion_ganancia = st.radio("Selecciona el tipo de gráfico para visualizar las ganancias según la especie", ('Escala Normal', 'Escala Logarítmica'), key='escala_ganancia')

    # Crear el gráfico interactivo con Plotly
    if opcion_ganancia == 'Escala Normal':
        fig = px.bar(df_ventas, 
                    x='Especie', 
                    y='Ganancia', 
                    title='Ganancia por Especie (Escala Normal)', 
                    labels={'Ganancia': 'Ganancia (Suma Total)', 'Especie': 'Especie'},
                    color='Ganancia',
                    text='Ganancia')
        fig.update_layout(xaxis_title='Especie', yaxis_title='Ganancia (Suma Total)', xaxis_tickangle=-45)
    else:
        fig = px.bar(df_ventas, 
                    x='Especie', 
                    y='Ganancia', 
                    title='Ganancia por Especie (Escala Logarítmica)', 
                    labels={'Ganancia': 'Ganancia (Suma Total)', 'Especie': 'Especie'},
                    color='Ganancia',
                    text='Ganancia',
                    log_y=True)
        fig.update_layout(xaxis_title='Especie', yaxis_title='Ganancia (Suma Total) (Logarítmica)', xaxis_tickangle=-45)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Selección de la especie
    especie_seleccionada = st.selectbox('Selecciona la especie', df['Especie'].unique())

    # Filtrar los datos según la especie seleccionada
    df_filtrado = df[df['Especie'] == especie_seleccionada]

    # Crear el gráfico de barras utilizando matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))

    # Crear el mapa centrado en la ubicación media
    mapa = folium.Map(location=[df_filtrado['Origen_Latitud'].mean(), df_filtrado['Origen_Longuitud'].mean()], zoom_start=6)

    # Añadir marcadores al mapa
    for idx, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row['Origen_Latitud'], row['Origen_Longuitud']],
            popup=row['Origen']
        ).add_to(mapa)

    # Mostrar el mapa en Streamlit
    folium_static(mapa)

    # Título de la aplicación
    st.title('Distribución de Precio por Kg ponderada por Volumen en Kg')

    # Crear el histograma ponderado
    fig = px.histogram(df, x='Precio_Kg', y='Volumen_Kg', 
                    histfunc='sum', 
                    nbins=24, 
                    title='Distribución de Precio por Kg ponderada por Volumen en Kg')

    # Actualizar etiquetas del gráfico
    fig.update_layout(xaxis_title='Precio por Kg', 
                    yaxis_title='Volumen en Kg', 
                    bargap=0.1)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Título de la aplicación
    st.title('Distribución de Precio por Kg ponderada por Talla en cm')

    # Crear el histograma ponderado
    fig = px.histogram(df, x='Talla_cm', y='Volumen_Kg', 
                    histfunc='sum', 
                    nbins=24, 
                    title='Distribución de Precio por Kg ponderada por Talla en cm')

    # Actualizar etiquetas del gráfico
    fig.update_layout(xaxis_title='Talla en cm', 
                    yaxis_title='Volumen en Kg', 
                    bargap=0.1)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Título de la aplicación
    st.title('Distribución de Precio por Kg ponderada por Millas Recorridas')

    # Crear el histograma ponderado
    fig = px.histogram(df, x='Millas_Recorridas', y='Volumen_Kg', 
                    histfunc='sum', 
                    nbins=24, 
                    title='Distribución de Precio por Kg ponderada por Millas Recorridas')

    # Actualizar etiquetas del gráfico
    fig.update_layout(xaxis_title='Millas Recorridas', 
                    yaxis_title='Volumen en Kg', 
                    bargap=0.1)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Agrupar por Marca de Motor y Caballos de fuerza, sumando los kilos
    df_agrupado = df.groupby(['Marca_Motor', 'Caballos_Motor'])['Volumen_Kg'].sum().unstack()

    # Convertir el DataFrame a formato largo para Plotly
    df_agrupado_long = df_agrupado.reset_index().melt(id_vars='Marca_Motor', var_name='Caballos_Motor', value_name='Volumen_Kg')

    # Crear el selector de gráficos
    opcion = st.radio('Selecciona el tipo de gráfico para captura por caballos de motor:', ['Escala Normal', 'Escala Logarítmica'])

    # Crear el gráfico interactivo con Plotly
    if opcion == 'Escala Normal':
        st.subheader('Captura total por caballos de motor')
        fig = px.bar(df_agrupado_long, 
                    x='Marca_Motor', 
                    y='Volumen_Kg', 
                    color='Caballos_Motor', 
                    title='Captura total por Motor y Caballos de fuerza',
                    labels={'Marca_Motor': 'Motor', 'Volumen_Kg': 'Kilos'},
                    color_continuous_scale='viridis',
                    text='Volumen_Kg')
        fig.update_layout(xaxis_title='Motor', yaxis_title='Kilos', xaxis_tickangle=-45)
    else:
        st.subheader('Captura total por caballos de motor (Escala Logarítmica)')
        fig = px.bar(df_agrupado_long, 
                    x='Marca_Motor', 
                    y='Volumen_Kg', 
                    color='Caballos_Motor', 
                    title='Captura total por caballos de motor (Escala Logarítmica)',
                    labels={'Marca_Motor': 'Motor', 'Volumen_Kg': 'Kilos'},
                    color_continuous_scale='viridis',
                    text='Volumen_Kg',
                    log_y=True)
        fig.update_layout(xaxis_title='Motor', yaxis_title='Kilos (Logarítmico)', xaxis_tickangle=-45)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Agrupar los datos
    ventas_por_embarcacion = df.groupby('Embarcacion')['Ganancia'].sum()
    millas_por_embarcacion = df.groupby('Embarcacion')['Millas_Recorridas'].sum()
    volumen_por_embarcacion = df.groupby('Embarcacion')['Volumen_Kg'].sum()

    # Crear un DataFrame combinado
    datos_combinados = pd.DataFrame({
        'Ganancia': ventas_por_embarcacion,
        'Millas Recorridas': millas_por_embarcacion,
        'Volumen de Capturas': volumen_por_embarcacion
    })

    # Convertir el DataFrame combinado a formato largo para Plotly
    datos_combinados_long = datos_combinados.reset_index().melt(id_vars='Embarcacion', var_name='Métrica', value_name='Valor')

    # Crear botones para seleccionar el gráfico
    opcion = st.radio('Selecciona el tipo de gráfico:', 
                    ['Ganancia por Embarcación', 
                    'Millas Recorridas por Embarcación', 
                    'Volumen de Capturas por Embarcación',
                    'Barras Apiladas: Ganancia, Millas, Volumen'])

    # Mostrar el gráfico correspondiente
    if opcion == 'Ganancia por Embarcación':
        st.subheader('Ganancia por Embarcación')
        fig = px.bar(ventas_por_embarcacion.reset_index(), 
                    x='Embarcacion', 
                    y='Ganancia', 
                    title='Ganancia por Embarcación',
                    labels={'Ganancia': 'Ganancia', 'Embarcacion': 'Embarcación'},
                    color='Ganancia',
                    text='Ganancia')
        fig.update_layout(xaxis_title='Embarcación', yaxis_title='Ganancia', xaxis_tickangle=-45)

    elif opcion == 'Millas Recorridas por Embarcación':
        st.subheader('Millas Recorridas por Embarcación')
        fig = px.bar(millas_por_embarcacion.reset_index(), 
                    x='Embarcacion', 
                    y='Millas_Recorridas', 
                    title='Millas Recorridas por Embarcación',
                    labels={'Millas_Recorridas': 'Millas Recorridas', 'Embarcacion': 'Embarcación'},
                    color='Millas_Recorridas',
                    text='Millas_Recorridas')
        fig.update_layout(xaxis_title='Embarcación', yaxis_title='Millas Recorridas', xaxis_tickangle=-45)

    elif opcion == 'Volumen de Capturas por Embarcación':
        st.subheader('Volumen de Capturas por Embarcación')
        fig = px.bar(volumen_por_embarcacion.reset_index(), 
                    x='Embarcacion', 
                    y='Volumen_Kg', 
                    title='Volumen de Capturas por Embarcación',
                    labels={'Volumen_Kg': 'Volumen (Kg)', 'Embarcacion': 'Embarcación'},
                    color='Volumen_Kg',
                    text='Volumen_Kg')
        fig.update_layout(xaxis_title='Embarcación', yaxis_title='Volumen (Kg)', xaxis_tickangle=-45)

    elif opcion == 'Barras Apiladas: Ganancia, Millas, Volumen':
        st.subheader('Barras Apiladas: Ganancia, Millas, Volumen por Embarcación')
        fig = px.bar(datos_combinados_long, 
                    x='Embarcacion', 
                    y='Valor', 
                    color='Métrica', 
                    title='Barras Apiladas: Ganancia, Millas, Volumen por Embarcación',
                    labels={'Valor': 'Valores', 'Embarcacion': 'Embarcación'},
                    text='Valor')
        fig.update_layout(xaxis_title='Embarcación', yaxis_title='Valores', xaxis_tickangle=-45)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Agrupar las ganancias por fecha de faena
    df_agrupado = df.groupby('Inicio_Faena')['Ganancia'].sum().reset_index()

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

 