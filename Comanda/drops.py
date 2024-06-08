from connection import conectar_bd,cerrar_conexion
from psycopg2 import errors
# Conectar a la base de datos
connection, cursor = conectar_bd()
def eliminar_rol_por_id():
    try:
        id_rol = int(input("Ingrese el id_rol del rol que desea eliminar: "))
    except ValueError:
        print("¡Error! Debe ingresar un número entero.")
        return
    try:
        # Consulta SQL para eliminar un rol por su id_rol
        delete_query = """
        DELETE FROM roles
        WHERE id_rol = %s;
        """
        cursor.execute(delete_query, (id_rol,))
        connection.commit()

        # Verificar si se eliminó realmente un registro
        if cursor.rowcount == 1:
            print(f"Se eliminó el rol con id_rol {id_rol}.")
        else:
            print(f"No se encontró ningún rol con id_rol {id_rol}.")
    except errors.UniqueViolation as e:
        print("Error al eliminar el rol:", e)
eliminar_rol_por_id()
# Cerrar cursor y conexión al finalizar
cerrar_conexion(connection, cursor)