import tkinter as tk
from tkinter import messagebox
from vistas.autores_vista import abrir_autores
from vistas.devoluciones_vista import abrir_devoluciones
from vistas.editoriales_categorias_vista import abrir_editoriales_categorias
from vistas.ejemplares_vista import abrir_ejemplares
from vistas.lectores_vista import abrir_lectores
from vistas.libros_vista import abrir_libros
from vistas.prestamos_vista import abrir_prestamos
from vistas.reportes_vista import abrir_reportes
from vistas.reservas_vista import abrir_reservas
from vistas.sanciones_vista import abrir_sanciones
from vistas.usuarios_vista import abrir_usuarios

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"

def abrir_menu(usuario):
    ventana = tk.Tk()
    ventana.title("Biblioteca 360 - Menú Principal")
    ventana.geometry("900x550")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    # Header
    header = tk.Frame(ventana, bg=COLOR_VINO, height=70)
    header.pack(fill="x")
    tk.Label(header, text="BIBLIOTECA 360", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold")).pack(side="left", padx=20, pady=15)
    tk.Label(header, text=f"{usuario.nombre_usuario}  |  {usuario.nombre_rol}",
             bg=COLOR_VINO, fg="white", font=("Arial", 10)).pack(side="right", padx=20)

    # Título
    tk.Label(ventana, text="MENÚ PRINCIPAL", bg=COLOR_FONDO,
             font=("Arial", 16, "bold"), fg=COLOR_VINO).pack(pady=20)

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=10)

    # Botones según el rol
    if usuario.nombre_rol == "Administrador":
        botones = [
            ("Usuarios", abrir_usuarios),
            ("Lectores", abrir_lectores),
            ("Libros", abrir_libros),
            ("Autores", abrir_autores),
            ("Editoriales / Categorías", abrir_editoriales_categorias),
            ("Ejemplares", abrir_ejemplares),
            ("Préstamos", abrir_prestamos),
            ("Devoluciones", abrir_devoluciones),
            ("Reservas", abrir_reservas),
            ("Sanciones", abrir_sanciones),
            ("Reportes", abrir_reportes),
        ]
    elif usuario.nombre_rol == "Bibliotecario":
        botones = [
            ("Lectores", abrir_lectores),
            ("Libros", abrir_libros),
            ("Ejemplares", abrir_ejemplares),
            ("Préstamos", abrir_prestamos),
            ("Devoluciones", abrir_devoluciones),
            ("Reservas", abrir_reservas),
            ("Sanciones", abrir_sanciones),
        ]
    else:  # Encargado de Reportes
        botones = [
            ("Reportes", None),
        ]

    def crear_boton(texto, comando):
        return tk.Button(frame, text=texto, bg=COLOR_CAFE, fg="white",
                         font=("Arial", 11, "bold"), width=22, height=2,
                         relief="flat", command=comando)

    fila = 0
    columna = 0
    for texto, comando in botones:
        btn = crear_boton(texto, comando if comando else lambda t=texto: messagebox.showinfo("Aviso", f"Módulo '{t}' en desarrollo"))
        btn.grid(row=fila, column=columna, padx=12, pady=10)
        columna += 1
        if columna == 3:
            columna = 0
            fila += 1

    def cerrar_sesion():
        ventana.destroy()
        from vistas.login_vista import abrir_login
        abrir_login()

    tk.Button(ventana, text="Cerrar Sesión", bg="#A63D40", fg="white",
              font=("Arial", 10, "bold"), width=15, relief="flat",
              command=cerrar_sesion).pack(pady=25)

    ventana.mainloop()