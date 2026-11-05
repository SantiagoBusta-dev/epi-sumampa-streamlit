import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datos
import graficos as g

@st.cache_data
def cargar():
    return datos.leer_epi()

def mostrar(fig):
    if fig is None:
        st.info("No hay datos para mostrar con los filtros seleccionados.")
    else:
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

alumnos, asistencia, insumos, pedidos, alertas = cargar()
st.markdown('<div class="section-kicker">01 · INFORMACIÓN DEL EPI</div>', unsafe_allow_html=True)
st.title("Panel de seguimiento")
st.write("Exploración de registros de demostración. Podés filtrar por turno y barrio para observar cómo cambian los indicadores.")

f1, f2 = st.columns(2)
turnos_disp = sorted(alumnos["turno"].dropna().unique())
barrios_disp = sorted(alumnos["barrio"].dropna().unique())
turnos = f1.multiselect("Turno", turnos_disp, default=turnos_disp)
barrios = f2.multiselect("Barrio", barrios_disp, default=barrios_disp)
a = alumnos[alumnos["turno"].isin(turnos) & alumnos["barrio"].isin(barrios)]
asis = asistencia[(asistencia["tipo"] == "Alumno") & asistencia["id_persona"].isin(a["id_alumno"])]

st.markdown("### Indicadores principales")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Alumnos", len(a))
m2.metric("Vacunas completas", f"{(a['vacunas_completas'] == 'Si').mean()*100:.0f}%" if len(a) else "—")
m3.metric("Seguro sin confirmar", int((a["seguro"] != "Si").sum()) if len(a) else 0)
m4.metric("Asistencia registrada", f"{asis['asistio_bool'].mean()*100:.0f}%" if len(asis) else "—")

st.markdown("### Características de los registros")
left, right = st.columns(2)
with left:
    st.markdown("**Distribución territorial**")
    mostrar(g.barrios(a))
    st.markdown("**Vacunación por barrio**")
    mostrar(g.vacunacion_barrio(a))
    st.markdown("**Asistencia por día**")
    mostrar(g.asistencia_dia(asis))
with right:
    st.markdown("**Edades según turno**")
    mostrar(g.edad_turno(a))
    st.markdown("**Situación del seguro**")
    mostrar(g.seguro(a))
    st.markdown("**Ausencias registradas**")
    mostrar(g.ausencias(asis))

st.markdown("### Insumos y pedidos")
x, y = st.columns([1, 1])
with x:
    mostrar(g.stock(insumos))
with y:
    st.dataframe(pedidos.merge(insumos[["id_insumo", "nombre"]], on="id_insumo")[["fecha", "nombre", "cantidad", "estado"]], hide_index=True, use_container_width=True)

with st.expander("Ver tabla de registros ficticios"):
    st.dataframe(a.drop(columns=["dni", "nombre", "apellido"], errors="ignore"), hide_index=True, use_container_width=True)

st.caption("Los datos son simulados. Con una muestra pequeña y un período breve no corresponde sacar conclusiones estadísticas generales.")
