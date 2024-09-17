# paginas/inicio.py
import streamlit as st

def display():
    st.image('resources/cabecera.jpg', use_column_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True) #Esto lo utilizamos para generar más espacio y darle aire para que respire el texto
    # Título
    st.markdown("<h1 style='text-align: center;'>Desarrollo de Modelos Predictivos y Estrategias de Implementación para Optimizar la Productividad y Rentabilidad de los Pescadores Artesanales en la caleta COISHCO - 2024</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: justify;'>
            <h4 style='text-align: center;'>Herramientas y Tecnologías</h4>
            Para la realización de este proyecto, hemos empleado una variedad de herramientas tecnológicas adquiridas durante nuestro curso, incluyendo Python, Pandas, Numpy, Plotly, Matplotlib y Keras. Estas herramientas han sido fundamentales para procesar y analizar grandes volúmenes de datos de manera eficiente, así como para la visualización clara e interactiva de los resultados, facilitando el entendimiento de las tendencias y patrones detectados.
        </div>
        <div style='text-align: justify;'>
            Mediante el uso de Streamlit, hemos logrado presentar nuestros resultados de manera dinámica y accesible, proporcionando a los usuarios la posibilidad de interactuar con los datos y explorar en profundidad las diversas facetas de nuestro análisis. Este proyecto refleja no solo el aprendizaje alcanzado en Hack a Boss, sino también nuestra determinación por aplicar la ciencia de datos en la solución de problemas prácticos del mundo real. Confiamos en que los insights y visualizaciones que ofrecemos sean tanto informativos como de utilidad práctica para los interesados.
        </div>
    """, unsafe_allow_html=True)
    