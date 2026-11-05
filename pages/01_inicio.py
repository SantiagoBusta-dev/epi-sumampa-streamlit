import streamlit as st
import datos

@st.cache_data
def cargar():
    return datos.leer_epi()

tablas = cargar()
alumnos = tablas.get("alumnos", __import__("pandas").DataFrame())
asistencia = tablas.get("asistencia", __import__("pandas").DataFrame())
st.markdown("""
<div class="hero">
  <div class="eyebrow">PRÁCTICA PROFESIONALIZANTE II · GRUPO 2</div>
  <h1>De los cuadernos a los datos</h1>
  <p>Una propuesta para ordenar la información del Espacio de Primera Infancia de Sumampa y transformarla en datos útiles para acompañar la tarea cotidiana.</p>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="section-kicker">EL PROYECTO</div>', unsafe_allow_html=True)
st.title("Una mirada integral de la información")
st.write("Esta versión trabaja con un único conjunto ficticio y más completo, organizado en siete tablas relacionadas: alumnos, tutores, docentes, asistencia, vínculos alumno-tutor, insumos y pedidos.")
cols = st.columns(4)
total = sum(len(x) for x in tablas.values())
cols[0].metric("Tablas", len(tablas))
cols[1].metric("Registros totales", f"{total:,}".replace(",", "."))
cols[2].metric("Alumnos", len(alumnos))
cols[3].metric("Asistencias", len(asistencia))
st.markdown("### ¿Qué podés explorar?")
cards = [
    ("👧 Alumnos y tutores", "Información de inscripción, edades, barrios, vacunas y vínculos familiares."),
    ("🗓️ Asistencia", "Registros por fecha, tipo de persona y estado de asistencia."),
    ("👩‍🏫 Equipo", "Composición del personal y distribución por rol."),
    ("📦 Insumos y pedidos", "Categorías de insumos, cantidades solicitadas y estado de los pedidos."),
]
for i in range(0, len(cards), 2):
    c1, c2 = st.columns(2)
    for col, (titulo, desc) in zip((c1,c2), cards[i:i+2]):
        with col:
            st.markdown(f'<div class="info-card"><h3>{titulo}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
st.info("Todos los registros del EPI incluidos en esta demostración son ficticios. La sección de PAMI utiliza un conjunto de datos públicos independiente.")
st.markdown("### Recorrido sugerido")
st.write("Empezá por **Panel integral del EPI** para ver gráficos y registros por tabla. Después visitá **Alertas y seguimiento** y **EDA ampliado** para profundizar el análisis.")
