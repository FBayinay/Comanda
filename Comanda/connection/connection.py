import psycopg2

def conectar_bd():
    connection = psycopg2.connect(
        host="10.147.17.37",
        database="comanda",
        user="fbayinay",
        password="159753"
    )
    cursor = connection.cursor()
    return connection, cursor

def cerrar_conexion(connection, cursor):
    cursor.close()
    connection.close()