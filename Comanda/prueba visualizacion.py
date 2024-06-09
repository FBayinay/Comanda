import tkinter as tk
from tkinter import ttk, messagebox
from connection import conectar_bd, cerrar_conexion

# Función para mostrar el contenido de una tabla seleccionada
def mostrar_tabla():
    try:
        # Obtener la tabla seleccionada
        table_name = tablas_listbox.get(tk.ACTIVE)
        if not table_name:
            return
        
        # Limpiar la tabla anterior
        for item in contenido_tree.get_children():
            contenido_tree.delete(item)
        
        # Ejecutar consulta para obtener el contenido de la tabla
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Obtener los nombres de las columnas
        column_names = [desc[0] for desc in cursor.description]
        
        # Establecer encabezados de la tabla
        contenido_tree["columns"] = column_names
        for col in column_names:
            contenido_tree.heading(col, text=col)
            contenido_tree.column(col, width=100)
        
        # Insertar filas en la tabla
        rows = cursor.fetchall()
        for row in rows:
            contenido_tree.insert("", tk.END, values=row)
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Conectar a la base de datos
connection, cursor = conectar_bd()

# Crear la ventana principal
root = tk.Tk()
root.title("Visor de Tablas de la Base de Datos")

# Frame para la lista de tablas
frame_tablas = tk.Frame(root)
frame_tablas.pack(side=tk.LEFT, fill=tk.Y)

# Título para la lista de tablas
tablas_label = tk.Label(frame_tablas, text="Tablas en la base de datos:")
tablas_label.pack(pady=10)

# Listbox para mostrar tablas
tablas_listbox = tk.Listbox(frame_tablas)
tablas_listbox.pack(fill=tk.BOTH, expand=True)

# Obtener la lista de tablas y llenar el Listbox
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
for table in cursor.fetchall():
    tablas_listbox.insert(tk.END, table[0])

# Frame para el contenido de la tabla
frame_contenido = tk.Frame(root)
frame_contenido.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Botón para mostrar el contenido de la tabla seleccionada
mostrar_btn = tk.Button(frame_contenido, text="Mostrar Contenido", command=mostrar_tabla)
mostrar_btn.pack(pady=10)

# Treeview para mostrar el contenido de la tabla
contenido_tree = ttk.Treeview(frame_contenido)
contenido_tree.pack(fill=tk.BOTH, expand=True)

# Cerrar la conexión cuando se cierra la ventana
def on_closing():
    cerrar_conexion(connection, cursor)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la aplicación
root.mainloop()
