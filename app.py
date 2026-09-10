import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def informacion_general(self):
        buffer = StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def clasificar_variables(self):
        numericas = self.df.select_dtypes(
            include=np.number
        ).columns.tolist()

        categoricas = self.df.select_dtypes(
            exclude=np.number
        ).columns.tolist()

        return numericas, categoricas

    def estadisticas_descriptivas(self):
        return self.df.describe()

    def valores_nulos(self):
        return self.df.isnull().sum()

    def porcentajes_nulos(self):
        return (
            self.df.isnull().sum()
            / len(self.df)
            * 100
        )

modulo = st.sidebar.selectbox("Seleccione una sección:",["Home","Carga del dataset","Módulo 3: Análisis Exploratorio de Datos"])

if modulo == "Home":
    st.title("Primer Proyecto de Portafolio Profesional")
    st.image("DMC.png",width=150)
    st.image("Python_logo.png",width=300)
    st.subheader("Julio Humberto Solis Flores")
    st.markdown("Especialización en Python for Analytics")
    st.write("2026")
    st.write("Este proyecto está basado en el archivo BankMarketing.csv, correspondiente a una institución")
    st.write("Para este trabajo se usaron tecnologías como Python, Pandas, Numpy, Streamlit, etc")

elif modulo == "Carga del dataset":

    st.header("Carga del dataset")

    st.markdown("""
    En este módulo se realiza la carga del archivo BankMarketing.csv
    para posteriormente efectuar el Análisis Exploratorio de Datos (EDA).
    """)

    archivo = st.file_uploader(
        "Seleccione el archivo BankMarketing.csv",
        type=["csv"]
    )

    if archivo is not None:

        df = pd.read_csv(archivo, sep=';')
        
        st.session_state["df"] = df

        st.success("Archivo cargado correctamente.")

        st.subheader("Vista previa del dataset")

        st.dataframe(df.head())

        filas, columnas = df.shape

        st.subheader("Dimensiones del dataset")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Filas", filas)

        with col2:
            st.metric("Columnas", columnas)

    else:

        st.warning("Debe cargar el archivo BankMarketing.csv para continuar.")


elif modulo == "Módulo 3: Análisis Exploratorio de Datos":

    st.header("Módulo 3: Análisis Exploratorio de Datos (EDA)")

    st.markdown("""
    En este módulo se realiza el análisis exploratorio del dataset
    BankMarketing.csv con el objetivo de identificar características,
    comportamientos y relaciones relevantes de los clientes frente
    a la campaña de marketing.
    """)

    # ---------------------------------------------------------
    # VALIDAR QUE EL DATASET HAYA SIDO CARGADO
    # ---------------------------------------------------------

    if "df" not in st.session_state:

        st.warning(
            "Primero debe cargar el archivo BankMarketing.csv "
            "en el Módulo 2."
        )

    else:

        df = st.session_state["df"]

        analyzer = DataAnalyzer(df)

        # -----------------------------------------------------
        # INFORMACIÓN BÁSICA
        # -----------------------------------------------------

        st.info(
            f"El dataset contiene {df.shape[0]} registros "
            f"y {df.shape[1]} variables."
        )

        # -----------------------------------------------------
        # TABS
        # -----------------------------------------------------

        tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "1. Información general",
            "2. Clasificación",
            "3. Estadísticas",
            "4. Valores faltantes",
            "5. Distribución numérica",
            "6. Variables categóricas",
            "7. Numérica vs categórica",
            "8. Categórica vs categórica",
            "9. Análisis dinámico",
            "10. Hallazgos clave"
        ])

        # =====================================================
        # ÍTEM 1
        # =====================================================

        with tab1:

            st.subheader("Ítem 1: Información general del dataset")

            st.markdown("""
            Esta sección permite conocer la estructura general del
            dataset, los tipos de datos y la existencia de valores nulos.
            """)

            col1, col2 = st.columns(2)

            with col1:

                st.write("### Información del dataset")

                informacion = analyzer.informacion_general()

                st.text(informacion)

            with col2:

                st.write("### Tipos de datos")

                tipos = pd.DataFrame({
                    "Variable": df.columns,
                    "Tipo de dato": df.dtypes.astype(str)
                })

                st.dataframe(
                    tipos,
                    use_container_width=True
                )

                st.write("### Valores nulos")

                nulos = analyzer.valores_nulos()

                tabla_nulos = pd.DataFrame({
                    "Variable": nulos.index,
                    "Valores nulos": nulos.values
                })

                st.dataframe(
                    tabla_nulos,
                    use_container_width=True
                )

        # =====================================================
        # ÍTEM 2
        # =====================================================

        with tab2:

            st.subheader("Ítem 2: Clasificación de variables")

            st.markdown("""
            Las variables se clasifican en numéricas y categóricas.
            Esta clasificación permite seleccionar posteriormente
            el tipo de análisis y visualización más adecuado.
            """)

            numericas, categoricas = analyzer.clasificar_variables()

            col1, col2 = st.columns(2)

            with col1:

                st.write("### Variables numéricas")

                st.metric(
                    "Cantidad",
                    len(numericas)
                )

                st.dataframe(
                    pd.DataFrame({
                        "Variables numéricas": numericas
                    }),
                    use_container_width=True
                )

            with col2:

                st.write("### Variables categóricas")

                st.metric(
                    "Cantidad",
                    len(categoricas)
                )

                st.dataframe(
                    pd.DataFrame({
                        "Variables categóricas": categoricas
                    }),
                    use_container_width=True
                )

        # =====================================================
        # ÍTEM 3
        # =====================================================

        with tab3:

            st.subheader("Ítem 3: Estadísticas descriptivas")

            st.markdown("""
            Las estadísticas descriptivas permiten analizar medidas
            como la media, mediana, desviación estándar, valores mínimos
            y máximos de las variables numéricas.
            """)

            estadisticas = analyzer.estadisticas_descriptivas()

            st.dataframe(
                estadisticas,
                use_container_width=True
            )

            st.write("### Interpretación básica")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Media**")
                st.write(
                    "Representa el valor promedio de los datos."
                )

            with col2:
                st.write("**Mediana**")
                st.write(
                    "Representa el valor central de los datos."
                )

            with col3:
                st.write("**Dispersión**")
                st.write(
                    "Permite observar qué tan alejados están "
                    "los datos respecto a su promedio."
                )

        # =====================================================
        # ÍTEM 4
        # =====================================================

        with tab4:

            st.subheader("Ítem 4: Análisis de valores faltantes")

            nulos = analyzer.valores_nulos()
            porcentajes = analyzer.porcentajes_nulos()

            tabla_faltantes = pd.DataFrame({
                "Variable": nulos.index,
                "Valores faltantes": nulos.values,
                "Porcentaje (%)": porcentajes.round(2).values
            })

            tabla_faltantes = tabla_faltantes[
                tabla_faltantes["Valores faltantes"] > 0
            ]

            if tabla_faltantes.empty:

                st.success(
                    "No se encontraron valores faltantes "
                    "en el dataset."
                )

            else:

                st.dataframe(
                    tabla_faltantes,
                    use_container_width=True
                )

                fig, ax = plt.subplots()

                ax.bar(
                    tabla_faltantes["Variable"],
                    tabla_faltantes["Valores faltantes"]
                )

                ax.set_title(
                    "Valores faltantes por variable"
                )

                ax.set_xlabel("Variable")
                ax.set_ylabel("Cantidad")

                plt.xticks(rotation=45)

                st.pyplot(fig)

                st.markdown("""
                **Discusión:** los valores faltantes pueden afectar
                los resultados del análisis. Por ello, deben identificarse
                antes de realizar interpretaciones sobre las variables.
                """)

        # =====================================================
        # ÍTEM 5
        # =====================================================

        with tab5:

            st.subheader(
                "Ítem 5: Distribución de variables numéricas"
            )

            st.markdown("""
            Los histogramas permiten observar la distribución de los
            valores y detectar concentraciones, asimetrías o posibles
            valores extremos.
            """)

            numericas, _ = analyzer.clasificar_variables()

            variables_grafico = st.multiselect(
                "Seleccione las variables numéricas:",
                numericas,
                default=numericas[:2]
            )

            bins = st.slider(
                "Cantidad de intervalos del histograma:",
                min_value=5,
                max_value=50,
                value=20
            )

            mostrar_kde = st.checkbox(
                "Mostrar curva de distribución KDE"
            )

            for variable in variables_grafico:

                fig, ax = plt.subplots()

                sns.histplot(
                    data=df,
                    x=variable,
                    bins=bins,
                    kde=mostrar_kde,
                    ax=ax
                )

                ax.set_title(
                    f"Distribución de {variable}"
                )

                st.pyplot(fig)

                st.write(
                    f"**Interpretación:** el histograma muestra "
                    f"cómo se distribuyen los valores de `{variable}`."
                )

        # =====================================================
        # ÍTEM 6
        # =====================================================

        with tab6:

            st.subheader(
                "Ítem 6: Análisis de variables categóricas"
            )

            _, categoricas = analyzer.clasificar_variables()

            variable_cat = st.selectbox(
                "Seleccione una variable categórica:",
                categoricas
            )

            conteos = df[variable_cat].value_counts()

            proporciones = (
                df[variable_cat]
                .value_counts(normalize=True)
                * 100
            )

            tabla_cat = pd.DataFrame({
                "Categoría": conteos.index,
                "Conteo": conteos.values,
                "Proporción (%)":
                    proporciones.round(2).values
            })

            col1, col2 = st.columns(2)

            with col1:

                st.write("### Conteos")

                st.dataframe(
                    tabla_cat,
                    use_container_width=True
                )

            with col2:

                st.write("### Gráfico de barras")

                fig, ax = plt.subplots()

                sns.countplot(
                    data=df,
                    x=variable_cat,
                    ax=ax
                )

                ax.set_title(
                    f"Distribución de {variable_cat}"
                )

                ax.tick_params(
                    axis="x",
                    rotation=45
                )

                st.pyplot(fig)

        # =====================================================
        # ÍTEM 7
        # =====================================================

        with tab7:

            st.subheader(
                "Ítem 7: Análisis bivariado "
                "(numérico vs categórico)"
            )

            st.markdown("""
            Se comparan variables numéricas entre diferentes grupos
            definidos por una variable categórica. El objetivo es
            identificar diferencias de comportamiento entre grupos.
            """)

            numericas, categoricas = analyzer.clasificar_variables()

            if "y" in categoricas:
                categoria_default = categoricas.index("y")
            else:
                categoria_default = 0

            variable_num = st.selectbox(
                "Variable numérica:",
                numericas,
                key="num_vs_cat_num"
            )

            variable_cat = st.selectbox(
                "Variable categórica:",
                categoricas,
                index=categoria_default,
                key="num_vs_cat_cat"
            )

            fig, ax = plt.subplots()

            sns.boxplot(
                data=df,
                x=variable_cat,
                y=variable_num,
                ax=ax
            )

            ax.set_title(
                f"{variable_num} vs {variable_cat}"
            )

            ax.tick_params(
                axis="x",
                rotation=45
            )

            st.pyplot(fig)

            st.write(
                f"El gráfico permite comparar la distribución de "
                f"`{variable_num}` entre las categorías de "
                f"`{variable_cat}`."
            )

        # =====================================================
        # ÍTEM 8
        # =====================================================

        with tab8:

            st.subheader(
                "Ítem 8: Análisis bivariado "
                "(categórico vs categórico)"
            )

            st.markdown("""
            Se analiza la relación entre dos variables categóricas
            mediante tablas de contingencia y proporciones.
            """)

            _, categoricas = analyzer.clasificar_variables()

            if "y" in categoricas:
                categoria_default = categoricas.index("y")
            else:
                categoria_default = 0

            variable_cat1 = st.selectbox(
                "Primera variable categórica:",
                categoricas,
                key="cat1"
            )

            variable_cat2 = st.selectbox(
                "Segunda variable categórica:",
                categoricas,
                index=categoria_default,
                key="cat2"
            )

            tabla_cruzada = pd.crosstab(
                df[variable_cat1],
                df[variable_cat2]
            )

            st.write("### Tabla de contingencia")

            st.dataframe(
                tabla_cruzada,
                use_container_width=True
            )

            tabla_porcentajes = pd.crosstab(
                df[variable_cat1],
                df[variable_cat2],
                normalize="index"
            ) * 100

            st.write("### Proporciones (%)")

            st.dataframe(
                tabla_porcentajes.round(2),
                use_container_width=True
            )

            fig, ax = plt.subplots()

            tabla_cruzada.plot(
                kind="bar",
                ax=ax
            )

            ax.set_title(
                f"{variable_cat1} vs {variable_cat2}"
            )

            ax.set_xlabel(variable_cat1)
            ax.set_ylabel("Cantidad")

            plt.xticks(rotation=45)

            st.pyplot(fig)

        # =====================================================
        # ÍTEM 9
        # =====================================================

        with tab9:

            st.subheader(
                "Ítem 9: Análisis basado en parámetros seleccionados"
            )

            st.markdown("""
            En esta sección el usuario puede seleccionar dinámicamente
            las variables que desea analizar.
            """)

            numericas, categoricas = analyzer.clasificar_variables()

            col1, col2 = st.columns(2)

            with col1:

                variable_x = st.selectbox(
                    "Seleccione variable numérica:",
                    numericas,
                    key="dinamica_num"
                )

            with col2:

                variable_y = st.selectbox(
                    "Seleccione variable categórica:",
                    categoricas,
                    key="dinamica_cat"
                )

            st.write(
                f"### Análisis: {variable_x} según {variable_y}"
            )

            resumen = df.groupby(variable_y)[
                variable_x
            ].agg(
                ["count", "mean", "median", "std"]
            ).reset_index()

            resumen.columns = [
                variable_y,
                "Cantidad",
                "Media",
                "Mediana",
                "Desviación estándar"
            ]

            st.dataframe(
                resumen.round(2),
                use_container_width=True
            )

            fig, ax = plt.subplots()

            sns.boxplot(
                data=df,
                x=variable_y,
                y=variable_x,
                ax=ax
            )

            ax.set_title(
                f"{variable_x} según {variable_y}"
            )

            ax.tick_params(
                axis="x",
                rotation=45
            )

            st.pyplot(fig)

        # =====================================================
        # ÍTEM 10
        # =====================================================

        with tab10:

            st.subheader(
                "Ítem 10: Hallazgos clave"
            )

            st.markdown("""
            Esta sección presenta un resumen de algunos indicadores
            importantes encontrados durante el análisis exploratorio.
            """)

            col1, col2, col3 = st.columns(3)

            with col1:

                total_clientes = len(df)

                st.metric(
                    "Total de registros",
                    f"{total_clientes:,}"
                )

            with col2:

                if "y" in df.columns:

                    aceptacion = (
                        df["y"]
                        .value_counts(normalize=True)
                        .get("yes", 0)
                        * 100
                    )

                    st.metric(
                        "Tasa de aceptación",
                        f"{aceptacion:.2f}%"
                    )

            with col3:

                if "duration" in df.columns:

                    duracion_promedio = df[
                        "duration"
                    ].mean()

                    st.metric(
                        "Duración promedio",
                        f"{duracion_promedio:.2f} seg."
                    )

            st.write("### Resumen de hallazgos")

            if "y" in df.columns:

                conteo_y = df["y"].value_counts()

                if "yes" in conteo_y:

                    porcentaje_yes = (
                        conteo_y["yes"]
                        / len(df)
                        * 100
                    )

                    st.write(
                        f"• La proporción de clientes que aceptaron "
                        f"la campaña fue de {porcentaje_yes:.2f}%."
                    )

                if "no" in conteo_y:

                    porcentaje_no = (
                        conteo_y["no"]
                        / len(df)
                        * 100
                    )

                    st.write(
                        f"• La proporción de clientes que no aceptaron "
                        f"la campaña fue de {porcentaje_no:.2f}%."
                    )

            if "age" in df.columns:

                edad_media = df["age"].mean()
                edad_mediana = df["age"].median()

                st.write(
                    f"• La edad promedio de los clientes fue de "
                    f"{edad_media:.2f} años y la mediana fue de "
                    f"{edad_mediana:.2f} años."
                )

            if "duration" in df.columns:

                duracion_mediana = df["duration"].median()

                st.write(
                    f"• La duración mediana de las llamadas fue de "
                    f"{duracion_mediana:.2f} segundos."
                )

            st.info("""
            Estos resultados constituyen hallazgos descriptivos del
            dataset y no representan modelos predictivos. El objetivo
            es identificar patrones y relaciones que ayuden a comprender
            el comportamiento de los clientes frente a la campaña.
            """)
