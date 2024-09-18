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
   
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Objetivos</h3><br>", unsafe_allow_html=True)
    colizq, colder = st.columns(2)
    with colizq:
        
        st.markdown("""
            Como objetivo general planteamos el siguiente:
            Determinar las condiciones óptimas para la pesca y su impacto en el valor comercial de diferentes especies, considerando la mejor hora para pescar y la relación entre la talla y el precio.


            1. **Inicialización del navegador**: Utilizamos Selenium para iniciar una instancia del navegador Firefox, lo cual nos permite cargar la URL específica desde donde se extraerán los datos. Este enfoque simula una sesión de navegación real, esencial para interactuar con los elementos web dinámicos.

            2. **Configuración inicial**: Antes de comenzar la extracción de datos, es crucial configurar correctamente las opciones en el sitio web. Para ello, llamamos a la función `preselecciones` que automatiza la selección de todas las estadísticas relevantes, días específicos, el mes de diciembre y los años 2021, 2022 y 2023. Este paso asegura que los datos que vamos a extraer son precisamente los que necesitamos para nuestro análisis.

            3. **Iteración sobre aeropuertos y aerolíneas**: El script ejecuta un bucle que recorre cada aeropuerto listado y, para cada uno de ellos, un bucle anidado itera sobre cada aerolínea disponible. Esta estructura de bucle doble es fundamental para asegurar que se exploran todas las combinaciones posibles de aeropuertos y aerolíneas.

            4. **Extracción de datos**: Durante la iteración, el script intenta seleccionar la combinación específica de aeropuerto y aerolínea y solicita la descarga del archivo .CSV correspondiente. Si la combinación no opera (es decir, no hay datos disponibles), el script omite esta y continúa con la siguiente. Además, se implementa una función de desplazamiento en la página para asegurar que el enlace de descarga está visible y accesible.

            5. **Cierre y limpieza**: Una vez finalizado el proceso de extracción para todas las combinaciones, el script cierra el navegador para terminar la sesión. Este paso es crucial para liberar recursos y evitar problemas de rendimiento en el sistema.
            """)
        