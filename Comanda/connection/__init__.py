# comanda/connection/__init__.py
from .database_manager import DatabaseManager  # si esto es necesario
from .connection import conectar_bd, cerrar_conexion  # Ajusta el nombre del módulo donde están definidos

__all__ = ['DatabaseManager', 'conectar_bd', 'cerrar_conexion']