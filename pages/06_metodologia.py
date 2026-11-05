import streamlit as st
st.markdown('<div class="section-kicker">05 · ORGANIZACIÓN DEL PROYECTO</div>',unsafe_allow_html=True)
st.title("Metodología y alcance")
st.write("La propuesta conecta el registro desde celulares con una planilla central y herramientas de análisis.")
st.markdown("### Circuito propuesto")
pasos=[
("01","Celular","El personal autorizado completa formularios sencillos."),
("02","Formularios","Alta del niño, asistencia diaria e insumos semanales."),
("03","Planilla central","Las respuestas se reúnen en una hoja de cálculo."),
("04","Python","Se revisan formatos, faltantes, duplicados y consistencia."),
("05","Panel","La información se explora con indicadores, gráficos, filtros y tablas.")
]
for n,t,d in pasos:
    st.markdown(f'<div class="info-card" style="min-height:0;margin-bottom:.65rem"><span class="section-kicker">{n}</span><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
st.markdown("### Las siete tablas del conjunto de demostración")
st.dataframe([
{"Tabla":"Alumnos","Contenido":"Datos de inscripción, edad, barrio y vacunas"},
{"Tabla":"Tutores","Contenido":"Datos de responsables y relación con el niño"},
{"Tabla":"Docentes","Contenido":"Personal, roles y datos de contacto"},
{"Tabla":"Asistencia","Contenido":"Registros por fecha y persona"},
{"Tabla":"Alumno-tutor","Contenido":"Relaciones entre identificadores de alumnos y tutores"},
{"Tabla":"Insumos","Contenido":"Nombre y categoría de los insumos"},
{"Tabla":"Pedidos","Contenido":"Insumo, fecha, cantidad y estado"}
],hide_index=True,use_container_width=True)
st.info("El CSV nuevo reemplaza los archivos separados de demostración que se usaban antes para alumnos, asistencia, insumos, pedidos y alertas. PAMI continúa como fuente independiente.")
st.markdown("### Sobre los datos")
st.write("El archivo EPI de esta versión contiene datos ficticios preparados para la práctica académica. En esta aplicación se muestran todos sus campos para demostrar filtros, gráficos, cruces entre tablas y visualización de registros. No se deben incorporar datos reales de niños, familias o personal sin autorización institucional y medidas adecuadas de protección.")
st.markdown("### Roles y acceso en una implementación real")
st.write("Docentes podrían completar asistencia desde el celular; coordinación gestionaría altas e insumos; el equipo del proyecto trabajaría con copias autorizadas para análisis. Los permisos de Google Forms y Sheets deben configurarse para limitar el acceso.")
