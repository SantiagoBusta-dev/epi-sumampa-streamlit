"""Exploración exploratoria de las tablas ficticias del EPI."""
from pathlib import Path
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.markdown('<div class="section-kicker">06 · EXPLORACIÓN DE DATOS</div>', unsafe_allow_html=True)
st.title("EDA ampliado")
st.write(
    "Exploración de las siete tablas de demostración recibidas para el proyecto. "
    "Permite revisar distribuciones, indicadores descriptivos y calidad de los datos."
)
st.warning(
    "Este conjunto contiene datos ficticios para pruebas académicas. "
    "Los resultados no describen la situación real del EPI y no deben utilizarse para tomar decisiones sobre niños o familias."
)

RUTA = Path(__file__).resolve().parents[1] / "data" / "epi_sumampa.csv"
CAMPOS_PRIVADOS = ("nombre", "apellido", "dni", "telefono", "domicilio", "direccion", "email", "correo")

@st.cache_data
def cargar_tablas(ruta):
    origen = pd.read_csv(ruta, dtype=str, keep_default_na=False)
    tablas = {}
    errores = {}
    for nombre, grupo in origen.groupby("tabla", sort=True):
        filas = []
        for contenido in grupo["datos_json"]:
            try:
                filas.append(json.loads(contenido))
            except (json.JSONDecodeError, TypeError):
                errores[nombre] = errores.get(nombre, 0) + 1
        tablas[nombre] = pd.DataFrame(filas)
    return tablas, errores

def campos_visibles(df):
    return [c for c in df.columns if not any(x in c.lower() for x in CAMPOS_PRIVADOS)]

def convertir_tipos(df):
    salida = df.copy()
    for col in salida.columns:
        if col.startswith("id_") or col in ("edad", "cantidad"):
            salida[col] = pd.to_numeric(salida[col], errors="coerce")
        elif col in ("fecha", "fecha_nacimiento"):
            salida[col] = pd.to_datetime(salida[col], errors="coerce")
    return salida

if not RUTA.exists():
    st.error("No se encontró data/epi_sumampa.csv. Revisá que el archivo esté dentro de la carpeta data.")
    st.stop()

tablas, errores = cargar_tablas(RUTA)
total = sum(len(df) for df in tablas.values())
total_columnas = sum(len(df.columns) for df in tablas.values())

m1, m2, m3, m4 = st.columns(4)
m1.metric("Tablas", len(tablas))
m2.metric("Registros", f"{total:,}".replace(",", "."))
m3.metric("Columnas", total_columnas)
m4.metric("Filas JSON inválidas", sum(errores.values()))

st.markdown("### Estructura general")
resumen = []
for nombre, df in tablas.items():
    resumen.append({
        "Tabla": nombre.replace("_", " ").title(),
        "Registros": len(df),
        "Variables": len(df.columns),
        "Campos vacíos": int(df.replace("", pd.NA).isna().sum().sum()),
        "Duplicados exactos": int(df.duplicated().sum()),
    })
st.dataframe(pd.DataFrame(resumen), hide_index=True, use_container_width=True)

nombres = list(tablas.keys())
seleccion = st.selectbox("Elegí una tabla para explorar", nombres, format_func=lambda x: x.replace("_", " ").title())
df_original = tablas[seleccion].copy()
df = convertir_tipos(df_original)
visibles = campos_visibles(df)

st.markdown(f"### Tabla: {seleccion.replace('_', ' ').title()}")
a, b, c = st.columns(3)
a.metric("Registros", len(df))
b.metric("Variables analizables", len(visibles))
c.metric("Duplicados exactos", int(df.duplicated().sum()))

vacios = df_original.replace("", pd.NA).isna().sum()
calidad = pd.DataFrame({
    "Variable": visibles,
    "Tipo": [str(df[c].dtype) for c in visibles],
    "Valores vacíos": [int(vacios[c]) for c in visibles],
    "Valores distintos": [int(df[c].nunique(dropna=True)) for c in visibles],
})
st.markdown("#### Calidad y estructura")
st.dataframe(calidad, hide_index=True, use_container_width=True)

if visibles:
    col_izq, col_der = st.columns(2)
    with col_izq:
        categoricas = [c for c in visibles if df[c].dtype == "object" and df[c].nunique(dropna=True) <= 30]
        if categoricas:
            campo_cat = st.selectbox("Distribución de una variable categórica", categoricas, key="cat")
            conteo = df[campo_cat].replace("", "Sin dato").value_counts().head(20)
            fig, ax = plt.subplots(figsize=(7, 4))
            conteo.sort_values().plot(kind="barh", ax=ax)
            ax.set_xlabel("Cantidad de registros")
            ax.set_ylabel(campo_cat.replace("_", " ").title())
            ax.set_title("Distribución de categorías")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Esta tabla no tiene variables categóricas adecuadas para el gráfico.")
    with col_der:
        numericas = [c for c in visibles if pd.api.types.is_numeric_dtype(df[c]) and not c.startswith("id_")]
        if numericas:
            campo_num = st.selectbox("Resumen de una variable numérica", numericas, key="num")
            serie = pd.to_numeric(df[campo_num], errors="coerce").dropna()
            if not serie.empty:
                st.dataframe(serie.describe().rename("Valor").to_frame(), use_container_width=True)
                fig, ax = plt.subplots(figsize=(7, 4))
                serie.plot(kind="hist", bins=min(15, max(5, serie.nunique())), ax=ax)
                ax.set_xlabel(campo_num.replace("_", " ").title())
                ax.set_ylabel("Frecuencia")
                ax.set_title("Distribución numérica")
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
        else:
            st.info("Esta tabla no tiene variables numéricas de análisis.")

st.markdown("### Relaciones y cruces")
if seleccion == "alumnos":
    alumnos = df.copy()
    if {"barrio", "vacunas_completas"}.issubset(alumnos.columns):
        cruce = pd.crosstab(alumnos["barrio"], alumnos["vacunas_completas"], margins=True)
        st.write("Vacunación completa según barrio (datos ficticios):")
        st.dataframe(cruce, use_container_width=True)
    if "edad" in alumnos.columns:
        st.write("Cantidad de registros por edad:")
        st.dataframe(alumnos["edad"].value_counts().sort_index().rename_axis("Edad").rename("Cantidad").reset_index(), hide_index=True, use_container_width=True)
elif seleccion == "asistencia":
    if {"tipo", "asistio"}.issubset(df.columns):
        st.write("Asistencia según tipo de persona:")
        st.dataframe(pd.crosstab(df["tipo"], df["asistio"], margins=True), use_container_width=True)
    if "fecha" in df.columns:
        por_fecha = df.groupby(df["fecha"].dt.date).size().rename("Registros").reset_index()
        st.write("Registros por fecha:")
        st.dataframe(por_fecha, hide_index=True, use_container_width=True)
elif seleccion == "pedidos":
    if {"estado", "cantidad"}.issubset(df.columns):
        st.write("Cantidad solicitada por estado:")
        st.dataframe(df.groupby("estado")["cantidad"].agg(["count", "sum", "mean"]).rename(columns={"count":"Pedidos", "sum":"Cantidad total", "mean":"Promedio"}), use_container_width=True)
elif seleccion == "docentes":
    if "rol" in df.columns:
        st.write("Distribución de roles:")
        st.dataframe(df["rol"].value_counts().rename_axis("Rol").rename("Cantidad").reset_index(), hide_index=True, use_container_width=True)
elif seleccion == "insumos":
    if "categoria" in df.columns:
        st.write("Insumos por categoría:")
        st.dataframe(df["categoria"].value_counts().rename_axis("Categoría").rename("Cantidad").reset_index(), hide_index=True, use_container_width=True)
elif seleccion == "tutores":
    if "relacion" in df.columns:
        st.write("Relación declarada con el niño o niña:")
        st.dataframe(df["relacion"].value_counts().rename_axis("Relación").rename("Cantidad").reset_index(), hide_index=True, use_container_width=True)
elif seleccion == "alumno_tutor":
    st.info("Esta tabla vincula identificadores de alumnos con identificadores de tutores. No se muestran nombres ni documentos personales.")

st.caption(
    "Criterio de privacidad: esta pantalla no presenta nombres, apellidos, DNI, teléfonos ni domicilios. "
    "El análisis se limita a conteos y resúmenes agregados."
)
