# database_manager.py
import psycopg2
from comanda.connection.connection import conectar_bd, cerrar_conexion

class DatabaseManager:
    def __init__(self):
        self.connection, self.cursor = conectar_bd()

    def insert_data(self, table_name, data):
        try:
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            values = tuple(data.values())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Datos insertados correctamente en la tabla", table_name)
        except (Exception, psycopg2.Error) as error:
            print("Error al insertar datos:", error)
            raise  # Propagar la excepción para manejarla en un nivel superior
    def get_table_names(self):
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        return [table[0] for table in self.cursor.fetchall()]

    def get_table_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        column_names = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        return column_names, rows

    def get_column_names(self, table_name):
        self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        return [row[0] for row in self.cursor.fetchall()]

    def close_connection(self):
        cerrar_conexion(self.connection, self.cursor)

    def get_table_info(self, table_name):
        # Devuelve tanto los nombres de las columnas como las filas de la tabla
        self.cursor.execute(f"SELECT * FROM {table_name}")
        column_names = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        return column_names, rows
