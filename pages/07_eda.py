import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datos

@st.cache_data
def cargar():
    return datos.leer_epi()

tablas=cargar()
st.markdown('<div class="section-kicker">06 · EXPLORACIÓN DE DATOS</div>',unsafe_allow_html=True)
st.title("EDA ampliado")
st.write("Análisis exploratorio de las siete tablas: estructura, calidad, distribuciones, variables numéricas y relaciones.")
total=sum(len(d) for d in tablas.values())
cols=st.columns(4)
cols[0].metric("Tablas",len(tablas))
cols[1].metric("Registros",f"{total:,}".replace(",","."))
cols[2].metric("Columnas",sum(len(d.columns) for d in tablas.values()))
cols[3].metric("Tablas relacionadas",3)
resumen=[]
for nombre,df in tablas.items():
    resumen.append({"Tabla":nombre.replace("_"," ").title(),"Registros":len(df),"Variables":len(df.columns),
                    "Celdas vacías":int(df.replace("",pd.NA).isna().sum().sum()),"Duplicados":int(df.duplicated().sum())})
st.markdown("### Resumen general")
st.dataframe(pd.DataFrame(resumen),hide_index=True,use_container_width=True)
seleccion=st.selectbox("Seleccioná una tabla",list(tablas),format_func=lambda x:x.replace("_"," ").title())
df=tablas[seleccion].copy()
st.markdown(f"### {seleccion.replace('_',' ').title()}")
a,b,c=st.columns(3)
a.metric("Registros",len(df))
b.metric("Variables",len(df.columns))
c.metric("Duplicados exactos",int(df.duplicated().sum()))
calidad=pd.DataFrame({
    "Variable":df.columns,
    "Tipo": [str(df[col].dtype) for col in df.columns],
    "Valores vacíos":[int(df[col].replace("",pd.NA).isna().sum()) for col in df.columns],
    "Valores distintos":[int(df[col].nunique(dropna=True)) for col in df.columns],
})
st.markdown("#### Calidad de datos")
st.dataframe(calidad,hide_index=True,use_container_width=True)
cat=[c for c in df.columns if df[c].nunique(dropna=True)<=30 and not c.startswith("id_")]
num=[c for c in df.columns if pd.to_numeric(df[c],errors="coerce").notna().sum()>0 and not c.startswith("id_")]
left,right=st.columns(2)
with left:
    if cat:
        campo=st.selectbox("Variable categórica",cat)
        conteo=df[campo].fillna("Sin dato").astype(str).value_counts()
        st.bar_chart(conteo,horizontal=True,height=320)
    else:
        st.info("No se detectaron variables categóricas para graficar.")
with right:
    if num:
        campo_num=st.selectbox("Variable numérica",num)
        serie=pd.to_numeric(df[campo_num],errors="coerce").dropna()
        if not serie.empty:
            st.dataframe(serie.describe().rename("Estadístico").to_frame(),use_container_width=True)
            fig,ax=plt.subplots(figsize=(6,3))
            serie.plot(kind="hist",bins=min(15,max(5,serie.nunique())),ax=ax)
            ax.set_title(f"Distribución de {campo_num}")
            fig.tight_layout()
            st.pyplot(fig,use_container_width=True)
            plt.close(fig)
    else:
        st.info("No se detectaron variables numéricas para resumir.")
st.markdown("#### Matriz de correlación (si hay varias variables numéricas)")
numericas=df.select_dtypes(include="number")
if numericas.shape[1]>=2:
    st.dataframe(numericas.corr(numeric_only=True).round(2),use_container_width=True)
else:
    st.caption("Esta tabla no contiene al menos dos variables numéricas.")
st.markdown("### Tabla completa")
st.dataframe(df,hide_index=True,use_container_width=True,height=480)
st.download_button("Descargar esta tabla completa",df.to_csv(index=False).encode("utf-8-sig"),
                   file_name=f"{seleccion}.csv",mime="text/csv")
if seleccion=="alumno_tutor":
    alumnos=tablas.get("alumnos",pd.DataFrame())
    tutores=tablas.get("tutores",pd.DataFrame())
    if not alumnos.empty and not tutores.empty:
        cruce=df.merge(alumnos,on="id_alumno",how="left").merge(tutores,on="id_tutor",how="left",suffixes=("_alumno","_tutor"))
        st.markdown("### Cruce de alumnos y tutores")
        st.dataframe(cruce,hide_index=True,use_container_width=True,height=420)
        st.download_button("Descargar cruce alumno-tutor",cruce.to_csv(index=False).encode("utf-8-sig"),
                           "cruce_alumno_tutor.csv","text/csv")
st.caption("Los datos de esta sección son ficticios y se presentan completos para fines de exploración y demostración.")
