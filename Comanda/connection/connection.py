# comanda/connection/connection.py
import psycopg2

def conectar_bd():
    connection = psycopg2.connect(
        host="192.168.43.42",
        database="comanda",
        user="fbayinay",
        password="159753"
    )
    cursor = connection.cursor()
    return connection, cursor

def cerrar_conexion(connection, cursor):
    cursor.close()
    connection.close()