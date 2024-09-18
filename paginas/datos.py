import streamlit as st
from modules.datos_page.data_count import cargar_y_contar_datos

def display():
    st.title('Extracción de datos y explicación')

    st.markdown("""
            <div style='text-align: justify;'>
            <p><strong style='font-size: 18px;'>Los datos presentados en esta plataforma han sido meticulosamente recolectados mediante técnicas avanzadas de web scraping, empleando un conjunto de herramientas especializadas en la extracción y manipulación de información de páginas web. Este proceso se llevó a cabo con el fin de proporcionar análisis detallados y actualizados sobre los vuelos nacionales en Estados Unidos. <br>Uno de los mayores desafíos al iniciar un proyecto de análisis de datos desde cero es, sin duda, la búsqueda y adquisición de datos relevantes y confiables. Antes de decidirnos por este enfoque específico, llevamos a cabo una exhaustiva investigación exploratoria en busca de temas potencialmente interesantes. Durante esta fase, exploramos múltiples fuentes de datos, incluyendo repositorios populares como Kaggle, diversas páginas gubernamentales y otras plataformas especializadas en datos abiertos. Después de evaluar varias opciones y temáticas, nos decantamos por el estudio de la puntualidad en los vuelos internos de Estados Unidos. Esta elección estuvo motivada tanto por la disponibilidad de datos como por la relevancia del tema en el contexto actual de la industria de la aviación, donde la eficiencia operativa es crucial. <br>Este enfoque nos permitió centrarnos en una problemática de alta relevancia y aplicabilidad, donde nuestras habilidades en ciencia de datos podrían ser aplicadas para generar insights significativos y propuestas de valor concretas para mejorar la experiencia de viaje en Estados Unidos.</strong></p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.5, 12, 0.5])
    with col2:  # Utilizamos la columna del medio para la imagen
        st.image('sources/cabecera_datos.jpg')  # Asegúrate de que la ruta de la imagen sea correcta

    st.header('Tecnologías utilizadas')
    st.markdown("""
    - **BeautifulSoup**: Una librería de Python que facilita la extracción de información de páginas web, parseando los documentos HTML y permitiendo la manipulación eficiente de los mismos.
    - **Requests**: Un módulo de Python para enviar solicitudes HTTP de manera sencilla, utilizado para obtener el código fuente de las páginas web desde las cuales recolectamos datos.
    - **Selenium WebDriver**: Herramienta de automatización para manejar navegadores web, que permite interactuar con elementos web de forma programática en sitios que requieren interacciones dinámicas.
    - **By**: Módulo en Selenium utilizado para localizar elementos dentro de una página web usando varios métodos como id, name, xpath, entre otros.
    - **Select**: Clase en Selenium para interactuar con los elementos `<select>` de los formularios HTML, facilitando la selección automática en menús desplegables.
    - **WebDriverWait y Expected Conditions (EC)**: Utilizados para gestionar la espera de elementos específicos en la página que pueden tardar en aparecer, asegurando que los datos estén disponibles antes de proceder con su extracción.
    - **sleep (time)**: Función del módulo `time` de Python que pausa la ejecución del script para simular interacciones humanas o cumplir con las políticas de uso de los servidores web, evitando ser detectados como bots.
    """)


    st.header('Fuente de los datos')
    st.markdown("""
        Los datos para este estudio fueron extraídos del [Departamento de Estadísticas de Transporte de EE. UU. (BTS)](https://www.transtats.bts.gov/ONTIME/Departures.aspx), una entidad del Departamento de Transporte (DOT). El BTS es reconocido como la principal fuente de estadísticas sobre la aviación comercial, la actividad de transporte multimodal de mercancías y la economía del transporte, proporcionando datos esenciales para tomadores de decisiones y el público en general.

        El BTS asegura la credibilidad de sus productos y servicios a través de un análisis riguroso, una calidad de datos transparente y una independencia de la influencia política, promoviendo métodos innovadores de recolección, análisis, visualización y difusión de datos. Estos esfuerzos ayudan a mejorar la eficiencia operativa, explorar temas emergentes y crear productos informativos que contribuyen a un entendimiento profundo del transporte y su papel transformador en la sociedad.

        La directora del BTS, la Sra. Patricia S. Hu, posee una extensa experiencia estadística, un profundo conocimiento del transporte y una sólida formación en investigación. El Dr. Rolf R. Schmitt, el Subdirector, es un experto reconocido en política de transporte y en el desarrollo de estadísticas para informar decisiones de transporte. Ambos lideran un equipo que es clave en el establecimiento de normativas y estrategias que influyen en el panorama del transporte estadounidense y global.
        """)


    st.header('Proceso de extracción')
    st.markdown("""
        El proceso de extracción se inició almacenando la URL de la página web de vuelos desde la que extraeríamos la información. Esta URL corresponde a la página oficial del [Departamento de Estadísticas de Transporte de EE. UU.](https://www.transtats.bts.gov/ONTIME/Departures.aspx).

        Desarrollamos una función en Python diseñada para desplegar y extraer las opciones disponibles de los menús desplegables de la página. La función, denominada `obtener_opciones`, realiza una solicitud GET a la URL, analiza el HTML de la página utilizando BeautifulSoup y extrae las opciones del menú especificado. A continuación, se muestra un ejemplo de cómo funciona esta función para obtener las listas de aeropuertos y aerolíneas:
        """)

    st.code("""
        url = "https://www.transtats.bts.gov/ONTIME/Departures.aspx"

        def obtener_opciones(url, aeropuertos_aerolineas):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            seleccionar_aeropuerto_aerolinea = soup.find("select", attrs={"name": aeropuertos_aerolineas})
            opciones = seleccionar_aeropuerto_aerolinea.find_all("option")
            listado_opciones = [opcion.text for opcion in opciones]
            return listado_opciones

        listado_aeropuertos = obtener_opciones(url, "cboAirport")
        listado_aerolineas = obtener_opciones(url, "cboAirline")
        """, language='python')

    st.markdown("""
        Utilizando estas listas, procedimos a iterar sobre cada combinación de aeropuerto y aerolínea, aplicando filtros en la página para obtener datos de vuelos específicos de diciembre de los años 2021, 2022 y 2023. Este método automatizado facilitó la recolección sistemática y eficiente de los datos necesarios para nuestro análisis.
        """)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([5,1,5])

    with col1:
        st.image('sources/datos_1.jpg', use_column_width=True)
        st.header('Automatización del Proceso de Selección')
        st.markdown("""
            Esta función automatiza la selección de elementos en un menú desplegable. Se utiliza específicamente para seleccionar los aeropuertos y aerolíneas previamente almacenados en dos listas. La elección de **By.NAME** se debe al hecho de que estos elementos están identificados por su nombre en el código HTML.
            """)

        st.code("""
            def seleccionar_por_indice(url, nombre_seleccionado, lista_elementos):
                \"\"\"Esta función selecciona los aeropuertos y las aerolíneas en el menú desplegable\"\"\"
                driver = webdriver.Firefox()
                driver.get(url)
                seleccion = Select(driver.find_element(By.NAME, nombre_seleccionado))
                
                for elemento in lista_elementos:
                    seleccion.select_by_visible_text(elemento)
                    sleep(1) 
        """, language='python')

    with col2:
        st.write("")

    with col3:
        st.image('sources/datos_2.jpg', use_column_width=True) 
        st.header('Función para seleccionar datos')
        st.markdown("""
            La función **preselecciones** se utiliza al inicio para marcar de antemano todas las estadísticas (por qué sale tarde, el tiempo que tarda en despegar, etc.), todos los días del mes, el mes de diciembre y los tres años con los que hemos hecho el trabajo.
            """)

        st.code("""
            def preselecciones(driver):
                \"\"\"Preselecciona las casillas necesarias para la extracción\"\"\"
                driver.find_element(By.ID, "chkAllStatistics").click() 
                driver.find_element(By.ID, "chkAllDays").click()  
                driver.find_element(By.ID, "chkMonths_11").click()  # click_mes_diciembre
                
                # Selecciona 2021, 2022 y 2023
                driver.find_element(By.ID, "chkYears_34").click()
                driver.find_element(By.ID, "chkYears_35").click() 
                driver.find_element(By.ID, "chkYears_36").click()
        """, language='python')

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Proceso de extracción automatizado</h3><br>", unsafe_allow_html=True)
    colizq, colder = st.columns(2)
    with colizq:
        
        st.markdown("""
            Este script automatiza completamente el proceso de extracción de datos de la página web para cada combinación de aeropuertos y aerolíneas. A continuación se detallan los pasos clave del proceso:

            1. **Inicialización del navegador**: Utilizamos Selenium para iniciar una instancia del navegador Firefox, lo cual nos permite cargar la URL específica desde donde se extraerán los datos. Este enfoque simula una sesión de navegación real, esencial para interactuar con los elementos web dinámicos.

            2. **Configuración inicial**: Antes de comenzar la extracción de datos, es crucial configurar correctamente las opciones en el sitio web. Para ello, llamamos a la función `preselecciones` que automatiza la selección de todas las estadísticas relevantes, días específicos, el mes de diciembre y los años 2021, 2022 y 2023. Este paso asegura que los datos que vamos a extraer son precisamente los que necesitamos para nuestro análisis.

            3. **Iteración sobre aeropuertos y aerolíneas**: El script ejecuta un bucle que recorre cada aeropuerto listado y, para cada uno de ellos, un bucle anidado itera sobre cada aerolínea disponible. Esta estructura de bucle doble es fundamental para asegurar que se exploran todas las combinaciones posibles de aeropuertos y aerolíneas.

            4. **Extracción de datos**: Durante la iteración, el script intenta seleccionar la combinación específica de aeropuerto y aerolínea y solicita la descarga del archivo .CSV correspondiente. Si la combinación no opera (es decir, no hay datos disponibles), el script omite esta y continúa con la siguiente. Además, se implementa una función de desplazamiento en la página para asegurar que el enlace de descarga está visible y accesible.

            5. **Cierre y limpieza**: Una vez finalizado el proceso de extracción para todas las combinaciones, el script cierra el navegador para terminar la sesión. Este paso es crucial para liberar recursos y evitar problemas de rendimiento en el sistema.
            """)
        

    with colder:
        st.code("""
        driver = webdriver.Firefox()
        driver.get(url)

        preselecciones(driver)

        for aeropuerto in listado_aeropuertos:
            select_aeropuerto = Select(driver.find_element(By.NAME, "cboAirport"))
            select_aeropuerto.select_by_visible_text(aeropuerto)

            for aerolinea in listado_aerolineas:
                select_aerolinea = Select(driver.find_element(By.NAME, "cboAirline"))
                select_aerolinea.select_by_visible_text(aerolinea)

                click_submit = driver.find_element(By.ID, "btnSubmit").click()
                driver.execute_script("window.scrollBy(0, 200);")

                try:
                    element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.ID, "DL_CSV")))
                    element.click()
                except:
                    pass

        driver.quit()
        """, language='python')
        st.markdown("""
            Este proceso está diseñado para ser lo más eficiente posible, minimizando la interacción humana y maximizando la precisión y la repetibilidad del proceso de extracción. La automatización mediante Selenium permite un control detallado sobre el navegador, crucial para interactuar con elementos web que de otro modo serían inaccesibles mediante métodos de extracción de datos más estáticos.
            """)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
    Por ir adelantando alguna cosa... aquí tenéis datos preliminares de lo que hemos descargado.
    """)
    # Llamar a la función para obtener los datos calculados
    numero_total_estados, numero_total_ciudades, numero_total_aeropuertos, numero_total_aerolineas = cargar_y_contar_datos()

    col1, col2, col3, col4 = st.columns(4)

    # Definimos el estilo CSS para el borde y el contenido de la columna
    column_style = """
        <style>
        .data-column {{
            border: 2px solid #CCCCCC;  /* Grosor y color del borde */
            border-radius: 10px;  /* Bordes redondeados */
            padding: 20px;  /* Espaciado interno */
            text-align: center;  /* Alineación del texto */
        }}
        .note {{
            font-size: small;  /* Tamaño de la fuente más pequeño para la nota */
            color: #555555;  /* Color gris para la nota */
        }}
        </style>
        <div class='data-column'>
            <h4>{title}</h4>
            <h1>{value}</h1>
            {note}
        </div>
        """

    with col1:
        st.markdown(column_style.format(title='Número total de Estados*', value=numero_total_estados, note="<p class='note'>*Incluye estados de EE. UU. y territorios no incorporados.</p>"), unsafe_allow_html=True)

    with col2:
        st.markdown(column_style.format(title='Número total de ciudades', value=numero_total_ciudades, note=""), unsafe_allow_html=True)

    with col3:
        st.markdown(column_style.format(title='Número total de aeropuertos', value=numero_total_aeropuertos, note=""), unsafe_allow_html=True)

    with col4:
        st.markdown(column_style.format(title='Número total de aerolíneas', value=numero_total_aerolineas, note=""), unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    colizq, colder = st.columns([1, 2.5])

    with colizq:
        st.subheader('Extracción de días festivos en Estados Unidos')
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        Lo siguiente que hemos trabajado es recopilar información sobre los días festivos en Estados Unidos desde 2019 hasta 2023. El proceso de extracción se realiza mediante web scraping en el sitio web: [Cuando en el Mundo](https://www.cuandoenelmundo.com/calendario/estados-unidos/2023).

        La función `fechar_festivos` se encarga de:
        - **Inicialización de listas**: Se crean tres listas vacías para almacenar los días, meses y años de cada festivo detectado.
        - **Iteración por año**: El proceso itera desde 2019 hasta 2023. Para cada año, construye una URL específica al calendario de días festivos de Estados Unidos.
        - **Extracción de datos**: Realiza una solicitud HTTP GET para obtener y analizar el HTML del calendario anual de festivos. Utilizando BeautifulSoup, busca elementos HTML que representen los días festivos.
        - **Almacenamiento de datos**: Los días y meses festivos se extraen y almacenan en las listas correspondientes.
        - **Creación de dataFrame**: Utilizando pandas, se crea un DataFrame con los datos recopilados y se mapean los nombres de los meses a números para facilitar su procesamiento.
        - **Conversión y almacenamiento**: Se convierten las columnas a tipos de datos apropiados y se combinan para formar una columna de fecha completa en formato `datetime`. Finalmente, se guarda el DataFrame en un archivo pickle para su uso posterior.
        """)

    with colder:
        st.code("""
    def fechar_festivos():
        dias_festivos = list()
        mes_festivos = list()
        years = list()

        for year in range(2019, 2024):
            url = f'https://www.cuandoenelmundo.com/calendario/estados-unidos/{year}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Días festivos
            reddays = soup.find_all('td', class_='day redday')
            for d in reddays:
                dias_festivos.append(d.text)

            # Meses festivos
            redmonths = soup.find_all('td', class_='month redday')
            for m in redmonths:
                mes_festivos.append(m.text)

            # Añadir el año
            for y in reddays:
                years.append(year)

        df = pd.DataFrame({
            'dia': dias_festivos,
            'mes': mes_festivos,
            'ano': years
        })

        diccionario = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
                    'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
                    'octubre': 10, 'noviembre': 11, 'diciembre': 12}

        df['dia'] = df['dia'].astype(int)
        df['mes'] = df['mes'].map(diccionario)
        df['festivos'] = pd.to_datetime(df['ano'].astype(str) + '-' +
                                        df['mes'].astype(str) + '-' +
                                        df['dia'].astype(str))
        df.to_pickle('fecha_festivos.pkl')

    fechar_festivos()
        """, language='python')

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.header('Obtención de las coordenadas de los aeropuertos de Estados Unidos')

    st.markdown("""
    Tras haber recolectado y procesado los datos iniciales de vuelos y días festivos, el siguiente paso en nuestro proyecto implica la visualización geográfica de estos datos. Para ello, es esencial disponer de las coordenadas precisas de cada aeropuerto en Estados Unidos. La importancia de integrar estos datos geoespaciales radica en nuestra capacidad para presentar información de manera más intuitiva y accesible mediante mapas interactivos.

    La utilización de las coordenadas de los aeropuertos nos permite implementar visualizaciones en mapas mediante la biblioteca Folium, una herramienta poderosa para la creación de mapas interactivos en Python. Estos mapas no solo enriquecerán visualmente nuestra presentación de datos, sino que también facilitarán análisis más complejos, como la evaluación de patrones de tráfico aéreo y la identificación de zonas con alta frecuencia de retrasos.

    Así, la obtención de las coordenadas geográficas se convierte en un componente crucial para la expansión de nuestro análisis, permitiendo no solo una mejor comprensión de la distribución geográfica de los aeropuertos y su actividad, sino también ofreciendo una base sólida para futuras investigaciones y desarrollos dentro del proyecto.
    """)
    st.markdown("<br><br>", unsafe_allow_html=True)
    colizq, colder = st.columns([1, 1.5])

    with colizq:
        st.subheader('**Proceso de obtención de coordenadas**')
        st.markdown("""
        El proceso para adquirir las coordenadas de los aeropuertos implica varias etapas críticas, comenzando por la identificación de fuentes de datos confiables y culminando con la integración de estas coordenadas en nuestro conjunto de datos existente. Uno de los primeros pasos es la consolidación de los datos de aeropuertos para asegurar que manejamos un conjunto único y preciso para cada ubicación.

        Para comenzar, se realiza una limpieza inicial de los datos, donde se separan y preparan los aeropuertos de origen y destino. Dado que nuestros datos incluyen tanto el aeropuerto de origen como el de destino para cada vuelo, es esencial reducir estos a una lista única para evitar duplicidades y simplificar el análisis posterior.

        Esta preparación incluye la creación de dos dataframes temporales, uno para los aeropuertos de origen y otro para los de destino, los cuales luego se concatenan para formar un único dataframe. Posteriormente, eliminamos los duplicados y reorganizamos las columnas para que el dataframe final solo contenga información única sobre cada aeropuerto, incluyendo su nombre, ciudad y estado.
        """)

    with colder:
        st.code("""
        # Código para consolidar los aeropuertos en un dataframe único
        df_origen = df_aviones[['aeropuerto_origen', 'ciudad_origen', 'estado_origen']].copy()
        df_destino = df_aviones[['aeropuerto_destino']].copy()
        df_destino.columns = ['aeropuerto_origen']
        df_destino['ciudad_origen'] = None
        df_destino['estado_origen'] = None

        # Concatenar los dataframes de origen y destino
        df_aeropuertos_concatenados = pd.concat([df_origen, df_destino])

        # Eliminar duplicados y resetear el índice
        df_aeropuertos_unicos = df_aeropuertos_concatenados.drop_duplicates(subset=['aeropuerto_origen'])
        df_aeropuertos_unicos.reset_index(drop=True, inplace=True)

        # Renombrar las columnas para claridad
        df_aeropuertos_unicos.rename(columns={
            'aeropuerto_origen': 'nombre_aeropuerto',
            'ciudad_origen': 'ciudad',
            'estado_origen': 'estado'
        }, inplace=True)

        print(df_aeropuertos_unicos)
        """, language='python')

    st.markdown("""
    Con este proceso, aseguramos que cada aeropuerto esté representado una sola vez en nuestra base de datos, lo cual es crucial para la etapa siguiente donde se vincularán las coordenadas geográficas. La claridad y precisión en esta fase son fundamentales para evitar errores en el mapeo y en la visualización de datos.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.image('sources/map_usa.jpg', use_column_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.header('Obtención de Coordenadas Usando la API de Foursquare')

    col_izq, col_der = st.columns([3, 1])

    with col_izq:
        st.code("""
        # API de Foursquare
        CLIENT_ID = "xxxxxxxxxxxxxxxx"
        CLIENT_SECRET = "xxxxxxxxxxxxxxxxx"
        API_KEY = "xxxxxxxxxxxxxxxxx"

        headers = {"Accept": "application/json", "Authorization": API_KEY}

        df_aeropuertos_unicos['latitude'] = None
        df_aeropuertos_unicos['longitude'] = None
        df_aeropuertos_unicos['direccion'] = None

        for index, row in df_aeropuertos_unicos.iterrows():
            url_params = {
                "query": "airport" + row['nombre_aeropuerto'],
                "near": f"{row['ciudad']}, {row['estado']}, USA",
                "limit": 1
            }

            response = requests.get(url="https://api.foursquare.com/v3/places/search", params=url_params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                
                if data['results']:
                    result = data['results'][0] 
                    latitude = result['geocodes']['main']['latitude']
                    longitude = result['geocodes']['main']['longitude']
                    direccion = result['location']['formatted_address']
                
                    df_aeropuertos_unicos.at[index, 'latitude'] = latitude
                    df_aeropuertos_unicos.at[index, 'longitude'] = longitude
                    df_aeropuertos_unicos.at[index, 'direccion'] = direccion
            else:
                print(f"Error en la fila {index} con el aeropuerto {row['nombre_aeropuerto']}. Respuesta: {response.status_code}")

        print(df_aeropuertos_unicos.head())
            """, language='python')

    with col_der:
        st.markdown("""
        **Explicación del proceso de uso de la API de Foursquare**

        Hemos decidido utilizar la API de Foursquare para obtener las coordenadas geográficas de los aeropuertos debido a la familiaridad con esta plataforma durante nuestra formación en Hack a Boss. Al buscar por palabras clave relacionadas con "aeropuerto" y ciudades específicas, esperábamos ubicar precisamente cada aeropuerto.

        Aunque la API funcionó bien en muchos casos, es importante destacar que la precisión de la ubicación no fue del 100%. En ocasiones, los resultados indicaban posiciones centradas en la ciudad en lugar del aeropuerto exacto, o cerca de este. Aunque consideramos corregir estos datos manualmente, decidimos que no era prioritario dado que la precisión absoluta no era crítica para nuestros propósitos.

        Posteriormente, al utilizar estas coordenadas en mapas de Folium, observamos y corregimos algunos errores evidentes, como aeropuertos incorrectamente ubicados en la Ciudad de México o en Trinidad y Tobago en lugar de Guam. Estos ajustes fueron posibles gracias a nuestra comprensión geográfica y a las capacidades interactivas de Folium, que permitieron una revisión visual directa de las ubicaciones.
        """)
 
 


# Llama a la función para mostrar la página
display()
