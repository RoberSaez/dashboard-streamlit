# InmoData 360

Dashboard interactivo en Streamlit para el análisis de compraventas por nacionalidades en Alicante.

## Requisitos

- Python 3.8+
- Ver dependencias en `requirements.txt`

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegúrate de tener el archivo de datos Excel en `documentos/FActNOTARIADOnacionalidades.xlsx` y los recursos gráficos (logo y favicon) en la carpeta `documentos`.

## Uso

Ejecuta la aplicación con:

```bash
streamlit run app.py
```

Abre el navegador en la URL que te indique Streamlit (por defecto http://localhost:8501).

## Estructura

- `app.py`: Código principal de la app Streamlit.
- `requirements.txt`: Dependencias del proyecto.
- `documentos/`: Carpeta con el logo, favicon y el archivo Excel de datos.

## Personalización

- Cambia el logo o favicon reemplazando los archivos en la carpeta `documentos`.
- Elige el municipio desde el sidebar para filtrar los datos y gráficos.

## Autor

- BDI - Big Data Inmobiliario
