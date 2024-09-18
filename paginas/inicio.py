# paginas/inicio.py
import streamlit as st

def display():
    st.image('resources/machine.jpg', use_column_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True) #Esto lo utilizamos para generar más espacio y darle aire para que respire el texto
    # Título
    st.markdown("<h1 style='text-align: center;'>Desarrollo de Modelos Predictivos y Estrategias de Implementación para Optimizar la Productividad y Rentabilidad de los Pescadores Artesanales en la caleta COISHCO - 2024</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: justify;'>
            <h4 style='text-align: center;'>Introducción</h4>
            La pesca de peces juveniles es una práctica desalentada por el Ministerio de la Producción según la Resolución 
            Ministerial Nº 209-2001-PE, la cual regula las “Tallas Mínimas de Captura y Tolerancia Máxima de Ejemplares 
            Juveniles de los Peces e Invertebrados Marinos”. Esta normativa establece que la extracción de especies de flora 
            o fauna acuática en épocas, cantidades, talla y zonas prohibidas, así como la captura sin el respectivo permiso 
            o excediendo el límite de captura por embarcación, será sancionada con penas privativas de libertad de tres a 
            cinco años. La pesca de productos que no han alcanzado la edad adulta pone en riesgo la reproducción y 
            sostenibilidad de las especies. Para evitar esto, la normativa peruana define tamaños mínimos para la 
            captura de peces y un porcentaje máximo de juveniles que pueden ser pescados accidentalmente, 
            criterios que varían según la especie y se actualizan periódicamente. Sin embargo, algunas embarcaciones 
            descartan en altamar los especímenes de menor tamaño para evitar sanciones, lo que incrementa la mortalidad 
            de los peces y distorsiona la información y monitoreo de las especies, según el IMARPE.
        </div>
        <div style='text-align: justify;'>
            Mediante el uso de Streamlit, hemos logrado presentar nuestros resultados de manera dinámica y accesible, proporcionando a los usuarios la posibilidad de interactuar con los datos y explorar en profundidad las diversas facetas de nuestro análisis. Este proyecto refleja no solo el aprendizaje alcanzado en Hack a Boss, sino también nuestra determinación por aplicar la ciencia de datos en la solución de problemas prácticos del mundo real. Confiamos en que los insights y visualizaciones que ofrecemos sean tanto informativos como de utilidad práctica para los interesados.
        </div>
    """, unsafe_allow_html=True)
    