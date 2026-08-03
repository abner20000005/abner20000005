import tkinter as tk
from tkinter import ttk
from controladores.reportes_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"

def abrir_reportes():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Reportes")
    ventana.geometry("1050x620")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    # Header
    tk.Label(ventana, text="REPORTES Y ESTADÍSTICAS", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    # Resumen rápido
    frame_resumen = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_resumen.pack(fill="x", padx=15, pady=10)

    def crear_tarjeta(parent, titulo, valor, col):
        f = tk.Frame(parent, bg=COLOR_VINO, width=200, height=70)
        f.grid(row=0, column=col, padx=10)
        f.pack_propagate(False)
        tk.Label(f, text=titulo, bg=COLOR_VINO, fg="white", font=("Arial", 10)).pack(pady=(8, 0))
        tk.Label(f, text=str(valor), bg=COLOR_VINO, fg="white", font=("Arial", 18, "bold")).pack()

    crear_tarjeta(frame_resumen, "Total Libros", total_libros(), 0)
    crear_tarjeta(frame_resumen, "Total Lectores", total_lectores(), 1)
    crear_tarjeta(frame_resumen, "Préstamos Activos", total_prestamos_activos(), 2)

    # Botones de reportes
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(pady=5)

    def mostrar(titulo, columnas, datos):
        tabla.delete(*tabla.get_children())
        tabla["columns"] = columnas
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=150, anchor="center")
        for fila in datos:
            valores = []
            for v in fila:
                if hasattr(v, "strftime"):
                    valores.append(str(v)[:10])
                else:
                    valores.append(v)
            tabla.insert("", tk.END, values=valores)
        lblTitulo.config(text=titulo)

    tk.Button(frame_botones, text="Libros Disponibles", bg=COLOR_CAFE, fg="white", width=18,
              relief="flat", font=("Arial", 9, "bold"),
              command=lambda: mostrar("Libros Disponibles",
                                      ("Código", "Título", "Ubicación", "Estado"),
                                      libros_disponibles())).pack(side="left", padx=4)

    tk.Button(frame_botones, text="Libros Prestados", bg=COLOR_CAFE, fg="white", width=16,
              relief="flat", font=("Arial", 9, "bold"),
              command=lambda: mostrar("Libros Prestados",
                                      ("Código", "Título", "Lector", "F. Préstamo", "F. Límite"),
                                      libros_prestados())).pack(side="left", padx=4)

    tk.Button(frame_botones, text="Préstamos Atrasados", bg="#A63D40", fg="white", width=18,
              relief="flat", font=("Arial", 9, "bold"),
              command=lambda: mostrar("Préstamos Atrasados",
                                      ("Código", "Título", "Lector", "F. Límite", "Días retraso"),
                                      prestamos_atrasados())).pack(side="left", padx=4)

    tk.Button(frame_botones, text="Multas Pendientes", bg="#A63D40", fg="white", width=16,
              relief="flat", font=("Arial", 9, "bold"),
              command=lambda: mostrar("Multas Pendientes",
                                      ("Lector", "Motivo", "Monto", "Estado"),
                                      multas_pendientes())).pack(side="left", padx=4)

    tk.Button(frame_botones, text="Más Solicitados", bg=COLOR_CAFE, fg="white", width=15,
              relief="flat", font=("Arial", 9, "bold"),
              command=lambda: mostrar("Libros Más Solicitados",
                                      ("Título", "Veces prestado"),
                                      libros_mas_solicitados())).pack(side="left", padx=4)

    lblTitulo = tk.Label(ventana, text="Seleccione un reporte", bg=COLOR_FONDO,
                         font=("Arial", 12, "bold"), fg=COLOR_VINO)
    lblTitulo.pack(pady=8)

    tabla = ttk.Treeview(ventana, show="headings", height=16)
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))