from connection import conectar_bd,cerrar_conexion
# Conectar a la base de datos
connection, cursor = conectar_bd()

# Función para insertar datos en la tabla roles
def insert_into_roles():
    nombre_rol=input("Inserte el rol: ")
    insert_query = """
    INSERT INTO roles (Nombre)
    VALUES (%s)
    RETURNING id_rol;
    """
    cursor.execute(insert_query, (nombre_rol,))
    id_rol = cursor.fetchone()[0]
    connection.commit()
    print(f"Insertado rol '{nombre_rol}' con ID: {id_rol}")

# Llamada a la función para insertar un nuevo rol
insert_into_roles()

# Cerrar cursor y conexión al finalizar
cerrar_conexion(connection, cursor)
#ajdasd