import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datos

@st.cache_data
def cargar():
    return datos.leer_epi()

def mostrar_tabla(df, nombre):
    st.dataframe(df, hide_index=True, use_container_width=True, height=380)
    st.download_button(
        f"Descargar tabla {nombre}.csv",
        df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{nombre}.csv",
        mime="text/csv",
        key=f"download_{nombre}"
    )

def grafico_conteo(df, columna, titulo):
    if columna not in df.columns or df.empty:
        return
    conteo = df[columna].fillna("Sin dato").astype(str).value_counts()
    st.bar_chart(conteo, horizontal=True, height=280)

def mostrar_tabla_y_graficos(df, nombre, categorias=None, numeros=None):
    st.markdown(f"### {nombre.replace('_',' ').title()}")
    k1,k2 = st.columns(2)
    k1.metric("Registros", len(df))
    k2.metric("Variables", len(df.columns))
    categorias = categorias or []
    numeros = numeros or []
    if categorias:
        cols = st.columns(min(2, len(categorias)))
        for i, campo in enumerate(categorias):
            with cols[i % len(cols)]:
                grafico_conteo(df, campo, campo)
                st.caption(f"Distribución de {campo.replace('_',' ')}")
    if numeros:
        cols = st.columns(min(2, len(numeros)))
        for i, campo in enumerate(numeros):
            with cols[i % len(cols)]:
                serie = pd.to_numeric(df[campo], errors="coerce").dropna()
                if not serie.empty:
                    fig, ax = plt.subplots(figsize=(6,3))
                    serie.plot(kind="hist", bins=min(15, max(5, serie.nunique())), ax=ax)
                    ax.set_title(f"Distribución de {campo.replace('_',' ')}")
                    ax.set_xlabel(campo)
                    fig.tight_layout()
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
    with st.expander(f"Ver todos los registros de {nombre.replace('_',' ')}", expanded=True):
        mostrar_tabla(df, nombre)

tablas = cargar()
alumnos = tablas.get("alumnos", pd.DataFrame())
asistencia = tablas.get("asistencia", pd.DataFrame())
tutores = tablas.get("tutores", pd.DataFrame())
docentes = tablas.get("docentes", pd.DataFrame())
insumos = tablas.get("insumos", pd.DataFrame())
pedidos = tablas.get("pedidos", pd.DataFrame())
relaciones = tablas.get("alumno_tutor", pd.DataFrame())

st.markdown('<div class="section-kicker">01 · EXPLORACIÓN INTEGRAL</div>', unsafe_allow_html=True)
st.title("Panel integral del EPI")
st.write("El conjunto ficticio está organizado en siete tablas. Elegí una sección para consultar sus indicadores, gráficos y registros completos.")
m = st.columns(5)
m[0].metric("Alumnos", len(alumnos))
m[1].metric("Tutores", len(tutores))
m[2].metric("Docentes", len(docentes))
m[3].metric("Asistencias", len(asistencia))
m[4].metric("Pedidos", len(pedidos))

tabs = st.tabs(["Alumnos", "Asistencia", "Tutores", "Docentes", "Insumos", "Pedidos", "Vínculos"])
with tabs[0]:
    st.markdown("#### Filtros de alumnos")
    c1,c2,c3 = st.columns(3)
    barrios = sorted(alumnos["barrio"].dropna().unique()) if "barrio" in alumnos else []
    vacunas = sorted(alumnos["vacunas_completas"].dropna().unique()) if "vacunas_completas" in alumnos else []
    edades = sorted(pd.to_numeric(alumnos["edad"], errors="coerce").dropna().unique()) if "edad" in alumnos else []
    barrio_sel = c1.multiselect("Barrio", barrios, default=barrios)
    vacuna_sel = c2.multiselect("Vacunación completa", vacunas, default=vacunas)
    edad_sel = c3.multiselect("Edad", edades, default=edades)
    filtrado = alumnos.copy()
    if "barrio" in filtrado: filtrado = filtrado[filtrado["barrio"].isin(barrio_sel)]
    if "vacunas_completas" in filtrado: filtrado = filtrado[filtrado["vacunas_completas"].isin(vacuna_sel)]
    if "edad" in filtrado: filtrado = filtrado[pd.to_numeric(filtrado["edad"], errors="coerce").isin(edad_sel)]
    mostrar_tabla_y_graficos(filtrado, "alumnos", ["barrio","vacunas_completas"], ["edad"])
with tabs[1]:
    c1,c2 = st.columns(2)
    tipos = sorted(asistencia["tipo"].dropna().unique()) if "tipo" in asistencia else []
    estados = sorted(asistencia["asistio"].dropna().unique()) if "asistio" in asistencia else []
    tipo_sel = c1.multiselect("Tipo de persona", tipos, default=tipos)
    estado_sel = c2.multiselect("Asistencia", estados, default=estados)
    filtrado = asistencia.copy()
    if "tipo" in filtrado: filtrado = filtrado[filtrado["tipo"].isin(tipo_sel)]
    if "asistio" in filtrado: filtrado = filtrado[filtrado["asistio"].isin(estado_sel)]
    mostrar_tabla_y_graficos(filtrado, "asistencia", ["tipo","asistio"])
    if "fecha" in filtrado:
        fechas = pd.to_datetime(filtrado["fecha"], errors="coerce")
        por_fecha = fechas.value_counts().sort_index()
        st.line_chart(por_fecha, height=260)
with tabs[2]:
    mostrar_tabla_y_graficos(tutores, "tutores", ["relacion"])
with tabs[3]:
    mostrar_tabla_y_graficos(docentes, "docentes", ["rol"])
with tabs[4]:
    mostrar_tabla_y_graficos(insumos, "insumos", ["categoria","nombre"])
with tabs[5]:
    c1,c2 = st.columns(2)
    estados_p = sorted(pedidos["estado"].dropna().unique()) if "estado" in pedidos else []
    estado_p = c1.multiselect("Estado del pedido", estados_p, default=estados_p)
    p = pedidos[pedidos["estado"].isin(estado_p)] if "estado" in pedidos else pedidos
    mostrar_tabla_y_graficos(p, "pedidos", ["estado"], ["cantidad"])
    if not p.empty and {"id_insumo","cantidad"}.issubset(p.columns) and "id_insumo" in insumos:
        unidos = p.merge(insumos, on="id_insumo", how="left", suffixes=("_pedido","_insumo"))
        st.markdown("#### Pedidos vinculados con el nombre del insumo")
        st.dataframe(unidos, hide_index=True, use_container_width=True)
with tabs[6]:
    st.markdown("#### Relación entre alumnos y tutores")
    if not relaciones.empty and {"id_alumno","id_tutor"}.issubset(relaciones.columns):
        unidos = relaciones.merge(alumnos, on="id_alumno", how="left", suffixes=("","_alumno"))
        unidos = unidos.merge(tutores, on="id_tutor", how="left", suffixes=("_alumno","_tutor"))
        st.metric("Vínculos registrados", len(unidos))
        st.dataframe(unidos, hide_index=True, use_container_width=True, height=420)
        st.download_button("Descargar vínculos completos", unidos.to_csv(index=False).encode("utf-8-sig"),
                           "vinculos_alumno_tutor.csv", "text/csv")
    else:
        st.dataframe(relaciones, hide_index=True, use_container_width=True)
st.caption("Los registros son ficticios y se muestran completos para demostrar las posibilidades de exploración del sistema.")
