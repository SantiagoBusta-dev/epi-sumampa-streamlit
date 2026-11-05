# EPI Sumampa: de los cuadernos a los datos

**Práctica Profesionalizante II · Grupo 2 · ITSE · Sede Sumampa**

Aplicación multipágina desarrollada con Streamlit. Presenta el circuito propuesto para ordenar registros del EPI, explorar datos ficticios de demostración y analizar conjuntos de datos abiertos de PAMI de manera separada.

## Secciones
- **Inicio:** presentación del proyecto y resumen.
- **Panel del EPI:** indicadores, filtros, gráficos de asistencia, vacunación, características e insumos.
- **Alertas y seguimiento:** alertas de demostración sin mostrar DNI ni nombres.
- **Análisis PAMI:** vacunación antigripal por año y por UGL.
- **Puntos de vacunación:** carga y exploración del conjunto territorial.
- **Metodología y privacidad:** circuito de datos, formularios, roles y criterios de acceso.

## Importante sobre los datos
Los datos del EPI incluidos en el repositorio son ficticios y se utilizan únicamente para probar la aplicación. No subir datos reales de niños, familias, DNI, teléfonos, domicilios ni información de salud. Los datos de PAMI corresponden a beneficiarios del Instituto y no a niños del EPI.

Los formularios se comparten por canales internos con el personal autorizado. La planilla central no debe publicarse ni dejarse con acceso abierto. La distribución interna de un enlace no equivale a una restricción técnica de identidad.

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
│   └── 06_metodologia.py
└── data/
    └── archivos CSV de demostración y datos abiertos
```

## Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en Streamlit Community Cloud
1. Subir o actualizar los archivos del proyecto en GitHub.
2. En Streamlit Community Cloud, crear una aplicación nueva o abrir la existente.
3. Seleccionar el repositorio, la rama `main` y el archivo principal `app.py`.
4. Presionar **Deploy** o **Reboot app** si corresponde.
5. Cuando se actualice la rama configurada, Streamlit detectará el cambio y reconstruirá la aplicación.

## Fuentes
- PAMI, campaña de vacunación antigripal: https://datos.pami.org.ar/dataset/campana-vacunacion
- PAMI, puntos de vacunación: https://datos.pami.org.ar/dataset/puntos-de-vacunacion
- Datos Argentina: https://datos.gob.ar/
