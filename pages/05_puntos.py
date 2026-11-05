import streamlit as st
import matplotlib.pyplot as plt
import datos

@st.cache_data(ttl=24*3600, show_spinner=False)
def descargar():
    return datos.cargar_puntos(datos.leer_texto("puntos"))

st.markdown('<div class="section-kicker">04 · DISTRIBUCIÓN TERRITORIAL</div>', unsafe_allow_html=True)
st.title("Puntos de vacunación de PAMI")
st.write("Exploración del listado público de puntos de vacunación.")
if "puntos_resultado" not in st.session_state:
    st.session_state["puntos_resultado"] = None
c1,c2=st.columns([1,2])
with c1:
    if st.button("Cargar datos de PAMI",type="primary",use_container_width=True):
        try:
            with st.spinner("Descargando y procesando..."):
                st.session_state["puntos_resultado"]=descargar()
        except Exception as e:
            st.error(f"No se pudo cargar el archivo: {type(e).__name__}")
with c2:
    archivo=st.file_uploader("O cargar un CSV descargado del portal",type=["csv"])
    if archivo is not None:
        try:
            st.session_state["puntos_resultado"]=datos.cargar_puntos(datos.decodificar(archivo.getvalue()))
        except Exception as e:
            st.error(f"No se pudo procesar: {type(e).__name__}")
if st.session_state["puntos_resultado"] is not None:
    puntos,resumen=st.session_state["puntos_resultado"]
    cols=st.columns(len(resumen))
    for col,(nombre,valor) in zip(cols,resumen.items()):
        col.metric(nombre.capitalize(),valor)
    provincias=datos.puntos_por_provincia(puntos)
    st.markdown("### Puntos por provincia")
    st.bar_chart(provincias.head(15),horizontal=True,height=450)
    st.metric("Puntos en Santiago del Estero",int(provincias.get("SANTIAGO DEL ESTERO",0)))
    st.markdown("### Registros completos")
    st.dataframe(puntos,hide_index=True,use_container_width=True,height=450)
    st.download_button("Descargar puntos procesados",puntos.to_csv(index=False).encode("utf-8-sig"),
                       "puntos_vacunacion.csv","text/csv")
else:
    st.info("Presioná «Cargar datos de PAMI» para iniciar. Requiere conexión a internet.")
