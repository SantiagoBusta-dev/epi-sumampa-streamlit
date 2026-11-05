import streamlit as st
import matplotlib.pyplot as plt
import datos
import graficos as g

@st.cache_data(ttl=24*3600, show_spinner=False)
def descargar():
    return datos.cargar_puntos(datos.leer_texto("puntos"))

st.markdown('<div class="section-kicker">04 · DISTRIBUCIÓN TERRITORIAL</div>', unsafe_allow_html=True)
st.title("Puntos de vacunación de PAMI")
st.write("Exploración del listado de puntos de vacunación publicado en el portal de datos abiertos.")

if "puntos_resultado" not in st.session_state:
    st.session_state["puntos_resultado"] = None

c1, c2 = st.columns([1, 2])
with c1:
    if st.button("Cargar datos de PAMI", type="primary", use_container_width=True):
        try:
            with st.spinner("Descargando y procesando los datos..."):
                st.session_state["puntos_resultado"] = descargar()
        except Exception as e:
            st.error(f"No se pudo descargar el archivo: {type(e).__name__}. Podés intentar nuevamente más tarde.")
with c2:
    archivo = st.file_uploader("O cargar un CSV descargado del portal", type=["csv"])
    if archivo is not None:
        try:
            st.session_state["puntos_resultado"] = datos.cargar_puntos(datos.decodificar(archivo.getvalue()))
        except Exception as e:
            st.error(f"No se pudo procesar el archivo: {type(e).__name__}")

if st.session_state["puntos_resultado"] is not None:
    puntos, resumen = st.session_state["puntos_resultado"]
    cols = st.columns(len(resumen))
    for col, (nombre, valor) in zip(cols, resumen.items()):
        col.metric(nombre.capitalize(), valor)
    st.markdown("### Distribución por provincia")
    provincias = datos.puntos_por_provincia(puntos)
    fig = g.puntos_provincia(provincias)
    if fig is not None:
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    st.metric("Puntos identificados en Santiago del Estero", int(provincias.get("SANTIAGO DEL ESTERO", 0)))
    with st.expander("Revisión de calidad de los datos"):
        st.markdown("**Domicilios que más se repiten**")
        st.dataframe(puntos["domicilio"].value_counts().head(10).rename("Cantidad").reset_index(), hide_index=True, use_container_width=True)
        st.markdown("**Provincias no reconocidas**")
        st.dataframe(puntos.loc[~puntos["reconocida"], "provincia_original"].value_counts().head(10).rename("Cantidad").reset_index(), hide_index=True, use_container_width=True)
else:
    st.info("Presioná «Cargar datos de PAMI» para iniciar el análisis. La descarga requiere conexión a internet.")

st.caption("La relación entre puntos y UGL se interpreta según el código incluido en el identificador del punto. Esa correspondencia debe validarse con la documentación del conjunto de datos antes de utilizarla como conclusión.")
