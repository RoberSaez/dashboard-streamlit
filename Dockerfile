# Imagen base de Python
FROM python:3.10-slim

# Crear el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8501 (Streamlit usa este puerto)
EXPOSE 8501

# Indicar a Streamlit que escuche en 0.0.0.0
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando para ejecutar Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
