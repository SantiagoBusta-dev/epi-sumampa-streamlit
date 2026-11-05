import streamlit as st
import datos

@st.cache_data
def cargar():
    return datos.leer_epi(), datos.cargar_anio(), datos.cargar_ugl()

(alumnos, asistencia, insumos, pedidos, alertas), anio, ugl = cargar()

st.markdown("""
<div class="hero">
  <div class="eyebrow">PRÁCTICA PROFESIONALIZANTE II · GRUPO 2</div>
  <h1>De los cuadernos a los datos</h1>
  <p>Una propuesta para ordenar la información del Espacio de Primera Infancia de Sumampa y transformarla en datos útiles para acompañar la tarea cotidiana.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-kicker">El proyecto en pocas palabras</div>', unsafe_allow_html=True)
st.title("Una forma más simple de trabajar con la información")
st.write("La propuesta conecta formularios digitales, una planilla central y herramientas de análisis. El objetivo es evitar la doble carga, facilitar las consultas y ofrecer una mirada más clara sobre asistencia, insumos y seguimiento.")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="info-card"><h3>📱 Registro desde el celular</h3><p>El personal autorizado completa formularios sencillos desde el teléfono, sin necesitar una computadora en el EPI.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="info-card"><h3>📋 Información organizada</h3><p>Las respuestas llegan a una planilla central para mantener los registros reunidos y ordenados.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="info-card"><h3>📊 Análisis y seguimiento</h3><p>Python permite limpiar, analizar y presentar la información mediante indicadores, gráficos y alertas.</p></div>', unsafe_allow_html=True)

st.markdown("### Vista general de los datos de demostración")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Registros infantiles", len(alumnos), help="Dataset ficticio utilizado para probar el funcionamiento.")
m2.metric("Registros de asistencia", len(asistencia))
m3.metric("Alertas de ejemplo", len(alertas))
m4.metric("Años en PAMI", len(anio))

st.info("**Importante:** los registros del EPI que aparecen en esta demostración son ficticios. Los datos de PAMI corresponden a beneficiarios del Instituto y se analizan por separado; no representan a los niños del EPI.")

st.markdown("### Cómo recorrer la aplicación")
st.write("Usá el menú lateral para entrar al panel del EPI, revisar las alertas, explorar los datos abiertos de PAMI o conocer la metodología y las medidas de privacidad.")
with st.expander("¿Qué buscamos resolver?"):
    st.write("Actualmente, el trabajo con registros en papel puede hacer más lenta la búsqueda de información y la elaboración de reportes. La propuesta busca que cada dato se registre una sola vez y pueda utilizarse luego para consultas y análisis.")
