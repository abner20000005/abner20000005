import tkinter as tk
from tkinter import ttk, messagebox
from controladores.sanciones_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_sanciones():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Sanciones")
    ventana.geometry("1000x580")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None
    monto_sel = 0
    lectores_dict = {}

    def cargar_lectores():
        cmbLector["values"] = []
        for id_l, nombre in obtener_lectores():
            lectores_dict[nombre] = id_l
        cmbLector["values"] = list(lectores_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for s in listar_sanciones():
            tabla.insert("", tk.END, values=(
                s.id_sancion, s.lector, s.motivo, f"L. {s.monto:.2f}", s.estado
            ))

    def limpiar():
        nonlocal id_seleccionado, monto_sel
        cmbLector.set("")
        txtMotivo.delete(0, tk.END)
        txtMonto.delete(0, tk.END)
        id_seleccionado = None
        monto_sel = 0

    def guardar():
        if not cmbLector.get():
            messagebox.showerror("Error", "Debe seleccionar un lector.")
            return
        if not txtMotivo.get().strip():
            messagebox.showerror("Error", "Debe ingresar el motivo.")
            return
        if not txtMonto.get().strip():
            messagebox.showerror("Error", "Debe ingresar el monto.")
            return
        try:
            monto = float(txtMonto.get())
        except:
            messagebox.showerror("Error", "El monto debe ser un número.")
            return
        if guardar_sancion(txtMotivo.get().strip(), monto, lectores_dict[cmbLector.get()]):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Sanción registrada correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo registrar.")

    def seleccionar(event):
        nonlocal id_seleccionado, monto_sel
        sel = tabla.selection()
        if not sel:
            return
        vals = tabla.item(sel[0])["values"]
        id_seleccionado = vals[0]
        # Extraer monto numérico
        for s in listar_sanciones():
            if s.id_sancion == id_seleccionado:
                monto_sel = float(s.monto)
                break

    def pagar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione una sanción.")
            return
        if not messagebox.askyesno("Confirmar", "¿Registrar el pago de esta sanción?"):
            return
        if pagar_sancion(id_seleccionado, monto_sel):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Pago registrado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo registrar el pago.")

    def anular():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione una sanción.")
            return
        if not messagebox.askyesno("Confirmar", "¿Anular la sanción seleccionada?"):
            return
        if anular_sancion(id_seleccionado):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Sanción anulada correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo anular.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE SANCIONES", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=12)

    tk.Label(frame, text="Lector:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=4)
    cmbLector = ttk.Combobox(frame, width=35, state="readonly")
    cmbLector.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame, text="Monto (L):", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=(15, 0), pady=4)
    txtMonto = tk.Entry(frame, width=15)
    txtMonto.grid(row=0, column=3, padx=5, pady=4, sticky="w")

    tk.Label(frame, text="Motivo:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=4)
    txtMotivo = tk.Entry(frame, width=80)
    txtMotivo.grid(row=1, column=1, columnspan=3, padx=5, pady=4, sticky="w")

    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=8)
    tk.Button(frameBotones, text="Registrar Sanción", bg="#7B4B3A", fg="white", width=16,
              relief="flat", font=("Arial", 10, "bold"), command=guardar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Registrar Pago", bg="#8C5B47", fg="white", width=14,
              relief="flat", font=("Arial", 10, "bold"), command=pagar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Anular", bg="#A63D40", fg="white", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=anular).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Limpiar", bg="#C9B79C", fg="black", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=limpiar).pack(side="left", padx=6)

    tabla = ttk.Treeview(ventana, columns=("ID", "Lector", "Motivo", "Monto", "Estado"),
                         show="headings", height=14)
    for col, txt, w in [("ID", "ID", 50), ("Lector", "Lector", 200), ("Motivo", "Motivo", 380),
                        ("Monto", "Monto", 100), ("Estado", "Estado", 100)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w, anchor="center")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_lectores()
    actualizar_tabla()