import streamlit as st
import pandas as pd 

def display():
    st.title('Fuente de los datos')

    st.markdown("""
            <div style='text-align: justify;'>
            <p><strong style='font-size: 18px;'>El proyecto de recopilación de información estadística se llevará a cabo en la caleta Coishco durante los meses de enero y febrero. Este lugar es conocido por ser un punto clave de desembarque de recursos hidrobiológicos, donde se realizan diversas actividades esenciales para el manejo de estos recursos.</strong></p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
 
    # Cargar los datos
    df = pd.read_excel('data/data.xlsx')

    st.write("### Vista previa de los datos")
    st.write(df.head())
 
    st.markdown("<br>", unsafe_allow_html=True)
    st.header('Uso de los datos')

    st.markdown("""
    Esta importante recopilación de datos no solo facilita una variedad de análisis y visualizaciones, sino que también nos ayuda a comprender mejor sobre las dinámicas existentes en la aviación. Con estos datos, podemos explorar tendencias en el tráfico aéreo, evaluar la puntualidad de las aerolíneas, y identificar los aeropuertos más activos. Esta información es esencial no solo para investigadores y analistas sino también para entusiastas de la aviación que buscan entender mejor los patrones y comportamientos del sector. Además, permite a las partes interesadas en la industria tomar decisiones más informadas basadas en tendencias históricas y actuales.
    """)
