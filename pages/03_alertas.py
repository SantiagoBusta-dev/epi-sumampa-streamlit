import streamlit as st
import pandas as pd
import datos

@st.cache_data
def cargar():
    return datos.leer_epi()

alumnos, asistencia, insumos, pedidos, alertas = cargar()
st.markdown('<div class="section-kicker">02 · SEGUIMIENTO</div>', unsafe_allow_html=True)
st.title("Alertas para orientar el seguimiento")
st.write("Las alertas sirven para señalar situaciones que conviene revisar. No reemplazan la evaluación del equipo ni deben utilizarse para sancionar o etiquetar a las familias.")

tipos = sorted(alertas["tipo"].dropna().unique())
seleccion = st.multiselect("Filtrar por tipo de alerta", tipos, default=tipos)
reporte = alertas[alertas["tipo"].isin(seleccion)].copy()

c1, c2, c3 = st.columns(3)
c1.metric("Alertas visibles", len(reporte))
c2.metric("Tipos de alerta", reporte["tipo"].nunique() if len(reporte) else 0)
c3.metric("Registros revisables", reporte["id_alumno"].nunique() if "id_alumno" in reporte and len(reporte) else 0)

st.markdown("### Listado de alertas")
# No se muestran nombres ni DNI en esta vista de demostración.
vista = reporte.drop(columns=["dni", "nombre", "apellido"], errors="ignore")
st.dataframe(vista, hide_index=True, use_container_width=True)

if "tipo" in reporte and len(reporte):
    st.markdown("### Alertas por categoría")
    resumen = reporte["tipo"].value_counts().rename_axis("Tipo").reset_index(name="Cantidad")
    st.bar_chart(resumen, x="Tipo", y="Cantidad", use_container_width=True)

st.warning("Los umbrales utilizados en esta demostración son supuestos de trabajo del grupo. Antes de aplicarlos en una situación real, deben revisarse y acordarse con la coordinación del EPI.")
