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

anio, ugl = cargar()
st.markdown('<div class="section-kicker">03 · DATOS ABIERTOS</div>', unsafe_allow_html=True)
st.title("Campaña de vacunación antigripal · PAMI")
st.write("Esta sección analiza datos abiertos publicados por PAMI. Se presentan como un análisis complementario y no como información del EPI.")

if not anio.empty:
    mx, mn = anio.loc[anio["total"].idxmax()], anio.loc[anio["total"].idxmin()]
    a, b, c = st.columns(3)
    a.metric("Mayor registro", f"{int(mx['total']):,}".replace(",", "."), f"Año {int(mx['anio'])}")
    b.metric("Menor registro", f"{int(mn['total']):,}".replace(",", "."), f"Año {int(mn['anio'])}")
    c.metric("Promedio anual", f"{round(anio['total'].mean()):,}".replace(",", "."))
    st.markdown("### Evolución anual")
    mostrar(g.anio(anio))
    with st.expander("Consultar tabla anual"):
        st.dataframe(anio, hide_index=True, use_container_width=True)
else:
    st.warning("No se encontraron registros anuales.")

st.markdown("### Comparación por Unidad de Gestión Local")
if not ugl.empty:
    sde = ugl[ugl["ugl"].str.upper() == "SANTIAGO DEL ESTERO"]
    if not sde.empty:
        fila = sde.iloc[0]
        x, y, z = st.columns(3)
        x.metric("Santiago del Estero", f"{int(fila['total']):,}".replace(",", "."))
        y.metric("Puesto", f"{int(fila['puesto'])} de {len(ugl)}")
        z.metric("Mediana de UGL", f"{int(ugl['total'].median()):,}".replace(",", "."))
    else:
        st.info("El archivo no contiene una fila identificada como Santiago del Estero.")
    mostrar(g.ugl(ugl))
    buscar = st.text_input("Buscar una UGL", placeholder="Escribí el nombre de una jurisdicción")
    tabla = ugl[ugl["ugl"].str.contains(buscar, case=False, na=False)] if buscar else ugl
    st.dataframe(tabla[["puesto", "ugl", "beneficiarios", "agentes", "total", "%_del_total"]], hide_index=True, use_container_width=True)

st.info("Las cantidades son valores absolutos. Como el archivo no incluye la población objetivo ni las dosis disponibles, no permiten calcular cobertura ni explicar por sí solas las diferencias entre UGL.")
