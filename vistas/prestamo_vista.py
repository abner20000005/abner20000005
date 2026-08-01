"""
- Interfaz interactiva para seleccionar un lector y un ejemplar disponible.
- Muestra las fechas automáticas de préstamo y fecha límite de devolución.
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

COLOR_FONDO = "#EDE6DD"
COLOR_HEADER = "#7B1E3A"
COLOR_BOTON_GUARDAR = "#6E4B3A"
COLOR_BOTON_MODIFICAR = "#8A5A44"
COLOR_BOTON_ELIMINAR = "#A63A3A"
COLOR_BOTON_LIMPIAR = "#C9B79C"

lectores = ["Juan Pérez", "María López", "Carlos Díaz"]
ejemplares = ["Libro A", "Libro B", "Libro C"]

def generar_fechas():
    hoy = datetime.now()
    fecha_prestamo.set(hoy.strftime("%d/%m/%Y"))
    fecha_devolucion.set((hoy + timedelta(days=7)).strftime("%d/%m/%Y"))


ventana = tk.Tk()
ventana.title("Biblioteca 360 - Préstamos")
ventana.geometry("600x400")
ventana.configure(bg=COLOR_FONDO)


header = tk.Label(ventana, text="GESTIÓN DE PRÉSTAMOS",
                  bg=COLOR_HEADER, fg="white",
                  font=("Arial", 16, "bold"),
                  pady=10)
header.pack(fill="x")


frame = tk.Frame(ventana, bg=COLOR_FONDO)
frame.pack(pady=20)

# Variables
lector_var = tk.StringVar()
ejemplar_var = tk.StringVar()
fecha_prestamo = tk.StringVar()
fecha_devolucion = tk.StringVar()


def lbl(texto, fila):
    tk.Label(frame, text=texto, bg=COLOR_FONDO, font=("Arial", 10)).grid(row=fila, column=0, sticky="w", pady=5)

lbl("Lector:", 0)
lbl("Ejemplar:", 1)
lbl("Fecha préstamo:", 2)
lbl("Fecha devolución:", 3)

style = ttk.Style()
style.theme_use("default")


combo_lector = ttk.Combobox(frame, textvariable=lector_var, values=lectores, width=30)
combo_lector.grid(row=0, column=1, pady=5)

combo_ejemplar = ttk.Combobox(frame, textvariable=ejemplar_var, values=ejemplares, width=30)
combo_ejemplar.grid(row=1, column=1, pady=5)

entry_prestamo = tk.Entry(frame, textvariable=fecha_prestamo, state="readonly", width=33)
entry_prestamo.grid(row=2, column=1, pady=5)

entry_devolucion = tk.Entry(frame, textvariable=fecha_devolucion, state="readonly", width=33)
entry_devolucion.grid(row=3, column=1, pady=5)

frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
frame_botones.pack(pady=20)

tk.Button(frame_botones, text="Generar Fechas",
          bg=COLOR_BOTON_MODIFICAR, fg="white",
          width=15, command=generar_fechas).grid(row=0, column=0, padx=5)

tk.Button(frame_botones, text="Guardar",
          bg=COLOR_BOTON_GUARDAR, fg="white",
          width=15).grid(row=0, column=1, padx=5)

tk.Button(frame_botones, text="Eliminar",
          bg=COLOR_BOTON_ELIMINAR, fg="white",
          width=15).grid(row=0, column=2, padx=5)

tk.Button(frame_botones, text="Limpiar",
          bg=COLOR_BOTON_LIMPIAR,
          width=15).grid(row=0, column=3, padx=5)

ventana.mainloop()