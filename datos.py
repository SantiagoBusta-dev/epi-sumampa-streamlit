"""Carga y limpieza de datos para la app de Streamlit (EPI Sumampa, PP2 · Grupo 2 · ITSE).

No usa Streamlit: así se puede probar por separado.
"""
import io
import unicodedata
import urllib.request
from pathlib import Path

import pandas as pd

_BASE = Path(__file__).parent
DATA = _BASE / "data" if (_BASE / "data").exists() else _BASE   # funciona con la carpeta data/ o con los CSV en la raíz
BASE = "http://datos.pami.org.ar/dataset/"

# Datasets de PAMI (INSSJP) en el portal de datos abiertos. Licencia CC BY 4.0.
FUENTES = {
    "anio": ("pami_vacunas_antigripales_por_anio.csv",
             BASE + "ef69efec-b9c3-4a06-a245-49ed592ea0dc/resource/b4e7d4b4-5272-4663-a7d1-90c9e802151e/download/vacunas-antigripales-aplicadas-por-anio.csv"),
    "ugl": ("pami_vacunas_antigripales_2019_por_ugl.csv",
            BASE + "ef69efec-b9c3-4a06-a245-49ed592ea0dc/resource/38516bab-ab62-4b47-852f-76ef57340223/download/vacunas-antigripales-aplicadas-por-ugl.csv"),
    "puntos": ("pami_puntos_de_vacunacion.csv",
               BASE + "e7a05259-51a8-4f8f-8800-5aa02a96b64d/resource/2ce15ce1-4d69-41c8-84b9-27a068ba4017/download/listado-puntos-vacunacion.csv"),
}
LINKS = {
    "Campaña de vacunación antigripal (PAMI)": "https://datos.pami.org.ar/dataset/campana-vacunacion",
    "Puntos de vacunación (PAMI)": "https://datos.pami.org.ar/dataset/puntos-de-vacunacion",
    "Campaña de vacunación antigripal (Datos Argentina)": "https://datos.gob.ar/dataset/campana-vacunacion",
    "Puntos de vacunación (Datos Argentina)": "https://datos.gob.ar/dataset/puntos-de-vacunacion",
}


# ---------------------------------------------------------------- EPI (datos ficticios)
def leer_epi():
    alumnos = pd.read_csv(DATA / "alumnos.csv", dtype={"dni": str})
    asistencia = pd.read_csv(DATA / "asistencia.csv", parse_dates=["fecha"])
    insumos = pd.read_csv(DATA / "insumos.csv")
    pedidos = pd.read_csv(DATA / "pedidos.csv", parse_dates=["fecha"])
    alertas = pd.read_csv(DATA / "reporte_alertas.csv")
    return alumnos, asistencia, insumos, pedidos, alertas


# ---------------------------------------------------------------- PAMI
def decodificar(datos):
    try:
        return datos.decode("utf-8")
    except UnicodeDecodeError:
        return datos.decode("cp1252", errors="replace")


def leer_texto(clave):
    """Usa la copia local si existe; si no, descarga el archivo del portal de PAMI."""
    nombre, url = FUENTES[clave]
    ruta = DATA / nombre
    if ruta.exists():
        return decodificar(ruta.read_bytes())
    pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return decodificar(urllib.request.urlopen(pedido, timeout=60).read())


def _entero(serie):
    # Los números vienen con punto de miles (1.500): se leen como texto y se convierten.
    return serie.str.replace(".", "", regex=False).astype(int)


def cargar_anio():
    d = pd.read_csv(io.StringIO(leer_texto("anio")), sep=";", skiprows=2, dtype=str)
    d.columns = ["anio", "indicadores", "beneficiarios", "agentes", "total"]
    d = d.drop(columns="indicadores").dropna(subset=["anio"])
    for c in ["beneficiarios", "agentes", "total"]:
        d[c] = _entero(d[c])
    d["anio"] = d["anio"].astype(int)
    d["variacion_%"] = (d["total"].pct_change() * 100).round(1)
    d["agentes_%_del_total"] = (d["agentes"] / d["total"] * 100).round(2)
    return d


def cargar_ugl():
    d = pd.read_csv(io.StringIO(leer_texto("ugl")), sep=";", skiprows=5, dtype=str)
    d.columns = ["ugl_id", "ugl", "indicadores", "beneficiarios", "agentes", "total"]
    d = d.drop(columns="indicadores").dropna(subset=["ugl_id"])
    d = d[d["ugl_id"] != "Total"].copy()           # la última fila es el total del archivo
    for c in ["beneficiarios", "agentes", "total"]:
        d[c] = _entero(d[c])
    d["ugl_id"] = d["ugl_id"].astype(int)
    d["%_del_total"] = (d["total"] / d["total"].sum() * 100).round(2)
    d = d.sort_values("total", ascending=False).reset_index(drop=True)
    d["puesto"] = d.index + 1
    return d


PROVINCIAS = {"BUENOS AIRES", "CABA", "CATAMARCA", "CHACO", "CHUBUT", "CORDOBA", "CORRIENTES", "ENTRE RIOS", "FORMOSA",
              "JUJUY", "LA PAMPA", "LA RIOJA", "MENDOZA", "MISIONES", "NEUQUEN", "RIO NEGRO", "SALTA", "SAN JUAN",
              "SAN LUIS", "SANTA CRUZ", "SANTA FE", "SANTIAGO DEL ESTERO", "TIERRA DEL FUEGO", "TUCUMAN"}
SINONIMOS = {"CAPITAL": "CABA", "CAPITAL FEDERAL": "CABA", "CDAD. BUENOS AIRES": "CABA",
             "CIUDAD AUTONOMA DE BUENOS AIRES": "CABA", "CIUDAD DE BUENOS AIRES": "CABA"}


def normalizar(texto):
    """Mayúsculas, sin tildes ni espacios sobrantes."""
    if pd.isna(texto):
        return pd.NA
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    t = " ".join(t.upper().split())
    return t if t else pd.NA


def cargar_puntos(texto):
    """Lee el listado de puntos de vacunación, lo limpia y devuelve (tabla, resumen de calidad)."""
    p = pd.read_csv(io.StringIO(texto), sep=";", skiprows=3, header=None, dtype=str,
                    names=["id", "nombre", "domicilio", "localidad", "provincia_original"], usecols=[0, 1, 2, 3, 4])
    n_inicial = len(p)
    p = p.dropna(subset=["id"])
    p = p.dropna(subset=["nombre", "domicilio"], how="all")          # filas sin datos (solo el id)
    p["provincia"] = p["provincia_original"].map(normalizar).replace(SINONIMOS)
    p["reconocida"] = p["provincia"].isin(PROVINCIAS)
    # El código de UGL está en el id: 901... = UGL 1, 902... = UGL 2, etc. (solo ids que empiezan con 9)
    p["ugl_id"] = pd.to_numeric(p["id"].where(p["id"].str.startswith("9")).str[1:3], errors="coerce")
    resumen = {"filas leídas": n_inicial, "filas sin datos": n_inicial - len(p), "filas útiles": len(p),
               "provincia no reconocida": int((~p["reconocida"]).sum())}
    return p, resumen


def puntos_por_provincia(puntos):
    return puntos[puntos["reconocida"]]["provincia"].value_counts()


def aplicaciones_por_punto(puntos, ugl):
    por_ugl = (puntos.dropna(subset=["ugl_id"]).assign(ugl_id=lambda d: d["ugl_id"].astype(int))
               .groupby("ugl_id").size().rename("puntos").reset_index())
    rel = ugl.merge(por_ugl, on="ugl_id", how="inner")
    rel["aplicaciones_por_punto"] = (rel["total"] / rel["puntos"]).round(0)
    return rel.sort_values("aplicaciones_por_punto", ascending=False)
