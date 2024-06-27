# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Define la variable de entorno para Flask
ENV FLASK_APP=app.py

# Expone el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para correr la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
