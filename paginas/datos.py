import streamlit as st
import pandas as pd 

def display():
    st.title('Extracción de datos y explicación')

    st.markdown("""
            <div style='text-align: justify;'>
            <p><strong style='font-size: 18px;'>Los datos presentados en esta plataforma han sido meticulosamente recolectados mediante técnicas avanzadas de web scraping, empleando un conjunto de herramientas especializadas en la extracción y manipulación de información de páginas web. Este proceso se llevó a cabo con el fin de proporcionar análisis detallados y actualizados sobre los vuelos nacionales en Estados Unidos. <br>Uno de los mayores desafíos al iniciar un proyecto de análisis de datos desde cero es, sin duda, la búsqueda y adquisición de datos relevantes y confiables. Antes de decidirnos por este enfoque específico, llevamos a cabo una exhaustiva investigación exploratoria en busca de temas potencialmente interesantes. Durante esta fase, exploramos múltiples fuentes de datos, incluyendo repositorios populares como Kaggle, diversas páginas gubernamentales y otras plataformas especializadas en datos abiertos. Después de evaluar varias opciones y temáticas, nos decantamos por el estudio de la puntualidad en los vuelos internos de Estados Unidos. Esta elección estuvo motivada tanto por la disponibilidad de datos como por la relevancia del tema en el contexto actual de la industria de la aviación, donde la eficiencia operativa es crucial. <br>Este enfoque nos permitió centrarnos en una problemática de alta relevancia y aplicabilidad, donde nuestras habilidades en ciencia de datos podrían ser aplicadas para generar insights significativos y propuestas de valor concretas para mejorar la experiencia de viaje en Estados Unidos.</strong></p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
 
    # Cargar los datos
    df = pd.read_excel('data/data.xlsx')

    st.write("### Vista previa de los datos")
    st.write(df.head())
 
# Llama a la función para mostrar la página
display()
