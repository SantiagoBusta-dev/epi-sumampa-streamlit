"""App de Streamlit — Digitalización y análisis de datos del EPI Sumampa.
PP2 · Grupo 2 · ITSE Sede Sumampa.

Ejecutar:  streamlit run app.py
"""
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import datos
import graficos as g

st.set_page_config(page_title="EPI Sumampa · Datos", page_icon="📊", layout="wide")


def mostrar(fig, vacio="No hay datos para este filtro."):
    """Dibuja una figura de matplotlib (o avisa si no hay datos)."""
    if fig is None:
        st.info(vacio)
        return
    st.pyplot(fig)
    plt.close(fig)


@st.cache_data
def cargar_epi():
    return datos.leer_epi()


@st.cache_data
def cargar_pami():
    return datos.cargar_anio(), datos.cargar_ugl()


@st.cache_data(ttl=24 * 3600, show_spinner=False)
def descargar_puntos():
    return datos.cargar_puntos(datos.leer_texto("puntos"))


alumnos, asistencia, insumos, pedidos, alertas = cargar_epi()
anio, ugl = cargar_pami()

st.title("📊 EPI Sumampa: de los registros en papel a los datos")
st.caption("Práctica Profesionalizante II · Grupo 2 · ITSE Sede Sumampa")

t_proy, t_epi, t_alertas, t_anio, t_puntos, t_fuentes = st.tabs(
    ["El proyecto", "EPI (datos ficticios)", "Alertas", "Vacunas antigripales (PAMI)", "Puntos de vacunación (PAMI)", "Fuentes"])

# ------------------------------------------------------------------------------ 1. El proyecto
with t_proy:
    st.subheader("El problema")
    st.write("El EPI (Espacio de Primera Infancia) de Sumampa guarda todos sus registros en papel: alumnos, asistencia, "
             "vacunación, seguro e insumos. Eso hace lento y poco confiable consultarlos y reportarlos.")
    st.subheader("Qué construimos")
    st.markdown("""
1. **Un dataset ficticio** de 16 alumnos de 2 a 3 años (no hubo autorización ni tiempo para usar datos reales).
2. **Preprocesamiento:** se detectan y corrigen errores de carga (duplicado, barrio mal escrito, seguro vacío) y se marca una inconsistencia de vacunación.
3. **EDA y reglas de alerta:** vacunación incompleta, seguro sin confirmar, ausencias repetidas, stock bajo y pedidos pendientes.
4. **Datos abiertos relacionados (PAMI):** vacunas antigripales por año y por UGL, y puntos de vacunación, para sumar contexto y volumen.
""")
    c1, c2, c3 = st.columns(3)
    c1.metric("Alumnos (ficticios)", len(alumnos))
    c2.metric("Alertas generadas", len(alertas))
    c3.metric("Dataset PAMI por UGL (filas)", len(ugl))
    st.warning("Los datos del EPI son **ficticios**: sirven para probar el flujo completo, no describen a los niños reales. "
               "Los datos de PAMI son de **beneficiarios del Instituto**, no de población infantil.")

# ------------------------------------------------------------------------------ 2. EPI
with t_epi:
    st.subheader("Dashboard del EPI (dataset ficticio)")
    f1, f2 = st.columns(2)
    turnos = f1.multiselect("Turno", sorted(alumnos["turno"].unique()), default=sorted(alumnos["turno"].unique()))
    barrios_sel = f2.multiselect("Barrio", ["Centro", "Norte", "Sur"], default=["Centro", "Norte", "Sur"])
    a = alumnos[alumnos["turno"].isin(turnos) & alumnos["barrio"].isin(barrios_sel)]
    asis_al = asistencia[(asistencia["tipo"] == "Alumno") & asistencia["id_persona"].isin(a["id_alumno"])]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Alumnos", len(a))
    m2.metric("Vacunas completas", f"{(a['vacunas_completas'] == 'Si').mean() * 100:.0f}%" if len(a) else "—")
    m3.metric("Seguro sin confirmar", int((a["seguro"] != "Si").sum()))
    m4.metric("Asistencia", f"{asis_al['asistio_bool'].mean() * 100:.0f}%" if len(asis_al) else "—")

    c1, c2 = st.columns(2)
    with c1:
        mostrar(g.barrios(a))
        mostrar(g.vacunacion_barrio(a))
        mostrar(g.asistencia_dia(asis_al))
    with c2:
        mostrar(g.edad_turno(a))
        mostrar(g.seguro(a))
        mostrar(g.ausencias(asis_al))
    st.markdown("#### Insumos")
    mostrar(g.stock(insumos))
    st.dataframe(pedidos.merge(insumos[["id_insumo", "nombre"]], on="id_insumo")[["fecha", "nombre", "cantidad", "estado"]],
                 hide_index=True)
    st.caption("Datos ficticios. Con 16 alumnos y una semana de asistencia no se hacen pruebas estadísticas: lo útil es identificar quién requiere atención.")

# ------------------------------------------------------------------------------ 3. Alertas
with t_alertas:
    st.subheader("Reporte de alertas")
    tipos = st.multiselect("Tipo de alerta", sorted(alertas["tipo"].unique()), default=sorted(alertas["tipo"].unique()))
    rep = alertas[alertas["tipo"].isin(tipos)]
    st.write(f"{len(rep)} alertas")
    st.dataframe(rep, hide_index=True)
    st.markdown("#### Consulta rápida por DNI")
    ejemplo = alumnos.loc[alumnos["tiene_alergia"], "dni"].iloc[0] if alumnos["tiene_alergia"].any() else ""
    dni = st.text_input("DNI del alumno (ficticio)", placeholder=f"Ejemplo: {ejemplo}")
    if dni.strip():
        ficha = alumnos[alumnos["dni"] == dni.strip()][["id_alumno", "nombre", "apellido", "dni", "edad", "barrio", "turno",
                                                        "vacunas_completas", "carnet_vacunas", "seguro", "alergias"]]
        if ficha.empty:
            st.error("No hay ningún alumno con ese DNI.")
        else:
            st.dataframe(ficha, hide_index=True)
    st.caption("Los umbrales (2 ausencias en la semana, stock mínimo) son supuestos del grupo.")

# ------------------------------------------------------------------------------ 4. Antigripal
with t_anio:
    st.subheader("Vacunas antigripales aplicadas por PAMI")
    mx, mn = anio.loc[anio["total"].idxmax()], anio.loc[anio["total"].idxmin()]
    m1, m2, m3 = st.columns(3)
    m1.metric("Máximo", f"{int(mx['total']):,}".replace(",", "."), f"año {int(mx['anio'])}", delta_color="off")
    m2.metric("Mínimo", f"{int(mn['total']):,}".replace(",", "."), f"año {int(mn['anio'])}", delta_color="off")
    m3.metric("Promedio anual", f"{round(anio['total'].mean()):,}".replace(",", "."))
    mostrar(g.anio(anio))
    st.dataframe(anio, hide_index=True)
    st.info("El total cambia mucho de un año a otro (−32,5% en 2010, +88,4% en 2016): un solo año no alcanza para evaluar la vacunación. "
            "El dataset no trae las dosis disponibles ni la población objetivo, por lo que no se pueden explicar las causas.")

    st.markdown("#### Por UGL (2019)")
    sde = ugl[ugl["ugl"] == "SANTIAGO DEL ESTERO"].iloc[0]
    k1, k2, k3 = st.columns(3)
    k1.metric("Santiago del Estero", f"{int(sde['total']):,}".replace(",", "."))
    k2.metric("Puesto", f"{int(sde['puesto'])} de {len(ugl)}")
    k3.metric("Mediana de las UGL", f"{int(ugl['total'].median()):,}".replace(",", "."))
    mostrar(g.ugl(ugl))
    buscar = st.text_input("Buscar UGL", placeholder="Ejemplo: Tucumán")
    tabla = ugl[ugl["ugl"].str.contains(datos.normalizar(buscar) or "", case=False, na=False)] if buscar else ugl
    st.dataframe(tabla[["puesto", "ugl", "beneficiarios", "agentes", "total", "%_del_total"]], hide_index=True)
    st.info("Son cantidades absolutas, no tasas: dependen de cuántos beneficiarios tiene cada UGL, dato que el archivo no incluye.")

# ------------------------------------------------------------------------------ 5. Puntos
with t_puntos:
    st.subheader("Puntos de vacunación de PAMI")
    st.write("Este dataset aporta volumen (miles de filas). Se descarga del portal de PAMI al presionar el botón. "
             "Si la descarga falla, se puede subir el archivo manualmente.")
    subido = st.file_uploader("…o subir el CSV descargado", type=["csv"])
    if "puntos" not in st.session_state:
        st.session_state["puntos"] = None
    if st.button("Descargar y analizar"):
        try:
            with st.spinner("Descargando y limpiando el archivo…"):
                st.session_state["puntos"] = descargar_puntos()
        except Exception as e:            # sin internet, portal caído, etc.
            st.error(f"No se pudo descargar el archivo ({type(e).__name__}). Descargalo del portal y subilo arriba.")
    if subido is not None:
        st.session_state["puntos"] = datos.cargar_puntos(datos.decodificar(subido.getvalue()))

    if st.session_state["puntos"] is not None:
        puntos, resumen = st.session_state["puntos"]
        cols = st.columns(len(resumen))
        for col, (k, v) in zip(cols, resumen.items()):
            col.metric(k.capitalize(), v)
        por_prov = datos.puntos_por_provincia(puntos)
        mostrar(g.puntos_provincia(por_prov))
        n_sde = int(por_prov.get("SANTIAGO DEL ESTERO", 0))
        st.metric("Puntos en Santiago del Estero", n_sde)
        st.markdown("#### Vacunas aplicadas por punto de vacunación (2019, por UGL)")
        rel = datos.aplicaciones_por_punto(puntos, ugl)
        st.dataframe(rel[["ugl", "puntos", "total", "aplicaciones_por_punto"]], hide_index=True)
        st.caption("El cruce usa el código de UGL contenido en el id de cada punto (901… = UGL 1, etc.). Conviene verificarlo con la provincia más frecuente de cada UGL.")
        with st.expander("Calidad de los datos: domicilios repetidos y provincias no reconocidas"):
            st.write(puntos["domicilio"].value_counts().head(5))
            st.write(puntos.loc[~puntos["reconocida"], "provincia"].value_counts().head(8))

# ------------------------------------------------------------------------------ 6. Fuentes
with t_fuentes:
    st.subheader("Fuentes y licencias")
    for nombre, url in datos.LINKS.items():
        st.markdown(f"- [{nombre}]({url})")
    st.markdown("**Licencia:** Creative Commons Attribution 4.0 (portal de datos abiertos de PAMI, INSSJP).")
    st.markdown("**Datos del EPI:** ficticios, generados por el grupo con una semilla fija (`random.seed(2026)`).")
    st.markdown("**Código y notebooks:** carpeta del proyecto (Etapas 1 a 5).")
