from connection import conectar_bd, cerrar_conexion

class DatabaseManager:
    def __init__(self):
        self.connection, self.cursor = conectar_bd()

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
