# paginas/inicio.py
import streamlit as st

def display():
    st.image('resources/machine.jpg', use_column_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True) #Esto lo utilizamos para generar más espacio y darle aire para que respire el texto
    # Título
    st.markdown("<h1 style='text-align: center;'>Desarrollo de Modelos Predictivos y Estrategias de Implementación para Optimizar la Productividad y Rentabilidad de los Pescadores Artesanales en la caleta COISHCO - 2024</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([5,0.5,2])
    with col1:
        st.markdown("""
            <div style='text-align: justify;'>
                <h3>Proyecto final para Hack a Boss</h3>
                <p><strong style='font-size: 18px;'>Este proyecto constituye el punto culminante de nuestra formación en el Bootcamp de Data Science e Inteligencia Artificial en Hack a Boss. En nuestro tercer y último proyecto, hemos decidido abordar un desafío crítico y de alta aplicabilidad en el sector aeronáutico: la optimización de la puntualidad y la gestión de retrasos en vuelos operados desde y hacia aeropuertos en Estados Unidos. A través de un exhaustivo análisis exploratorio de datos, este estudio ofrece perspectivas sobre causas, desempeños y factores influyentes en la puntualidad aérea, proporcionando un modelo predictivo en cuanto a la puntualidad de las aerolíneas para mejorar la satisfacción de los pasajeros.</strong></p>
            </div>
        """, unsafe_allow_html=True)
    