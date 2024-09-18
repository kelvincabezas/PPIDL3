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
 
 
