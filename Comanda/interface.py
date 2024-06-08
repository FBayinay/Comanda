import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    host="192.168.18.37",
    database="comanda",
    user="fbayinay",
    password="159753"
    )


# Crear un cursor
cur = conn.cursor()

# Obtener la lista de tablas
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

# Recorrer las tablas y mostrarlas
print("Tablas en la base de datos:")
for table in cur.fetchall():
    print(table[0])

# Cerrar cursor y conexión
cur.close()
conn.close()

