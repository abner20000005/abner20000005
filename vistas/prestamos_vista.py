import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
from controladores.prestamos_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_prestamos():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Préstamos")
    ventana.geometry("1050x600")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None
    id_ejemplar_sel = None
    lectores_dict = {}
    ejemplares_dict = {}

    def cargar_combos():
        cmbLector["values"] = []
        cmbEjemplar["values"] = []
        for id_l, nombre in obtener_lectores_activos():
            lectores_dict[nombre] = id_l
        cmbLector["values"] = list(lectores_dict.keys())
        for id_e, texto in obtener_ejemplares_disponibles():
            ejemplares_dict[texto] = id_e
        cmbEjemplar["values"] = list(ejemplares_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for p in listar_prestamos():
            tabla.insert("", tk.END, values=(
                p.id_prestamo, str(p.fecha_prestamo)[:10], str(p.fecha_limite)[:10],
                p.estado, p.lector, p.codigo, p.libro
            ))

    def limpiar():
        nonlocal id_seleccionado, id_ejemplar_sel
        cmbLector.set("")
        cmbEjemplar.set("")
        txtFechaPrestamo.delete(0, tk.END)
        txtFechaPrestamo.insert(0, str(date.today()))
        txtFechaLimite.delete(0, tk.END)
        txtFechaLimite.insert(0, str(date.today() + timedelta(days=15)))
        id_seleccionado = None
        id_ejemplar_sel = None
        cargar_combos()

    def validar():
        if not cmbLector.get():
            messagebox.showerror("Error", "Debe seleccionar un lector.")
            return False
        if not cmbEjemplar.get():
            messagebox.showerror("Error", "Debe seleccionar un ejemplar.")
            return False
        if not txtFechaPrestamo.get().strip() or not txtFechaLimite.get().strip():
            messagebox.showerror("Error", "Debe ingresar las fechas.")
            return False
        return True

    def guardar():
        if not validar():
            return
        if guardar_prestamo(
            txtFechaPrestamo.get().strip(),
            txtFechaLimite.get().strip(),
            lectores_dict[cmbLector.get()],
            ejemplares_dict[cmbEjemplar.get()]
        ):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo registrar el préstamo.")

    def seleccionar(event):
        nonlocal id_seleccionado, id_ejemplar_sel
        sel = tabla.selection()
        if not sel:
            return
        vals = tabla.item(sel[0])["values"]
        id_seleccionado = vals[0]
        for p in listar_prestamos():
            if p.id_prestamo == id_seleccionado:
                id_ejemplar_sel = p.id_ejemplar
                break

    def anular():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un préstamo.")
            return
        if not messagebox.askyesno("Confirmar", "¿Anular el préstamo seleccionado?"):
            return
        if anular_prestamo(id_seleccionado, id_ejemplar_sel):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Préstamo anulado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo anular.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE PRÉSTAMOS", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=10)

    tk.Label(frame, text="Lector:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=4)
    cmbLector = ttk.Combobox(frame, width=35, state="readonly")
    cmbLector.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame, text="Ejemplar:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=(15, 0), pady=4)
    cmbEjemplar = ttk.Combobox(frame, width=40, state="readonly")
    cmbEjemplar.grid(row=0, column=3, padx=5, pady=4)

    tk.Label(frame, text="Fecha préstamo:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=4)
    txtFechaPrestamo = tk.Entry(frame, width=37)
    txtFechaPrestamo.grid(row=1, column=1, padx=5, pady=4)
    txtFechaPrestamo.insert(0, str(date.today()))

    tk.Label(frame, text="Fecha límite:", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=(15, 0), pady=4)
    txtFechaLimite = tk.Entry(frame, width=42)
    txtFechaLimite.grid(row=1, column=3, padx=5, pady=4)
    txtFechaLimite.insert(0, str(date.today() + timedelta(days=15)))

    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=8)
    tk.Button(frameBotones, text="Registrar Préstamo", bg="#7B4B3A", fg="white", width=18,
              relief="flat", font=("Arial", 10, "bold"), command=guardar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Anular Préstamo", bg="#A63D40", fg="white", width=16,
              relief="flat", font=("Arial", 10, "bold"), command=anular).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Limpiar", bg="#C9B79C", fg="black", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=limpiar).pack(side="left", padx=6)

    tabla = ttk.Treeview(ventana, columns=("ID", "F.Prestamo", "F.Limite", "Estado", "Lector", "Codigo", "Libro"),
                         show="headings", height=14)
    for col, txt, w in [("ID", "ID", 50), ("F.Prestamo", "F. Préstamo", 100), ("F.Limite", "F. Límite", 100),
                        ("Estado", "Estado", 90), ("Lector", "Lector", 180), ("Codigo", "Código", 100),
                        ("Libro", "Libro", 220)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w, anchor="center")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_combos()
    actualizar_tabla()