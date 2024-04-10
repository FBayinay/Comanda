import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv

class Mesa:
    def __init__(self, numero):
        self.numero = numero
        self.ocupada = False
        self.consumo = []

class Restaurante:
    def __init__(self, num_mesas):
        self.mesas = [Mesa(i) for i in range(1, num_mesas + 1)]

restaurante = Restaurante(12)  # Cambia 20 por la cantidad de mesas que deseas tener
ventanas_consumo = {}  # Diccionario para almacenar las ventanas de consumo

def guardar_factura(numero_mesa, lista_consumos):
    ahora = datetime.now()
    fecha_hora = ahora.strftime("%d_%m_%Y--Hora_%H-%M-%S")
    nombre_archivo = f"chofo_{fecha_hora}.csv"

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Restaurante Chofo", fecha_hora, ""])
        writer.writerow(["Insumo", "Valor"])
        for item, valor in lista_consumos:
            writer.writerow([item, str(valor)])
        writer.writerow(["Total", str(sum([valor for _, valor in lista_consumos]))])  # Agregar línea de total

    messagebox.showinfo("Factura Guardada", f"Factura guardada como {nombre_archivo}")

def mostrar_ventana_consumo(numero_mesa):
    root.iconify()  # Oculta la ventana principal

    if numero_mesa in ventanas_consumo and ventanas_consumo[numero_mesa].winfo_exists():
        ventanas_consumo[numero_mesa].deiconify()  # Mostrar la ventana existente
    else:
        ventana_consumo = tk.Toplevel(root)
        ventana_consumo.geometry("400x400")  # Cambiar el tamaño a la ventana Agregar insumo
        ventana_consumo.title(f"Mesa {numero_mesa}")

        lista_consumos = []

        def agregar_consumo():
            item = entry_consumo.get()
            valor = entry_valor.get()
            if item and valor:
                lista_consumos.append((item, float(valor)))
                actualizar_lista_consumos()
                entry_consumo.delete(0, tk.END)
                entry_valor.delete(0, tk.END)

        def actualizar_lista_consumos():
            for widget in frame_consumos.winfo_children():
                widget.destroy()

            for i, (item, valor) in enumerate(lista_consumos):
                tk.Label(frame_consumos, text=item).grid(row=i, column=0, padx=100, pady=5)
                tk.Label(frame_consumos, text=str(valor)).grid(row=i, column=1, padx=10, pady=5)

        entry_consumo = tk.Entry(ventana_consumo)
        entry_consumo.grid(row=1, column=0, padx=10, pady=10)
        entry_valor = tk.Entry(ventana_consumo)
        entry_valor.grid(row=1, column=1, padx=10, pady=10)

        boton_agregar = tk.Button(ventana_consumo, text="Agregar", command=agregar_consumo)
        boton_agregar.grid(row=2, column=0, columnspan=2, pady=10)

        frame_consumos = tk.Frame(ventana_consumo)
        frame_consumos.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        def calcular_total():
            total = sum([valor for _, valor in lista_consumos])
            guardar_factura(numero_mesa, lista_consumos)
            messagebox.showinfo("Total a Pagar", f"Total a pagar en la mesa {numero_mesa}: {total}")
            restaurante.mesas[numero_mesa - 1].ocupada = False
            ventana_consumo.destroy()
            actualizar_interfaz()
            root.deiconify()  # Muestra la ventana principal nuevamente

        boton_cobrar = tk.Button(ventana_consumo, text="Cobrar", command=calcular_total)
        boton_cobrar.grid(row=90, column=0, columnspan=2, pady=10)

        # Manejar el evento de cierre de la ventana
        ventana_consumo.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_consumo(numero_mesa, ventana_consumo))

        ventanas_consumo[numero_mesa] = ventana_consumo  # Almacena la ventana en el diccionario

    # Verifica si la mesa está ocupada y tiene consumos previos, en cuyo caso los muestra
    mesa = restaurante.mesas[numero_mesa - 1]
    if mesa.ocupada and mesa.consumo:
        lista_consumos = mesa.consumo
        actualizar_lista_consumos()

def cerrar_ventana_consumo(numero_mesa, ventana_consumo):
    ventana_consumo.destroy()
    del ventanas_consumo[numero_mesa]
    root.deiconify()  # Muestra la ventana principal nuevamente

def actualizar_interfaz():
    for mesa in restaurante.mesas:
        color = "green" if mesa.ocupada else "gray"
        botones[mesa.numero - 1].config(bg=color)

def on_mesa_click(numero_mesa):
    mesa = restaurante.mesas[numero_mesa - 1]
    if mesa.ocupada:
        mostrar_ventana_consumo(mesa.numero)
    else:
        mesa.ocupada = True
        actualizar_interfaz()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Administrador de Mesas")

botones = []
for mesa in restaurante.mesas:
    boton = tk.Button(root, text=f"Mesa {mesa.numero}", width=20, height=6, command=lambda m=mesa.numero: on_mesa_click(m))
    boton.grid(row=(mesa.numero - 1) // 4, column=(mesa.numero - 1) % 4, padx=10, pady=10)
    botones.append(boton)

actualizar_interfaz()

root.mainloop()
