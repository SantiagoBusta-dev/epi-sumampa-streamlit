# EPI Sumampa: de los cuadernos a los datos

**Práctica Profesionalizante II · Grupo 2 · ITSE · Sede Sumampa**

Aplicación multipágina desarrollada con Streamlit. Presenta el circuito propuesto para ordenar registros del EPI, explorar datos ficticios de demostración y analizar conjuntos de datos abiertos de PAMI de manera separada.

## Secciones
- **Inicio:** presentación del proyecto y resumen.
- **Panel del EPI:** indicadores, filtros y gráficos de demostración.
- **Alertas y seguimiento:** alertas ilustrativas sin mostrar datos personales.
- **Análisis PAMI:** vacunación antigripal por año y por UGL.
- **Puntos de vacunación:** carga y exploración del conjunto territorial.
- **Metodología y privacidad:** circuito de datos, formularios, roles y criterios de acceso.
- **EDA ampliado:** exploración de las siete tablas del archivo `data/epi_sumampa.csv`, con distribuciones, estadísticas descriptivas, cruces y controles básicos de calidad.

## Importante sobre los datos
Los datos del EPI incluidos en el repositorio son ficticios y se utilizan únicamente para probar la aplicación. Los resultados del EDA no describen la situación real del EPI ni deben utilizarse para tomar decisiones sobre niños o familias. No subir datos reales de niños, familias, DNI, teléfonos, domicilios ni información de salud.

El conjunto PAMI corresponde a información pública de beneficiarios del Instituto y se presenta en una sección independiente; no debe mezclarse con los datos ficticios del EPI.

Los formularios se comparten por canales internos con el personal autorizado. La planilla central no debe publicarse ni dejarse con acceso abierto. Compartir un enlace internamente no equivale a restringir técnicamente quién puede acceder.

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

## Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en Streamlit Community Cloud
1. Subir o actualizar los archivos del proyecto en GitHub.
2. En Streamlit Community Cloud, abrir la aplicación existente.
3. Comprobar que el repositorio, la rama y `app.py` sean los correctos.
4. Guardar los cambios y esperar la reconstrucción de la aplicación.

## Fuentes
- PAMI, campaña de vacunación antigripal: https://datos.pami.org.ar/dataset/campana-vacunacion
- PAMI, puntos de vacunación: https://datos.pami.org.ar/dataset/puntos-de-vacunacion
- Datos Argentina: https://datos.gob.ar/
