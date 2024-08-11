import os
from dotenv import load_dotenv

# Usa la ruta absoluta al archivo .env
dotenv_path = 'D:/Users/Federico/Desktop/UTN/3_año/Desarrollo de software/Comanda/GitHub/Proyecto/Restaurante/docker/.env'
print(f"Loading .env file from: {dotenv_path}")
load_dotenv(dotenv_path)
print(f"FLASK_CONTEXT: {os.getenv('FLASK_CONTEXT')}")
