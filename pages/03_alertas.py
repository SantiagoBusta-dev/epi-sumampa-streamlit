import streamlit as st
import pandas as pd
import datos

@st.cache_data
def cargar():
    return datos.leer_epi()

tablas = cargar()
alumnos = tablas.get("alumnos", pd.DataFrame())
asistencia = tablas.get("asistencia", pd.DataFrame())
pedidos = tablas.get("pedidos", pd.DataFrame())
insumos = tablas.get("insumos", pd.DataFrame())

st.markdown('<div class="section-kicker">02 · SEGUIMIENTO</div>', unsafe_allow_html=True)
st.title("Alertas y seguimiento")
st.write("Alertas generadas automáticamente a partir de los registros ficticios. Los criterios son ilustrativos y pueden ajustarse para una demostración.")
alertas = []

if {"vacunas_completas","id_alumno"}.issubset(alumnos.columns):
    pendientes = alumnos[alumnos["vacunas_completas"].astype(str).str.lower().isin(["no","incompleto","pendiente"])].copy()
    for _,r in pendientes.iterrows():
        alertas.append({"Tipo":"Vacunación a revisar","ID":r.get("id_alumno"),"Persona":f"{r.get('nombre','')} {r.get('apellido','')}".strip(),
                        "Detalle":f"Estado de vacunas: {r.get('vacunas_completas')}","Prioridad":"Revisar"})
if {"tipo","id_persona","asistio"}.issubset(asistencia.columns):
    a = asistencia[asistencia["tipo"].astype(str).str.lower()=="alumno"].copy()
    aus = a[a["asistio"].astype(str).str.lower().isin(["no","ausente","falta"])]
    if not aus.empty:
        conteo = aus.groupby("id_persona").size().reset_index(name="Ausencias")
        conteo = conteo[conteo["Ausencias"] >= 2]
        alumnos_cols = [c for c in ["id_alumno","nombre","apellido","barrio"] if c in alumnos.columns]
        if alumnos_cols and "id_alumno" in alumnos.columns:
            conteo = conteo.merge(alumnos[alumnos_cols], left_on="id_persona", right_on="id_alumno", how="left")
        for _,r in conteo.iterrows():
            alertas.append({"Tipo":"Ausencias reiteradas","ID":r.get("id_persona"),"Persona":f"{r.get('nombre','')} {r.get('apellido','')}".strip(),
                            "Detalle":f"{int(r['Ausencias'])} ausencias registradas","Prioridad":"Revisar"})
if "estado" in pedidos.columns:
    pend = pedidos[pedidos["estado"].astype(str).str.lower().isin(["pendiente","demorado","pendiente de entrega"])].copy()
    if "id_insumo" in pend and "id_insumo" in insumos:
        pend = pend.merge(insumos, on="id_insumo", how="left")
    for _,r in pend.iterrows():
        alertas.append({"Tipo":"Pedido pendiente","ID":r.get("id_pedido"),"Persona":r.get("nombre",""),
                        "Detalle":f"{r.get('cantidad','')} unidades · {r.get('estado','')}","Prioridad":"Seguimiento"})

df = pd.DataFrame(alertas, columns=["Tipo","ID","Persona","Detalle","Prioridad"])
if df.empty:
    st.success("No se generaron alertas con los criterios actuales.")
else:
    c1,c2,c3 = st.columns(3)
    c1.metric("Alertas generadas",len(df))
    c2.metric("Tipos de alerta",df["Tipo"].nunique())
    c3.metric("Prioridad revisar",int((df["Prioridad"]=="Revisar").sum()))
    st.markdown("### Distribución por tipo")
    st.bar_chart(df["Tipo"].value_counts(), horizontal=True)
    filtro = st.multiselect("Filtrar tipos", sorted(df["Tipo"].unique()), default=sorted(df["Tipo"].unique()))
    vista = df[df["Tipo"].isin(filtro)]
    st.markdown("### Detalle de alertas")
    st.dataframe(vista, hide_index=True, use_container_width=True, height=420)
    st.download_button("Descargar alertas", vista.to_csv(index=False).encode("utf-8-sig"),
                       "alertas_demo.csv", "text/csv")
st.warning("Estas alertas son demostrativas. No constituyen diagnósticos ni decisiones automáticas: en un uso real, cualquier seguimiento debe ser revisado por el equipo responsable.")
