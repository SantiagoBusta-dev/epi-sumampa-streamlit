"""EPI Sumampa — aplicación multipágina para Práctica Profesionalizante II."""
import streamlit as st

st.set_page_config(
    page_title="EPI Sumampa | De los cuadernos a los datos",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'DM Sans', sans-serif;}
h1, h2, h3 {font-family: 'Manrope', sans-serif; letter-spacing: -0.035em;}
.stApp {background: #f5f7f4;}
[data-testid="stSidebar"] {background: #152f2a;}
[data-testid="stSidebar"] * {color: #f2f7f2 !important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color:#c7d8d0 !important;}
.block-container {padding-top: 2.1rem; padding-bottom: 3rem; max-width: 1450px;}
.hero {
  padding: 2.2rem 2.4rem; border-radius: 24px;
  background: linear-gradient(120deg,#173d35 0%,#286b58 62%,#4e9273 100%);
  color: white; margin-bottom: 1.5rem;
}
.hero h1 {color:white; font-size: clamp(2rem,4vw,3.1rem); margin:0.2rem 0 0.6rem;}
.hero p {color:#e1eee7; font-size:1.05rem; max-width:850px;}
.eyebrow {text-transform:uppercase; letter-spacing:.14em; font-size:.75rem; font-weight:700; color:#b9d9c7;}
.section-kicker {color:#43836a; font-weight:700; letter-spacing:.1em; text-transform:uppercase; font-size:.72rem;}
.info-card {
 background:white; border:1px solid #e3eae4; border-radius:18px;
 padding:1.1rem 1.25rem; min-height:125px;
 box-shadow:0 5px 18px rgba(20,55,42,.045);
}
.info-card h3 {font-size:1.02rem; margin:.2rem 0 .45rem; color:#193d33;}
.info-card p {color:#5b6e64; margin:0; font-size:.92rem;}
div[data-testid="stMetric"] {
 background:white; border:1px solid #e3eae4; padding:1rem 1.1rem;
 border-radius:16px; box-shadow:0 5px 18px rgba(20,55,42,.04);
}
div[data-testid="stMetricLabel"] {color:#63756b;}
div[data-testid="stMetricValue"] {color:#193d33;}
.stTabs [data-baseweb="tab-list"] {gap:8px;}
.stTabs [data-baseweb="tab"] {border-radius:10px 10px 0 0;}
div[data-testid="stDataFrame"] {border:1px solid #e3eae4; border-radius:12px; overflow:hidden;}
hr {border-color:#e1e9e2;}
.small-note {font-size:.84rem; color:#64766c;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🌱 EPI SUMAMPA")
st.sidebar.caption("De los cuadernos a los datos")
st.sidebar.markdown("---")
st.sidebar.caption("PRÁCTICA PROFESIONALIZANTE II · GRUPO 2")
st.sidebar.caption("ITSE · Sede Sumampa")
st.sidebar.markdown("---")
st.sidebar.caption("Navegá por las secciones para conocer el proyecto, explorar los datos y revisar el análisis.")

paginas = [
    st.Page("pages/01_inicio.py", title="Inicio", icon="🏠", default=True),
    st.Page("pages/02_epi.py", title="Panel del EPI", icon="🌱"),
    st.Page("pages/03_alertas.py", title="Alertas y seguimiento", icon="🔎"),
    st.Page("pages/04_pami.py", title="Análisis PAMI", icon="📈"),
    st.Page("pages/05_puntos.py", title="Puntos de vacunación", icon="📍"),
    st.Page("pages/06_metodologia.py", title="Metodología y privacidad", icon="🧭"),
]
nav = st.navigation(paginas)
nav.run()
