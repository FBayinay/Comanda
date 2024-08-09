print("MacroV6")
print("By:BF")
import pyautogui
import random
import time
import os
import sys
import keyboard
import threading

screen_width, screen_height = pyautogui.size()

EXCLUSION_TOP = 72
EXCLUSION_BOTTOM = 280
EXCLUSION_RIGHT = 100

stop_thread = False
iterations = 0
max_iterations = 3

tiempo_aleatorio = random.uniform(3, 3.5)
tiempo2 = random.uniform(0.8, 1.2)

def find_image(images):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    for img in images:
        full_img_path = os.path.join(base_path, img)
        print(f"Buscando imagen: {full_img_path}")  # Depuración
        try:
            location = pyautogui.locateOnScreen(full_img_path, confidence=0.7, region=(0, EXCLUSION_TOP, screen_width - EXCLUSION_RIGHT, screen_height - EXCLUSION_BOTTOM))
            if location:
                print(f"Imagen encontrada: {full_img_path} en {location}")  # Depuración
                return location
        except pyautogui.ImageNotFoundException:
            print(f"Imagen no encontrada: {full_img_path}")  # Depuración
            continue
    return None



def move_to_image_and_execute(images, palabra, index, repetitions):
    if stop_thread:
        return

    img_location = find_image(images)
    if img_location:
        center_x, center_y = pyautogui.center(img_location)

        if img_location.left < (screen_width * (1/4 + 0.5/4)):
            offset_x = 30
        else:
            offset_x = -100

        if repetitions == 1:
            offset_x += 30
            offset_y = -5
        else:
            offset_y = 0

        pyautogui.moveTo(center_x + offset_x, center_y + offset_y, duration=0.5)
        time.sleep(tiempo2)
        for _ in range(repetitions):
            if stop_thread:
                return
            pyautogui.click(clicks=3)
            time.sleep(tiempo2)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(tiempo2)
            pyautogui.write(palabra[index])
            pyautogui.press('enter')
            time.sleep(tiempo_aleatorio)

def close_inspect_window():
    # Coordenadas aproximadas de la "X" en la esquina superior derecha
    coord_x = screen_width - 120
    coord_y = 10
    pyautogui.moveTo(coord_x, coord_y, duration=0.5)
    pyautogui.click()

def macro_thread(palabras, palabras2):
    global iterations
    images = ["image1.png", "image2.png", "image3.png"]

    while iterations < max_iterations and not stop_thread:
        for i in range(30):
            if stop_thread:
                break
            move_to_image_and_execute(images, palabras, i, 1)

        if stop_thread:
            break

        pyautogui.hotkey('ctrl', 'shift', 'i')
        time.sleep(tiempo_aleatorio)

        if stop_thread:
            break

        # Cerrar la ventana de inspección
        close_inspect_window()

        # Esperar 5 segundos antes de la siguiente iteración
        time.sleep(5)
        iterations += 1

    if stop_thread:
        close_inspect_window()

    print("Se han completado las iteraciones o se ha detenido la macro.")

def main():
    global stop_thread
    print("Esperando que presiones 'Supr' para comenzar...")
    t = None

    while True:
        if keyboard.is_pressed('delete'):
            stop_thread = False
            if not t or not t.is_alive():
                t = threading.Thread(target=macro_thread, args=(palabras, palabras2))
                t.start()
        elif keyboard.is_pressed('e'):
            print("Deteniendo macro...")
            stop_thread = True
            if t and t.is_alive():
                t.join()
            break

        time.sleep(random.uniform(0.09, 0.15))

palabras = [
    "auto", "auto fiat", "vestido", "vestido elegante", "camion", "camion mercedes",
    "inteligencia", "inteligencia artificial", "animal", "animal domestico",
    "perro", "perro labrador", "flor", "flor silvestre", "arbol", "arbol frutal",
    "pais", "pais europeo", "ciudad", "ciudad capital", "fideo", "fideo seco",
    "libro", "libro de ciencia ficcion", "comida", "comida italiana", "color", "color primario",
    "camino", "camino rocoso"
]
palabras2 = ["ropa", "ropa deportiva", "fruta", "fruta tropical",
    "bebida", "bebida energetica", "actor", "actor de comedia", "actriz", "actriz ganadora del Oscar",
    "pelicula", "pelicula de aventuras", "planta", "planta de interior", "poeta", "poeta contemporaneo",
    "heroe", "heroe de acción", "vestido", "vestido elegante"
]

if __name__ == '__main__':
    main()
