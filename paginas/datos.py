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
    Esta valiosa recopilación de datos no solo facilita una amplia gama de análisis y visualizaciones, sino que también nos permite comprender mejor las dinámicas dentro del sector pesquero. Con estos datos, podemos explorar tendencias en las capturas, evaluar la eficiencia de las flotas pesqueras, y analizar las zonas más productivas. Esta información es crucial no solo para investigadores y analistas, sino también para aquellos interesados en la sostenibilidad y gestión de los recursos marinos. Además, permite a las partes interesadas en la industria pesquera tomar decisiones más informadas, basadas en patrones históricos y tendencias actuales, promoviendo una pesca más responsable y eficiente.
    """)
