import streamlit as st
import matplotlib.pyplot as plt
import datos
import graficos as g

@st.cache_data
def cargar():
    return datos.cargar_anio(), datos.cargar_ugl()

def mostrar(fig):
    if fig is None:
        st.info("No hay datos disponibles.")
    else:
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

st.markdown('<div class="section-kicker">03 · DATOS ABIERTOS</div>', unsafe_allow_html=True)
st.title("Campaña de vacunación antigripal · PAMI")
st.write("Análisis complementario de datos abiertos de PAMI. Esta información es independiente del conjunto ficticio del EPI.")
try:
    anio, ugl = cargar()
except Exception as e:
    st.error(f"No se pudieron cargar los datos abiertos de PAMI: {type(e).__name__}. Revisá la conexión e intentá nuevamente.")
    st.stop()
if not anio.empty:
    mx, mn = anio.loc[anio["total"].idxmax()], anio.loc[anio["total"].idxmin()]
    a,b,c = st.columns(3)
    a.metric("Mayor registro", f"{int(mx['total']):,}".replace(",","."), f"Año {int(mx['anio'])}")
    b.metric("Menor registro", f"{int(mn['total']):,}".replace(",","."), f"Año {int(mn['anio'])}")
    c.metric("Promedio anual", f"{round(anio['total'].mean()):,}".replace(",","."))
    st.markdown("### Evolución anual")
    mostrar(g.grafico_barras(anio.set_index("anio")["total"], "Vacunas aplicadas por año"))
    with st.expander("Ver tabla anual completa"):
        st.dataframe(anio, hide_index=True, use_container_width=True)
st.markdown("### Comparación por Unidad de Gestión Local")
if not ugl.empty:
    sde = ugl[ugl["ugl"].str.upper()=="SANTIAGO DEL ESTERO"]
    if not sde.empty:
        fila=sde.iloc[0]
        x,y,z=st.columns(3)
        x.metric("Santiago del Estero",f"{int(fila['total']):,}".replace(",","."))
        y.metric("Puesto",f"{int(fila['puesto'])} de {len(ugl)}")
        z.metric("Mediana de UGL",f"{int(ugl['total'].median()):,}".replace(",","."))
    st.bar_chart(ugl.set_index("ugl")["total"], horizontal=True, height=500)
    buscar=st.text_input("Buscar una UGL")
    tabla=ugl[ugl["ugl"].str.contains(buscar,case=False,na=False)] if buscar else ugl
    st.dataframe(tabla,hide_index=True,use_container_width=True)
st.info("Los totales absolutos no equivalen a tasas de cobertura: para calcular cobertura se necesita conocer la población objetivo.")
