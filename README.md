# EPI Sumampa — De los cuadernos a los datos

**Práctica Profesionalizante II · Grupo 2 · ITSE · Sede Sumampa**

Aplicación multipágina en Streamlit para explorar un conjunto de datos ficticios del EPI y, en una sección separada, conjuntos de datos abiertos de PAMI.

## Cambios de esta versión
- Se utiliza un único archivo `data/epi_sumampa.csv` como fuente de datos del EPI.
- El archivo reúne siete tablas: `alumnos`, `tutores`, `docentes`, `asistencia`, `alumno_tutor`, `insumos` y `pedidos`.
- Se reemplazó la dependencia de los antiguos CSV separados de alumnos, asistencia, insumos, pedidos y alertas.
- El panel integral incluye filtros, indicadores, gráficos, cruces entre tablas, tablas completas y descarga CSV.
- Las alertas se generan a partir del nuevo conjunto ficticio.
- El EDA permite revisar calidad, distribuciones, estadísticas, correlaciones y registros completos.
- PAMI se conserva como análisis independiente.

## Estructura
```text
.
├── app.py
├── datos.py
├── graficos.py
├── requirements.txt
├── README.md
├── pages/
│   ├── 01_inicio.py
│   ├── 02_epi.py
│   ├── 03_alertas.py
│   ├── 04_pami.py
│   ├── 05_puntos.py
│   ├── 06_metodologia.py
│   └── 07_eda.py
└── data/
    └── epi_sumampa.csv
```

## 🌐 Aplicación en línea

Podés acceder a la aplicación desde el siguiente enlace:

👉 **[Abrir EPI Sumampa en Streamlit](https://epi-sumampa-app-hsgmgtbwb4dnouaj3sx7sq.streamlit.app/)**

```

## Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Actualizar el repositorio existente
1. Hacé una copia de seguridad del repositorio antes de cambiarlo.
2. Reemplazá `app.py`, `datos.py`, `graficos.py` y `requirements.txt` por los de esta versión.
3. Reemplazá las páginas `01_inicio.py` a `06_metodologia.py` y agregá `07_eda.py`.
4. En `data/`, conservá solamente `epi_sumampa.csv` como archivo de datos del EPI.
5. Eliminá los CSV anteriores del EPI: `alumnos.csv`, `asistencia.csv`, `insumos.csv`, `pedidos.csv` y `reporte_alertas.csv`.
6. Conservá los archivos de datos PAMI si ya están descargados; no son parte del conjunto EPI.
7. Guardá los cambios y verificá la aplicación en Streamlit Community Cloud.

## Datos y alcance
El archivo `epi_sumampa.csv` contiene datos ficticios para una práctica académica. La aplicación muestra todos los campos del archivo para demostrar su exploración y visualización. No reemplazarlo por datos reales de niños, familias o personal sin autorización institucional y medidas adecuadas de protección.

Los datos abiertos de PAMI se muestran en páginas independientes y no se mezclan con los datos ficticios del EPI.

## Fuentes PAMI
- https://datos.pami.org.ar/dataset/campana-vacunacion
- https://datos.pami.org.ar/dataset/puntos-de-vacunacion
