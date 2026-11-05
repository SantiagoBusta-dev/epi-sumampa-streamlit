"""Gráficos (matplotlib) de la app. Cada función devuelve una figura, o None si no hay datos."""
import matplotlib.pyplot as plt
import pandas as pd

COLOR, NARANJA = "#3b6ea5", "#d98c3f"


def _ejes(figsize=(6, 3.4)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig, ax


def _etiquetar(ax):
    for b in ax.patches:
        if b.get_height() > 0:
            ax.annotate(int(b.get_height()), (b.get_x() + b.get_width() / 2, b.get_height()),
                        ha="center", va="bottom", fontsize=9)


# ------------------------------------------------------------------ EPI
def barrios(alumnos):
    if alumnos.empty:
        return None
    s = alumnos["barrio"].value_counts().reindex(["Centro", "Norte", "Sur"], fill_value=0)
    fig, ax = _ejes()
    s.plot.bar(ax=ax, color=COLOR, rot=0)
    _etiquetar(ax)
    ax.set_title("Alumnos por barrio"); ax.set_xlabel(""); ax.set_ylabel("Cantidad")
    fig.tight_layout()
    return fig


def edad_turno(alumnos):
    if alumnos.empty:
        return None
    t = pd.crosstab(alumnos["edad"], alumnos["turno"]).reindex(columns=["Mañana", "Tarde"], fill_value=0)
    fig, ax = _ejes()
    t.plot.bar(ax=ax, stacked=True, color={"Mañana": COLOR, "Tarde": NARANJA}, rot=0)
    ax.set_title("Alumnos por edad y turno"); ax.set_xlabel("Edad (años)"); ax.set_ylabel("Cantidad")
    fig.tight_layout()
    return fig


def vacunacion_barrio(alumnos):
    if alumnos.empty:
        return None
    t = (pd.crosstab(alumnos["barrio"], alumnos["vacunas_completas"])
         .reindex(index=["Centro", "Norte", "Sur"], columns=["Si", "No"], fill_value=0))
    fig, ax = _ejes()
    t.plot.bar(ax=ax, stacked=True, color={"Si": COLOR, "No": NARANJA}, rot=0)
    ax.set_title("Vacunas completas por barrio"); ax.set_xlabel(""); ax.set_ylabel("Alumnos")
    ax.legend(title="Completas")
    fig.tight_layout()
    return fig


def seguro(alumnos):
    if alumnos.empty:
        return None
    s = alumnos["seguro"].value_counts()
    fig, ax = _ejes()
    s.plot.bar(ax=ax, color=COLOR, rot=0)
    _etiquetar(ax)
    ax.set_title("Seguro del alumno"); ax.set_xlabel(""); ax.set_ylabel("Alumnos")
    fig.tight_layout()
    return fig


def asistencia_dia(asis_alumnos):
    if asis_alumnos.empty:
        return None
    d = asis_alumnos.assign(dia=asis_alumnos["fecha"].dt.strftime("%a %d/%m"))
    t = (d.groupby(["fecha", "dia", "asistio_bool"]).size().unstack(fill_value=0)
         .reindex(columns=[True, False], fill_value=0).reset_index().set_index("dia").drop(columns="fecha"))
    t.columns = ["Presente", "Ausente"]
    fig, ax = _ejes()
    t.plot.bar(ax=ax, stacked=True, color={"Presente": COLOR, "Ausente": NARANJA}, rot=0)
    ax.set_title("Asistencia de alumnos por día"); ax.set_xlabel(""); ax.set_ylabel("Alumnos")
    fig.tight_layout()
    return fig


def ausencias(asis_alumnos):
    if asis_alumnos.empty:
        return None
    a = (asis_alumnos[~asis_alumnos["asistio_bool"]].groupby("id_persona").size()
         .reindex(asis_alumnos["id_persona"].unique(), fill_value=0).sort_values(ascending=False))
    fig, ax = _ejes((7, 3.4))
    ax.bar(a.index.astype(str), a.values, color=[NARANJA if v >= 2 else COLOR for v in a.values])
    _etiquetar(ax)
    ax.set_title("Ausencias por alumno (naranja: 2 o más)"); ax.set_xlabel("id del alumno"); ax.set_ylabel("Ausencias")
    fig.tight_layout()
    return fig


def stock(insumos):
    if insumos.empty:
        return None
    pct = (insumos["stock_actual"] / insumos["stock_minimo"] * 100).round(0)
    fig, ax = _ejes()
    ax.bar(insumos["nombre"], pct, color=[NARANJA if v < 100 else COLOR for v in pct])
    ax.axhline(100, color="gray", linestyle="--", linewidth=1)
    ax.set_title("Stock actual como % del mínimo"); ax.set_ylabel("% del mínimo")
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ PAMI
def anio(d):
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.6))
    mx, mn = d["total"].idxmax(), d["total"].idxmin()
    axs[0].bar(d["anio"].astype(str), d["total"] / 1000,
               color=[NARANJA if i in (mx, mn) else COLOR for i in d.index])
    axs[0].set_title("Vacunas antigripales aplicadas por año (miles)"); axs[0].set_ylabel("Miles")
    v = d.dropna(subset=["variacion_%"])
    axs[1].bar(v["anio"].astype(str), v["variacion_%"], color=[COLOR if x >= 0 else NARANJA for x in v["variacion_%"]])
    axs[1].axhline(0, color="gray", linewidth=0.8)
    axs[1].set_title("Variación respecto del año anterior (%)"); axs[1].set_ylabel("%")
    for ax in axs:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def ugl(d, destacado="SANTIAGO DEL ESTERO"):
    fig, ax = _ejes((11, 4))
    ax.bar(d["ugl"].str.title(), d["total"] / 1000, color=[NARANJA if u == destacado else COLOR for u in d["ugl"]])
    ax.set_title("Vacunas antigripales por UGL en 2019 (miles) — Santiago del Estero en naranja")
    ax.set_ylabel("Miles"); ax.tick_params(axis="x", rotation=90, labelsize=8)
    fig.tight_layout()
    return fig


def puntos_provincia(por_prov, destacado="SANTIAGO DEL ESTERO"):
    if por_prov.empty:
        return None
    top = por_prov.head(12)
    fig, ax = _ejes((9, 4))
    ax.bar(top.index.str.title(), top.values, color=[NARANJA if i == destacado else COLOR for i in top.index])
    ax.set_title("Puntos de vacunación de PAMI por provincia (12 con más puntos)"); ax.set_ylabel("Puntos")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    return fig
