import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io 


# ===============================
# CLASE (POO)
# ===============================

class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def info_dataset(self):

        buffer = io.StringIO()

        self.df.info(buf=buffer)

        info = buffer.getvalue()

        return info

    def info_general(self):
        return self.df.dtypes

    def valores_nulos(self):
        return self.df.isnull().sum()

    def clasificar_variables(self):
        numericas = self.df.select_dtypes(include=np.number).columns.tolist()
        categoricas = self.df.select_dtypes(exclude=np.number).columns.tolist()
        return numericas, categoricas

    def estadisticas_descriptivas(self):
        return self.df.describe()

    def histograma(self, columna):

        fig, ax = plt.subplots()
        sns.histplot(self.df[columna], kde=True, ax=ax)
        ax.set_title(f"Distribución de {columna}")

        return fig

    def barras(self, columna):

        fig, ax = plt.subplots()
        self.df[columna].value_counts().plot(kind="bar", ax=ax)

        ax.set_title(f"Conteo de {columna}")

        return fig

    def boxplot(self, num, cat):

        fig, ax = plt.subplots()

        sns.boxplot(x=self.df[cat], y=self.df[num], ax=ax)

        ax.set_title(f"{num} vs {cat}")

        return fig


# ===============================
# STREAMLIT CONFIG
# ===============================

st.set_page_config(page_title="EDA Bank Marketing", layout="wide")

st.sidebar.title("Menú")

menu = st.sidebar.radio(
    "Navegación",
    ["Home", "Carga Dataset", "EDA", "Conclusiones"]
)

# ===============================
# HOME
# ===============================

if menu == "Home":
   
    st.title("📊 Proyecto EDA - Bank Marketing")
   ## col4,col5 = st.columns(2)
    col1, col2 = st.columns(2)
    col3, = st.columns(1) 
    col6, = st.columns(1)
    
   ## with col4:
   ##     st.image("C:\\Users\\usuario\\Pictures\\Dmc.png",width=200 )
   ## with col5:
   ##     st.image("C:\\Users\\usuario\\Pictures\\Python.png",width=80 )


    with col1:
        st.info("""
        **Nombre:** Esthiwer Ken Cruz Ayte  
        **Curso:** Especialización en Python for Analytics  
        **Año:** 2026
        """)

    with col2:
        st.success("🚀 Módulo 2 - Proyecto Aplicado")

    with col3:

        st.markdown("---")

        st.markdown("""
        <u><b>Objetivo del trabajo:</b></u>

        Aplicación desarrollada en Streamlit para analizar el dataset Bank Marketing.
        Se presenta una BD de la empresa BankMarketing que es una institución el cual busca
        entender factores que influyen en la aceptación de sus campañas de marketing.
        
        Durante los últimos 6 meses, la efectividad (e = (Ventas/Base)×100%) cayó de 12%
        a 8%, afectando los bonos de los ejecutivos comerciales.
        Este proyecto consiste en analizar los datos de la última campaña para descubrir
        relaciones y comportamientos relevantes entre las variables.

        <u><b>Tecnologías utilizadas:</b></u>

         - Python
         - Pandas
         - Numpy
         - Seaborn
         - Matplotlib
         - Streamlit

        """, unsafe_allow_html=True) 

        st.markdown("---") 

    with col6:
        st.info("""
        **Puesto:** Analista de Gestión de Reclamos y solicitudes  
        **Empresa:** Seguros Falabella  
        """)


# ===============================
# CARGA DATASET
# ===============================

elif menu == "Carga Dataset":

    st.title("Carga del Dataset")

    archivo = st.file_uploader("Subir CSV", type=["csv"])

    if archivo:

        df = pd.read_csv(archivo, sep=";")

        st.success("Dataset cargado")

        st.subheader("Vista previa")

        st.dataframe(df.head())

        st.subheader("Dimensiones")

        st.write("Filas:", df.shape[0])
        st.write("Columnas:", df.shape[1])

        st.session_state["df"] = df

    else:

        st.warning("Cargue el dataset para continuar")

# ===============================
# EDA
# ===============================

elif menu == "EDA":

    if "df" not in st.session_state:

        st.warning("Primero cargue el dataset")

    else:

        df = st.session_state["df"]

        analyzer = DataAnalyzer(df)

        st.title("Análisis Exploratorio")

        tabs = st.tabs([
            "1. Info Dataset",
            "2. Clasificación Variables",
            "3. Estadísticas",
            "4. Valores Faltantes",
            "5. Distribución Numéricas",
            "6. Variables Categóricas",
            "7. Numérico vs Categórico",
            "8. Categórico vs Categórico",
            "9. Análisis Dinámico",
            "10. Hallazgos"
        ])

# ===============================
# ITEM 1
# ===============================

        with tabs[0]:

            st.subheader("Información general del dataset")
        
            # .info()
            st.markdown("### Estructura del dataset .info()")
        
            st.text(analyzer.info_dataset())
        
            # Tipos de datos
            st.markdown("### Tipos de datos")
        
            st.dataframe(analyzer.info_general())
        
            # Valores nulos
            st.markdown("### Conteo de valores nulos")
        
            st.dataframe(analyzer.valores_nulos())
# ===============================
# ITEM 2
# ===============================


        with tabs[1]:

            numericas, categoricas = analyzer.clasificar_variables()

            col1, col2 = st.columns(2)

        with col1:

            st.subheader("Variables Numéricas")
    
            st.write(numericas)
    
            st.success(f"Cantidad de variables numéricas: {len(numericas)}")

        with col2:

            st.subheader("Variables Categóricas")
    
            st.write(categoricas)
    
            st.success(f"Cantidad de variables categóricas: {len(categoricas)}")

# ===============================
# ITEM 3
# ===============================

        with tabs[2]:

            st.subheader("Estadísticas descriptivas")
        
            desc = analyzer.estadisticas_descriptivas()
        
            st.dataframe(desc)
        
            st.markdown("### Interpretación básica")
        
            media_age = df["age"].mean()
            mediana_age = df["age"].median()
            std_age = df["age"].std()
        
            st.write(f"La edad promedio de los clientes es aproximadamente **{media_age:.2f} años**.")
            st.write(f"La mediana de edad es **{mediana_age:.2f}**, lo que indica el punto central de la distribución.")
            st.write(f"La desviación estándar es **{std_age:.2f}**, lo que muestra la dispersión de las edades respecto al promedio.")

# ===============================
# ITEM 4
# ===============================

        with tabs[3]:

            st.subheader("Valores faltantes")

            nulos = analyzer.valores_nulos()

            st.write(nulos)

            fig, ax = plt.subplots()

            nulos.plot(kind="bar", ax=ax)

            st.pyplot(fig)

            st.markdown("### Discusión")

            st.success("El dataset no presenta valores faltantes, lo que facilita el análisis posterior.")

# ===============================
# ITEM 5
# ===============================

        with tabs[4]:

            numericas, _ = analyzer.clasificar_variables()
            col = st.selectbox("Variable numérica", numericas, key="hist_num")
            fig = analyzer.histograma(col)

            st.pyplot(fig) 

            st.markdown("### Interpretación")

            st.write(
            "La distribución muestra cómo se concentran los valores de la variable seleccionada. "
            "Permite identificar sesgos en la distribución, valores extremos y la dispersión de los datos."
            )

# ===============================
# ITEM 6
# ===============================

        with tabs[5]:

            _, categoricas = analyzer.clasificar_variables()

            col = st.selectbox("Variable categórica", categoricas, key="cat_bar")

            fig = analyzer.barras(col)

            st.pyplot(fig) 

            st.markdown("### Proporciones")

            proporcion = df[col].value_counts(normalize=True) * 100
            
            st.dataframe(proporcion.round(2))
            
# ===============================
# ITEM 7
# ===============================

        with tabs[6]:

            st.subheader("Análisis bivariado: Numérico vs Categórico")
        
            numericas, categoricas = analyzer.clasificar_variables()
        
            col1, col2 = st.columns(2)

        with col1:
            num = st.selectbox("Variable numérica", numericas, key="num_box")

        with col2:
            cat = st.selectbox("Variable categórica", categoricas, key="cat_box")

    # -------------------------
    # BOXPLOT
    # -------------------------

            fig = analyzer.boxplot(num, cat)
        
            st.pyplot(fig)
        
            # -------------------------
            # PROPORCIONALIDAD
            # -------------------------
        
            st.markdown("### Proporcionalidad por categoría")
        
            tabla_prop = pd.crosstab(df[cat], df["y"], normalize="index") * 100
        
            st.dataframe(tabla_prop.round(2))
        
            # gráfico proporcional
        
            fig2, ax2 = plt.subplots()
        
            tabla_prop.plot(kind="bar", stacked=True, ax=ax2)
            
            fig2, ax2 = plt.subplots()

            tabla_prop.plot(kind="bar", stacked=True, ax=ax2)
            
            ax2.set_ylabel("Porcentaje")
            ax2.set_title(f"Proporción de respuesta (y) según {cat}")
            
            # -------------------------
            # AGREGAR PORCENTAJES
            # -------------------------
            
            for container in ax2.containers:
                ax2.bar_label(container, fmt="%.1f%%", label_type="center")
            
            st.pyplot(fig2)
                    
            # -------------------------
            # INTERPRETACIÓN
            # -------------------------
        
            st.markdown("### Interpretación")
        
            st.write(
                "La proporcionalidad permite observar cómo cambia la aceptación de la campaña "
                "según cada categoría seleccionada. Esto ayuda a identificar segmentos de clientes "
                "con mayor probabilidad de responder positivamente a la campaña."
            )

# ===============================
# ITEM 8
# ===============================

        with tabs[7]:

            st.subheader("Análisis bivariado: Categórico vs Categórico")
        
            _, categoricas = analyzer.clasificar_variables()
        
            col1 = st.selectbox("Variable categórica 1", categoricas, key="cat1")
        
            col2 = st.selectbox("Variable categórica 2", categoricas, key="cat2")
        
            # -------------------------
            # TABLA DE CONTINGENCIA
            # -------------------------
        
            st.markdown("### Conteo de categorías")
        
            tabla = pd.crosstab(df[col1], df[col2])
        
            st.dataframe(tabla)
        
            # -------------------------
            # PROPORCIONALIDAD
            # -------------------------
        
            st.markdown("### Proporcionalidad (%)")
        
            tabla_prop = pd.crosstab(df[col1], df[col2], normalize="index") * 100
        
            st.dataframe(tabla_prop.round(2))
        
            # -------------------------
            # GRÁFICO PROPORCIONAL
            # -------------------------
        
            fig, ax = plt.subplots()
        
            tabla_prop.plot(kind="bar", stacked=True, ax=ax)
        
            ax.set_ylabel("Porcentaje")
            ax.set_title(f"Distribución proporcional de {col2} según {col1}")
        
            st.pyplot(fig)
        
            # -------------------------
            # INTERPRETACIÓN
            # -------------------------
        
            st.markdown("### Interpretación")
        
            st.write(
                "La tabla y el gráfico muestran cómo se distribuyen proporcionalmente las categorías "
                "de una variable respecto a otra. Esto permite identificar patrones entre variables "
                "categóricas, como qué grupos tienen mayor o menor participación dentro del dataset."
            )

# ===============================
# ITEM 9
# ===============================

        with tabs[8]:

            columnas = st.multiselect("Seleccionar columnas", df.columns)

            if columnas:

                st.dataframe(df[columnas].head())

            if "age" in df.columns:

                rango = st.slider(
                    "Filtrar edad",
                    int(df.age.min()),
                    int(df.age.max()),
                    (30, 50)
                )

                df_filtrado = df[
                    (df.age >= rango[0]) &
                    (df.age <= rango[1])
                ]

                if st.checkbox("Mostrar datos filtrados"):

                    st.dataframe(df_filtrado)

# ===============================
# ITEM 10
# ===============================

        with tabs[9]:

            st.subheader("Hallazgos clave")

            st.write("""
            - La duración del contacto parece influir en la aceptación de la campaña.
            - La mayoría de clientes pertenece a edades entre 30 y 50 años.
            - Algunas categorías laborales predominan en el dataset.
            - Los resultados de campañas anteriores pueden influir en la respuesta actual.
            - El análisis exploratorio permite entender mejor el comportamiento del cliente.
            """)

# ===============================
# CONCLUSIONES
# ===============================

elif menu == "Conclusiones":

    st.title("Conclusiones")

    st.write("""
             
    1. Los clientes que permanecen más tiempo en la llamada tiene mayor probabilidad de aceptar la campaña
    
    2. Nuestra base de clientes se centra en Administradores(25%),Obreros(23%) y técnicos(16%) sin embargo 
    los que presentan una mayor aceptación son los estudiantes y retirados 31% y 25% respectivamente, 
    lo que nos podría llevar a reconsiderar nuestro enfoque del cliente.
    
    3. El historial de campañas previas puede influir en la respuesta del cliente, se observa que las personas registradas anteriormente los que nos les gustaron  registraron actualmente un 14% de aceptación 
       No existentes tuvieron una aceptación de 9% mientras que los que lo aprobaron anteriormente , esta vez solo fue un 65% 
       lo que replantea que posiblemente la campaña o estrategia no ha sido muy impactante
   
    4. Los analfabetos también tienen una mayor aceptación en las campañas, esto podría ser una salida para impulsar a esta segmentación de personas
    
    5. los que tienen celular perciben una mayor aceptación de sus campañas con respecto a los que usan teléfono 14% celular 5% teléfono en aceptación. lo que nos hace pensar 
       en activar un push potente a este segmento
             
    6. Los clientes de edad media representan el mayor porcentaje de contactos (30-50).
    
    7. El tener un crédito hipotecario y crédito personal no influye en el análisis de la data, dado que tiene el mismo nivel de aceptación

    8. Las características demográficas permiten segmentar mejor los clientes.

    """)