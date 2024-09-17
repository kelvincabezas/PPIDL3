# modules/create_sidebar.py
import streamlit as st
from streamlit_option_menu import option_menu
from paginas import inicio, datos, eda, modelo_predictivo

def create_sidebar():
    # Añadir texto personalizado en el sidebar con markdown y HTML
    st.sidebar.markdown(
        f'<div style="text-align: center; font-size: 18px; margin-bottom: 30px;">'
        f'Proyecto realizado por<br>'
        f'APAZA PEREZ OSCAR GONZALO
        CABEZAS HUANIO RUBEN KELVIN
        RUIZ ALVA JERSON ENMANUEL
        PONCE DE LEON TORRES FABYOLA KORAYMA'
        f'</div>',
        unsafe_allow_html=True
    )

