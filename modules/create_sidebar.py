# modules/create_sidebar.py
import streamlit as st
from streamlit_option_menu import option_menu
from paginas import inicio, datos, eda, modelo_predictivo

def create_sidebar():
    # Añadir texto personalizado en el sidebar con markdown y HTML
    st.sidebar.markdown(
        f'<div style="text-align: center; font-size: 18px; margin-bottom: 30px;">'
        f'Proyecto realizado por<br>'
        f'APAZA PEREZ OSCAR GONZALO'
        f'</div>',
        unsafe_allow_html=True
    )

    # Crear el menú de opciones en el sidebar con option_menu
    with st.sidebar:
        selected = option_menu("Menú", ["Inicio", "Datos", "EDA", "Modelo Predictivo"],
            icons=["house", "database", "bar-chart-line", "airplane"],
            menu_icon="cast", default_index=0, orientation="vertical")

    # Llama a la función de la página correspondiente en función de la selección
    if selected == "Inicio":
        inicio.display()
    elif selected == "Datos":
        datos.display()
    elif selected == "EDA":
        eda.display()
    elif selected == "Modelo Predictivo":
        aviones.display()
