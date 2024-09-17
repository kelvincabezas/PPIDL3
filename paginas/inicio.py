# paginas/inicio.py
import streamlit as st

def display():
    st.image('resources/cabecera.jpg', use_column_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True) #Esto lo utilizamos para generar más espacio y darle aire para que respire el texto
    # Título
    st.markdown("<h1 style='text-align: center;'>Estudio de puntualidad aérea: Un análisis en profundidad sobre la puntualidad en los aeropuertos estadounidenses</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([5,0.5,2])
    with col1:
        st.markdown("""
            <div style='text-align: justify;'>
                <h3>Proyecto final para Hack a Boss</h3>
                <p><strong style='font-size: 18px;'>Este proyecto constituye el punto culminante de nuestra formación en el Bootcamp de Data Science e Inteligencia Artificial en Hack a Boss. En nuestro tercer y último proyecto, hemos decidido abordar un desafío crítico y de alta aplicabilidad en el sector aeronáutico: la optimización de la puntualidad y la gestión de retrasos en vuelos operados desde y hacia aeropuertos en Estados Unidos. A través de un exhaustivo análisis exploratorio de datos, este estudio ofrece perspectivas sobre causas, desempeños y factores influyentes en la puntualidad aérea, proporcionando un modelo predictivo en cuanto a la puntualidad de las aerolíneas para mejorar la satisfacción de los pasajeros.</strong></p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.write("")

    with col3:
        st.image("resources/logotipo_hack_a_boss.png")


    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns([5, 0.8, 5])

    with col4:
        st.markdown("""
            <div style='text-align: justify;'>
                <h4 style='text-align: center;'>El Equipo</h4>
                Este estudio ha sido desarrollado por José Núñez, Rubén Maestre, Dafne Moreno y Nahuel Núñez. Como equipo, hemos combinado nuestras competencias técnicas y experiencia analítica para investigar los retrasos en los vuelos, un tema crítico en la gestión aeronáutica. A través del análisis de grandes volúmenes de datos, hemos identificado tendencias significativas y patrones de comportamiento que influyen en la puntualidad aérea. Nuestro trabajo se centra en proporcionar un entendimiento detallado de los factores que afectan los tiempos de vuelo, con el objetivo de contribuir a la mejora de las operaciones en aeropuertos estadounidenses.
            </div>
            <div style='text-align: justify;'>
                Nuestro enfoque sistemático nos ha permitido desglosar los elementos clave que contribuyen a los retrasos aéreos, evaluando cómo variaciones en la gestión de aerolíneas, la infraestructura aeroportuaria y condiciones externas como festividades y clima impactan en la eficiencia operacional. Las conclusiones derivadas de este análisis proporcionan una base para la formulación de estrategias que pueden ser implementadas por entidades del sector para optimizar la puntualidad de sus operaciones.
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.write("")

    with col6:
        st.markdown("""
            <div style='text-align: justify;'>
                <h4 style='text-align: center;'>Metodología y Objetivos</h4>
                En la fase inicial de nuestro estudio, implementamos técnicas de web scraping utilizando Selenium para recolectar datos relevantes de múltiples fuentes en línea. Este enfoque nos permitió compilar un conjunto de datos exhaustivo y actualizado, esencial para nuestro Análisis Exploratorio de Datos (EDA). Durante el EDA, investigamos diversas variables para identificar aquellas que influyen significativamente en la puntualidad de los vuelos. El objetivo principal de esta fase era preparar el terreno para el desarrollo de un modelo predictivo.
            </div>
            <div style='text-align: justify;'>
                Con los insights obtenidos del EDA, procedimos a entrenar varios modelos de Machine Learning, buscando el que ofreciera la mejor capacidad predictiva respecto a la probabilidad de retraso de los vuelos. Aunque enfrentamos desafíos técnicos debido al gran tamaño de algunos modelos, que dificultaba su integración en plataformas como GitHub y Streamlit debido a restricciones de almacenamiento, seleccionamos un modelo con excelentes métricas de rendimiento. Este modelo está preparado para ser utilizado en entornos operativos, y estamos dispuestos a desarrollar un análisis más detallado y personalizado para aerolíneas que estén interesadas en optimizar sus operaciones.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: justify;'>
            <h4 style='text-align: center;'>Herramientas y Tecnologías</h4>
            Para la realización de este proyecto, hemos empleado una variedad de herramientas tecnológicas adquiridas durante nuestro curso, incluyendo Python, Pandas, Numpy, Plotly, Matplotlib y Keras. Estas herramientas han sido fundamentales para procesar y analizar grandes volúmenes de datos de manera eficiente, así como para la visualización clara e interactiva de los resultados, facilitando el entendimiento de las tendencias y patrones detectados.
        </div>
        <div style='text-align: justify;'>
            Mediante el uso de Streamlit, hemos logrado presentar nuestros resultados de manera dinámica y accesible, proporcionando a los usuarios la posibilidad de interactuar con los datos y explorar en profundidad las diversas facetas de nuestro análisis. Este proyecto refleja no solo el aprendizaje alcanzado en Hack a Boss, sino también nuestra determinación por aplicar la ciencia de datos en la solución de problemas prácticos del mundo real. Confiamos en que los insights y visualizaciones que ofrecemos sean tanto informativos como de utilidad práctica para los interesados.
        </div>
    """, unsafe_allow_html=True)


    