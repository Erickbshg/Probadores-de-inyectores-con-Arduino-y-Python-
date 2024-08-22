import tkinter as tk
import serial
import time
from tkinter import messagebox

# Configurar la conexión con Arduino
puerto = 'COM3'  # Cambia esto según tu configuración
baudrate = 9600
arduino = serial.Serial(puerto, baudrate, timeout=1)
time.sleep(2)  # Tiempo para que la conexión se establezca

def enviar_orden():
    try:
        # Leer los valores ingresados y convertirlos a enteros
        orden = [int(entry1.get()), int(entry2.get()), int(entry3.get()), int(entry4.get())]

        # Filtrar los valores para mantener solo los inyectores válidos (entre 1 y 4)
        orden = [num for num in orden if 1 <= num <= 4]

        if len(orden) == 0:
            raise ValueError  # Si no hay inyectores válidos, lanzar un error

        # Convertir de 1-4 a 0-3 para que el Arduino entienda
        orden = [num - 1 for num in orden]
        comando = 'o ' + ' '.join(map(str, orden)) + '\n'
        arduino.write(comando.encode())
        output_label.config(text=f"Orden enviada: {orden}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos entre 1 y 4 para el orden de los inyectores.")

def enviar_velocidad():
    try:
        velocidad = int(velocidad_entry.get())
        comando = f'v {velocidad}\n'
        arduino.write(comando.encode())
        output_label.config(text=f"Velocidad enviada: {velocidad} ms")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido para la velocidad.")

def toggle_fullscreen(event=None):
    """ Alterna entre pantalla completa y ventana. """
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    root.bind('<F11>', toggle_fullscreen)
    root.bind('<Escape>', end_fullscreen)

def end_fullscreen(event=None):
    """ Termina el modo pantalla completa. """
    root.attributes('-fullscreen', False)
    root.bind('<F11>', toggle_fullscreen)

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Inyectores")

# Hacer la ventana en pantalla completa
root.attributes('-fullscreen', True)
root.configure(bg='black')

# Cambiar el color de las etiquetas, campos de entrada y botones
style = {'bg': 'black', 'fg': 'white', 'font': ('Arial', 18)}

# Añadir título con letras ASCII
titulo_ascii = r"""
  ___                            _                      
 |_ _|  _ _    _  _   ___   __  | |_   ___   _ _   __ _ 
  | |  | ' \  | || | / -_) / _| |  _| / _ \ | '_| / _` |
 |___| |_||_|  \_, | \___| \__|  \__| \___/ |_|   \__,_|
               |__/                                     
"""

# Crear un label para el título con fuente 'Courier'
titulo_label = tk.Label(root, text=titulo_ascii, bg='black', fg='white', font=('Courier', 18, 'bold'))
titulo_label.pack(pady=20)

# Crear un frame para contener las entradas y botones
main_frame = tk.Frame(root, bg='black')
main_frame.pack(expand=True, padx=20, pady=20)

# Crear etiquetas y campos de entrada para el orden de los inyectores
tk.Label(main_frame, text="Orden de Inyectores (1-4):", **style).pack(pady=10)

entry1 = tk.Entry(main_frame, **style)
entry1.pack(pady=5)
entry2 = tk.Entry(main_frame, **style)
entry2.pack(pady=5)
entry3 = tk.Entry(main_frame, **style)
entry3.pack(pady=5)
entry4 = tk.Entry(main_frame, **style)
entry4.pack(pady=5)

tk.Button(main_frame, text="Enviar Orden", command=enviar_orden, **style).pack(pady=20)

# Crear etiqueta y campo de entrada para la velocidad
tk.Label(main_frame, text="Velocidad (ms):", **style).pack(pady=10)
velocidad_entry = tk.Entry(main_frame, **style)
velocidad_entry.pack(pady=5)

tk.Button(main_frame, text="Enviar Velocidad", command=enviar_velocidad, **style).pack(pady=20)

# Etiqueta para mostrar mensajes de salida
output_label = tk.Label(main_frame, text="", **style)
output_label.pack(pady=20)

# Agregar un botón para salir de la pantalla completa
exit_button = tk.Button(main_frame, text="Salir", command=root.quit, **style)
exit_button.pack(pady=20)

# Asociar las teclas de pantalla completa
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Iniciar la interfaz gráfica
root.mainloop()
