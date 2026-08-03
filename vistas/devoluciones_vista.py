import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from controladores.devoluciones_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_devoluciones():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Devoluciones")
    ventana.geometry("1050x600")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    prestamos_dict = {}  # texto -> (id_prestamo, fecha_limite, id_ejemplar)

    def cargar_prestamos():
        cmbPrestamo["values"] = []
        prestamos_dict.clear()
        for id_p, texto, f_limite, id_e in obtener_prestamos_activos():
            prestamos_dict[texto] = (id_p, f_limite, id_e)
        cmbPrestamo["values"] = list(prestamos_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for d in listar_devoluciones():
            tabla.insert("", tk.END, values=(
                d.id_devolucion, str(d.fecha)[:10], d.dias_retraso, f"L. {d.multa:.2f}",
                d.lector, d.codigo, d.libro
            ))

    def limpiar():
        cmbPrestamo.set("")
        txtFecha.delete(0, tk.END)
        txtFecha.insert(0, str(date.today()))
        lblInfo.config(text="")

    def registrar():
        if not cmbPrestamo.get():
            messagebox.showerror("Error", "Debe seleccionar un préstamo.")
            return
        if not txtFecha.get().strip():
            messagebox.showerror("Error", "Debe ingresar la fecha de devolución.")
            return

        id_prestamo, fecha_limite, id_ejemplar = prestamos_dict[cmbPrestamo.get()]
        ok, dias, multa = registrar_devolucion(
            id_prestamo, id_ejemplar, fecha_limite, txtFecha.get().strip()
        )
        if ok:
            actualizar_tabla()
            cargar_prestamos()
            limpiar()
            if dias > 0:
                messagebox.showinfo("Éxito", f"Devolución registrada.\nDías de retraso: {dias}\nMulta: L. {multa:.2f}")
            else:
                messagebox.showinfo("Éxito", "Devolución registrada sin retraso.")
        else:
            messagebox.showerror("Error", "No se pudo registrar la devolución.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE DEVOLUCIONES", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=12)

    tk.Label(frame, text="Préstamo activo:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=4)
    cmbPrestamo = ttk.Combobox(frame, width=70, state="readonly")
    cmbPrestamo.grid(row=0, column=1, columnspan=3, padx=5, pady=4, sticky="w")

    tk.Label(frame, text="Fecha devolución:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=4)
    txtFecha = tk.Entry(frame, width=20)
    txtFecha.grid(row=1, column=1, padx=5, pady=4, sticky="w")
    txtFecha.insert(0, str(date.today()))

    lblInfo = tk.Label(frame, text="", bg=COLOR_FONDO, fg=COLOR_VINO, font=("Arial", 10, "bold"))
    lblInfo.grid(row=1, column=2, columnspan=2, sticky="w", padx=10)

    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=8)
    tk.Button(frameBotones, text="Registrar Devolución", bg="#7B4B3A", fg="white", width=20,
              relief="flat", font=("Arial", 10, "bold"), command=registrar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Limpiar", bg="#C9B79C", fg="black", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=limpiar).pack(side="left", padx=6)

    tabla = ttk.Treeview(ventana, columns=("ID", "Fecha", "Retraso", "Multa", "Lector", "Codigo", "Libro"),
                         show="headings", height=14)
    for col, txt, w in [("ID", "ID", 50), ("Fecha", "Fecha", 100), ("Retraso", "Días retraso", 100),
                        ("Multa", "Multa", 90), ("Lector", "Lector", 180), ("Codigo", "Código", 100),
                        ("Libro", "Libro", 220)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w, anchor="center")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    cargar_prestamos()
    actualizar_tabla()