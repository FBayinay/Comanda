from connection import conectar_bd, cerrar_conexion

connection, cursor = conectar_bd()
# Obtener la lista de tablas
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

# Recorrer las tablas y mostrarlas
print("Tablas en la base de datos:")
for table in cursor.fetchall():
    print(table[0])

cerrar_conexion(connection, cursor)