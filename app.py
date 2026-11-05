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

/* Fijar una apariencia clara y evitar texto blanco heredado del tema oscuro */
:root {
  color-scheme: light;
  --text-color: #193d33;
  --secondary-text-color: #5b6e64;
  --background-color: #f5f7f4;
  --secondary-background-color: #ffffff;
  --primary-color: #286b58;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
  background: #f5f7f4 !important;
  color: #193d33 !important;
}
.stMarkdown, .stMarkdown p, .stMarkdown li,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stText"],
[data-testid="stCaptionContainer"],
label, .stCaption {
  color: #40584d;
}
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
  font-family: 'Manrope', sans-serif;
  color: #193d33 !important;
  letter-spacing: -0.035em;
}
.block-container {
  padding-top: 2.1rem;
  padding-bottom: 3rem;
  max-width: 1450px;
}

/* Barra lateral */
[data-testid="stSidebar"] {
  background: #152f2a !important;
}
[data-testid="stSidebar"] * {
  color: #f2f7f2 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
  color: #c7d8d0 !important;
}

/* Portada */
.hero {
  padding: 2.2rem 2.4rem;
  border-radius: 24px;
  background: linear-gradient(120deg,#173d35 0%,#286b58 62%,#4e9273 100%);
  color: white !important;
  margin-bottom: 1.5rem;
}
.hero h1, .hero h2, .hero h3, .hero p, .hero span {
  color: white !important;
}
.hero h1 {
  font-size: clamp(2rem,4vw,3.1rem);
  margin: 0.2rem 0 0.6rem;
}
.hero p {
  color: #e1eee7 !important;
  font-size: 1.05rem;
  max-width: 850px;
}
.eyebrow {
  text-transform: uppercase;
  letter-spacing: .14em;
  font-size: .75rem;
  font-weight: 700;
  color: #b9d9c7 !important;
}
.section-kicker {
  color: #286b58 !important;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  font-size: .72rem;
}

/* Tarjetas y métricas */
.info-card {
  background: #ffffff !important;
  color: #193d33 !important;
  border: 1px solid #e3eae4;
  border-radius: 18px;
  padding: 1.1rem 1.25rem;
  min-height: 125px;
  box-shadow: 0 5px 18px rgba(20,55,42,.045);
}
.info-card h3 {
  font-size: 1.02rem;
  margin: .2rem 0 .45rem;
  color: #193d33 !important;
}
.info-card p {
  color: #5b6e64 !important;
  margin: 0;
  font-size: .92rem;
}
div[data-testid="stMetric"] {
  background: #ffffff !important;
  color: #193d33 !important;
  border: 1px solid #e3eae4;
  padding: 1rem 1.1rem;
  border-radius: 16px;
  box-shadow: 0 5px 18px rgba(20,55,42,.04);
}
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] * {
  color: #63756b !important;
}
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
  color: #193d33 !important;
}

/* Controles, tablas y separadores */
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {border-radius: 10px 10px 0 0;}
div[data-testid="stDataFrame"] {
  border: 1px solid #e3eae4;
  border-radius: 12px;
  overflow: hidden;
}
hr {border-color: #e1e9e2;}
.small-note {font-size: .84rem; color: #64766c !important;}

/* Enlaces y elementos de formulario sobre fondos claros */
.stApp a {color: #286b58;}
.stApp input, .stApp textarea {
  color: #193d33;
}
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
