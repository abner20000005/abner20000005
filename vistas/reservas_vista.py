import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from controladores.reservas_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_reservas():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Reservas")
    ventana.geometry("1000x580")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None
    lectores_dict = {}
    libros_dict = {}

    def cargar_combos():
        cmbLector["values"] = []
        cmbLibro["values"] = []
        for id_l, nombre in obtener_lectores():
            lectores_dict[nombre] = id_l
        cmbLector["values"] = list(lectores_dict.keys())
        for id_li, titulo in obtener_libros():
            libros_dict[titulo] = id_li
        cmbLibro["values"] = list(libros_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for r in listar_reservas():
            tabla.insert("", tk.END, values=(
                r.id_reserva, str(r.fecha)[:10], r.estado, r.lector, r.libro
            ))

    def limpiar():
        nonlocal id_seleccionado
        cmbLector.set("")
        cmbLibro.set("")
        txtFecha.delete(0, tk.END)
        txtFecha.insert(0, str(date.today()))
        id_seleccionado = None

    def guardar():
        if not cmbLector.get():
            messagebox.showerror("Error", "Debe seleccionar un lector.")
            return
        if not cmbLibro.get():
            messagebox.showerror("Error", "Debe seleccionar un libro.")
            return
        if not txtFecha.get().strip():
            messagebox.showerror("Error", "Debe ingresar la fecha.")
            return
        if guardar_reserva(txtFecha.get().strip(), lectores_dict[cmbLector.get()], libros_dict[cmbLibro.get()]):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Reserva registrada correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo registrar la reserva.")

    def seleccionar(event):
        nonlocal id_seleccionado
        sel = tabla.selection()
        if not sel:
            return
        id_seleccionado = tabla.item(sel[0])["values"][0]

    def cancelar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione una reserva.")
            return
        if not messagebox.askyesno("Confirmar", "¿Cancelar la reserva seleccionada?"):
            return
        if cancelar_reserva(id_seleccionado):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Reserva cancelada correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo cancelar.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE RESERVAS", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=12)

    tk.Label(frame, text="Lector:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=4)
    cmbLector = ttk.Combobox(frame, width=35, state="readonly")
    cmbLector.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame, text="Libro:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=(15, 0), pady=4)
    cmbLibro = ttk.Combobox(frame, width=40, state="readonly")
    cmbLibro.grid(row=0, column=3, padx=5, pady=4)

    tk.Label(frame, text="Fecha reserva:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=4)
    txtFecha = tk.Entry(frame, width=37)
    txtFecha.grid(row=1, column=1, padx=5, pady=4)
    txtFecha.insert(0, str(date.today()))

    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=8)
    tk.Button(frameBotones, text="Registrar Reserva", bg="#7B4B3A", fg="white", width=18,
              relief="flat", font=("Arial", 10, "bold"), command=guardar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Cancelar Reserva", bg="#A63D40", fg="white", width=16,
              relief="flat", font=("Arial", 10, "bold"), command=cancelar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Limpiar", bg="#C9B79C", fg="black", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=limpiar).pack(side="left", padx=6)

    tabla = ttk.Treeview(ventana, columns=("ID", "Fecha", "Estado", "Lector", "Libro"),
                         show="headings", height=14)
    for col, txt, w in [("ID", "ID", 50), ("Fecha", "Fecha", 110), ("Estado", "Estado", 100),
                        ("Lector", "Lector", 220), ("Libro", "Libro", 300)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w, anchor="center")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_combos()
    actualizar_tabla()