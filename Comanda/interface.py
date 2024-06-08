import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="normalizacion",
    user="RodriJul",
    password="1234",
    host="localhost"  
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

