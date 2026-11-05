"""Funciones gráficas reutilizables para la aplicación."""
import matplotlib.pyplot as plt
import pandas as pd

VERDE = "#286b58"
NARANJA = "#d98c3f"

def grafico_barras(serie, titulo, xlabel="", ylabel="Cantidad", horizontal=False):
    if serie is None or len(serie) == 0:
        return None
    fig, ax = plt.subplots(figsize=(8, 4))
    if horizontal:
        serie.sort_values().plot(kind="barh", ax=ax, color=VERDE)
    else:
        serie.plot(kind="bar", ax=ax, color=VERDE, rot=30)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig

def grafico_torta(serie, titulo):
    if serie is None or len(serie) == 0:
        return None
    fig, ax = plt.subplots(figsize=(6, 4))
    serie.plot(kind="pie", autopct="%1.1f%%", ax=ax, ylabel="")
    ax.set_title(titulo)
    fig.tight_layout()
    return fig
