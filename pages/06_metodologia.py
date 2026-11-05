import streamlit as st

st.markdown('<div class="section-kicker">05 · ORGANIZACIÓN DEL PROYECTO</div>', unsafe_allow_html=True)
st.title("Metodología, roles y privacidad")
st.write("La propuesta busca que la información se registre una sola vez y pueda utilizarse luego para organizar consultas y análisis.")

st.markdown("### Circuito de información")
pasos = [
    ("01", "Celular", "El personal autorizado completa el formulario correspondiente."),
    ("02", "Formularios", "Cada formulario responde a una tarea concreta y tiene una frecuencia definida."),
    ("03", "Planilla central", "Las respuestas se reúnen en una hoja de cálculo con acceso limitado."),
    ("04", "Python", "Se revisan formatos, duplicados, valores faltantes y consistencia."),
    ("05", "Panel", "Los datos procesados se presentan mediante indicadores y gráficos."),
]
for numero, titulo, descripcion in pasos:
    st.markdown(f'<div class="info-card" style="min-height:0;margin-bottom:.65rem;"><span class="section-kicker">{numero}</span><h3>{titulo}</h3><p>{descripcion}</p></div>', unsafe_allow_html=True)

st.markdown("### Organización de los formularios")
st.dataframe([
    {"Formulario": "Alta del niño", "Responsable": "Coordinación", "Frecuencia": "Una vez, al ingresar"},
    {"Formulario": "Asistencia diaria", "Responsable": "Docentes", "Frecuencia": "Todos los días"},
    {"Formulario": "Insumos", "Responsable": "Coordinación", "Frecuencia": "Semanal"},
], hide_index=True, use_container_width=True)

st.markdown("### Roles de trabajo")
st.markdown("""
- **Docentes:** completan el registro diario de asistencia desde el celular.
- **Coordinación:** realiza las altas, registra los insumos y supervisa la planilla central.
- **Equipo del proyecto:** trabaja con copias de datos autorizadas para realizar la limpieza, el análisis y el desarrollo del panel.
""")

st.markdown("### Acceso y protección de la información")
st.markdown("""
- Los enlaces de los formularios se comparten únicamente por canales internos con el personal autorizado del EPI.
- La planilla central no se publica ni se comparte de forma abierta; su acceso queda limitado a coordinación y a las personas del equipo que estén autorizadas.
- Los docentes utilizan el enlace del formulario desde su teléfono y no necesitan acceso a la planilla.
- Para los análisis y las demostraciones se utilizan códigos y datos ficticios o anonimizados; no se muestran nombres ni documentos personales.
- La información personal solo debería utilizarse con la autorización correspondiente y para las tareas previstas.
""")
st.warning("Compartir un enlace solo por un canal interno no impide técnicamente que otra persona lo reenvíe. Si se necesita restringir quién puede responder, hay que configurar la autenticación y los permisos de Google Forms de acuerdo con las cuentas disponibles para el personal.")

st.markdown("### Alcance de esta demostración")
st.write("La aplicación utiliza registros ficticios del EPI para mostrar cómo funcionaría el circuito. Los indicadores y umbrales son ilustrativos y deben validarse con la coordinación antes de cualquier uso real. Los datos abiertos de PAMI se presentan en una sección independiente.")
