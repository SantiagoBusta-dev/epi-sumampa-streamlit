# EPI Sumampa: de los registros en papel a los datos (app de Streamlit)

Práctica Profesionalizante II · Grupo 2 · ITSE Sede Sumampa

App con 6 pestañas: el proyecto, el dashboard del EPI (datos **ficticios**), las alertas con consulta por DNI,
las vacunas antigripales de PAMI (por año y por UGL), los puntos de vacunación de PAMI y las fuentes.

> Los datos del EPI son ficticios. Los datos de PAMI son de beneficiarios del Instituto, no de niños.

## Archivos
| Archivo | Para qué sirve |
|---|---|
| `app.py` | La interfaz de Streamlit |
| `datos.py` | Carga y limpieza de los datos (sin Streamlit) |
| `graficos.py` | Los gráficos (matplotlib) |
| `requirements.txt` | Librerías necesarias |
| `data/` | CSV del EPI (ficticio) y de PAMI (antigripales por año y por UGL) |

El tercer dataset (puntos de vacunación) se descarga desde la app al apretar el botón.

## Ejecutarla en la computadora
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicarla en Streamlit Community Cloud
1. En https://github.com crear un repositorio **público** (por ejemplo `epi-sumampa-streamlit`) y subir estos archivos: `app.py`, `datos.py`, `graficos.py`, `requirements.txt`, `README.md` y la carpeta `data/`. `app.py` tiene que quedar en la raíz del repositorio.
2. Entrar a https://share.streamlit.io e iniciar sesión (con GitHub, para que vea el repositorio).
3. Elegir **Create app** → **Deploy a public app from GitHub**.
4. Completar: repositorio, rama `main` y archivo principal `app.py`. Apretar **Deploy**.
5. Esperar unos minutos. La app queda en una dirección del tipo `https://<nombre>.streamlit.app`.

## Fuentes (licencia Creative Commons Attribution 4.0)
- Campaña de vacunación antigripal: https://datos.pami.org.ar/dataset/campana-vacunacion
- Puntos de vacunación: https://datos.pami.org.ar/dataset/puntos-de-vacunacion
- Los mismos en Datos Argentina: https://datos.gob.ar/dataset/campana-vacunacion y https://datos.gob.ar/dataset/puntos-de-vacunacion
