import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from controladores.ejemplares_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_ejemplares():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Ejemplares")
    ventana.geometry("1000x600")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None
    libros_dict = {}

    def cargar_libros():
        cmbLibro["values"] = []
        for id_l, titulo in obtener_libros():
            libros_dict[titulo] = id_l
        cmbLibro["values"] = list(libros_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for e in listar_ejemplares():
            disp = "Sí" if e.disponible else "No"
            tabla.insert("", tk.END, values=(
                e.id_ejemplar, e.codigo, e.titulo, e.estado_fisico,
                e.ubicacion, disp, str(e.fecha)[:10] if e.fecha else ""
            ))

    def limpiar():
        nonlocal id_seleccionado
        txtCodigo.delete(0, tk.END)
        cmbEstado.set("Bueno")
        txtUbicacion.delete(0, tk.END)
        cmbDisponible.set("Sí")
        txtFecha.delete(0, tk.END)
        txtFecha.insert(0, str(date.today()))
        cmbLibro.set("")
        id_seleccionado = None

    def validar():
        if not txtCodigo.get().strip():
            messagebox.showerror("Error", "Debe ingresar el código interno.")
            return False
        if not cmbLibro.get():
            messagebox.showerror("Error", "Debe seleccionar un libro.")
            return False
        if not txtFecha.get().strip():
            messagebox.showerror("Error", "Debe ingresar la fecha de adquisición.")
            return False
        return True

    def guardar():
        if not validar():
            return
        disponible = 1 if cmbDisponible.get() == "Sí" else 0
        res = guardar_ejemplar(
            txtCodigo.get().strip(), cmbEstado.get(), txtUbicacion.get().strip(),
            disponible, txtFecha.get().strip(), libros_dict[cmbLibro.get()]
        )
        if res == "duplicado":
            messagebox.showerror("Error", "Ya existe un ejemplar con ese código.")
            return
        if res:
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Ejemplar guardado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo guardar.")

    def seleccionar(event):
        nonlocal id_seleccionado
        sel = tabla.selection()
        if not sel:
            return
        vals = tabla.item(sel[0])["values"]
        id_seleccionado = vals[0]
        for e in listar_ejemplares():
            if e.id_ejemplar == id_seleccionado:
                txtCodigo.delete(0, tk.END)
                txtCodigo.insert(0, e.codigo)
                cmbEstado.set(e.estado_fisico)
                txtUbicacion.delete(0, tk.END)
                txtUbicacion.insert(0, e.ubicacion)
                cmbDisponible.set("Sí" if e.disponible else "No")
                txtFecha.delete(0, tk.END)
                txtFecha.insert(0, str(e.fecha)[:10] if e.fecha else "")
                cmbLibro.set(e.titulo)
                break

    def modificar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un ejemplar.")
            return
        if not validar():
            return
        disponible = 1 if cmbDisponible.get() == "Sí" else 0
        if modificar_ejemplar(
            id_seleccionado, txtCodigo.get().strip(), cmbEstado.get(),
            txtUbicacion.get().strip(), disponible, txtFecha.get().strip(),
            libros_dict[cmbLibro.get()]
        ):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Ejemplar modificado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo modificar.")

    def eliminar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un ejemplar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el ejemplar seleccionado?"):
            return
        res = eliminar_ejemplar(id_seleccionado)
        if res == "relacionado":
            messagebox.showerror("Error", "No se puede eliminar. Tiene préstamos asociados.")
        elif res:
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Ejemplar eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo eliminar.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE EJEMPLARES", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=10)

    tk.Label(frame, text="Código:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=3)
    txtCodigo = tk.Entry(frame, width=22)
    txtCodigo.grid(row=0, column=1, padx=5, pady=3)

    tk.Label(frame, text="Libro:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=(15, 0), pady=3)
    cmbLibro = ttk.Combobox(frame, width=35, state="readonly")
    cmbLibro.grid(row=0, column=3, padx=5, pady=3)

    tk.Label(frame, text="Estado físico:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=3)
    cmbEstado = ttk.Combobox(frame, width=20, state="readonly",
                             values=["Bueno", "Regular", "Dañado", "Perdido"])
    cmbEstado.grid(row=1, column=1, padx=5, pady=3)
    cmbEstado.set("Bueno")

    tk.Label(frame, text="Ubicación:", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=(15, 0), pady=3)
    txtUbicacion = tk.Entry(frame, width=37)
    txtUbicacion.grid(row=1, column=3, padx=5, pady=3)

    tk.Label(frame, text="Disponible:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=3)
    cmbDisponible = ttk.Combobox(frame, width=20, state="readonly", values=["Sí", "No"])
    cmbDisponible.grid(row=2, column=1, padx=5, pady=3)
    cmbDisponible.set("Sí")

    tk.Label(frame, text="Fecha adquisición:", bg=COLOR_FONDO).grid(row=2, column=2, sticky="w", padx=(15, 0), pady=3)
    txtFecha = tk.Entry(frame, width=37)
    txtFecha.grid(row=2, column=3, padx=5, pady=3)
    txtFecha.insert(0, str(date.today()))

    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=8)
    for txt, cmd, col in [("Guardar", guardar, "#7B4B3A"), ("Modificar", modificar, "#8C5B47"),
                          ("Eliminar", eliminar, "#A63D40"), ("Limpiar", limpiar, "#C9B79C")]:
        fg = "black" if txt == "Limpiar" else "white"
        tk.Button(frameBotones, text=txt, bg=col, fg=fg, width=12, relief="flat",
                  font=("Arial", 10, "bold"), command=cmd).pack(side="left", padx=6)

    tabla = ttk.Treeview(ventana, columns=("ID", "Codigo", "Libro", "Estado", "Ubicacion", "Disponible", "Fecha"),
                         show="headings", height=14)
    for col, txt, w in [("ID", "ID", 50), ("Codigo", "Código", 110), ("Libro", "Libro", 250),
                        ("Estado", "Estado", 100), ("Ubicacion", "Ubicación", 120),
                        ("Disponible", "Disponible", 90), ("Fecha", "Fecha", 100)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w, anchor="center")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_libros()
    actualizar_tabla()