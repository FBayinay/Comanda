FROM python:3.12.5-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo del contenedor
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de tu aplicación al directorio de trabajo del contenedor
COPY . .

# Expone el puerto que la aplicación usará
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
