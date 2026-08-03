import tkinter as tk
from tkinter import ttk, messagebox
from controladores.lectores_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_lectores():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Lectores")
    ventana.geometry("1050x620")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None
    tipos_dict = {}

    def cargar_tipos():
        cmbTipo["values"] = []
        for id_t, nombre in obtener_tipos_lectores():
            tipos_dict[nombre] = id_t
        cmbTipo["values"] = list(tipos_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for l in listar_lectores():
            tabla.insert("", tk.END, values=(
                l.id_lector, l.nombre, l.apellido, l.identidad,
                l.telefono or "", l.tipo, l.estado or ""
            ))

    def limpiar():
        nonlocal id_seleccionado
        for w in (txtNombre, txtApellido, txtIdentidad, txtTelefono, txtCorreo, txtDireccion):
            w.delete(0, tk.END)
        cmbTipo.set("")
        cmbEstado.set("Activo")
        id_seleccionado = None

    def validar():
        if not txtNombre.get().strip():
            messagebox.showerror("Error", "Debe ingresar el nombre.")
            return False
        if not txtApellido.get().strip():
            messagebox.showerror("Error", "Debe ingresar el apellido.")
            return False
        if not txtIdentidad.get().strip():
            messagebox.showerror("Error", "Debe ingresar la identidad.")
            return False
        if not cmbTipo.get():
            messagebox.showerror("Error", "Debe seleccionar el tipo de lector.")
            return False
        return True

    def guardar():
        if not validar():
            return
        res = guardar_lector(
            txtNombre.get().strip(), txtApellido.get().strip(), txtIdentidad.get().strip(),
            txtTelefono.get().strip(), txtCorreo.get().strip(), txtDireccion.get().strip(),
            cmbEstado.get(), tipos_dict[cmbTipo.get()]
        )
        if res == "duplicado":
            messagebox.showerror("Error", "Ya existe un lector con esa identidad.")
            return
        if res:
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Lector guardado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo guardar el lector.")

    def seleccionar(event):
        nonlocal id_seleccionado
        sel = tabla.selection()
        if not sel:
            return
        vals = tabla.item(sel[0])["values"]
        id_seleccionado = vals[0]
        for l in listar_lectores():
            if l.id_lector == id_seleccionado:
                txtNombre.delete(0, tk.END)
                txtNombre.insert(0, l.nombre)
                txtApellido.delete(0, tk.END)
                txtApellido.insert(0, l.apellido)
                txtIdentidad.delete(0, tk.END)
                txtIdentidad.insert(0, l.identidad)
                txtTelefono.delete(0, tk.END)
                txtTelefono.insert(0, l.telefono or "")
                txtCorreo.delete(0, tk.END)
                txtCorreo.insert(0, l.correo or "")
                txtDireccion.delete(0, tk.END)
                txtDireccion.insert(0, l.direccion or "")
                cmbTipo.set(l.tipo)
                cmbEstado.set(l.estado or "Activo")
                break

    def modificar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un lector.")
            return
        if not validar():
            return
        if modificar_lector(
            id_seleccionado, txtNombre.get().strip(), txtApellido.get().strip(),
            txtIdentidad.get().strip(), txtTelefono.get().strip(), txtCorreo.get().strip(),
            txtDireccion.get().strip(), cmbEstado.get(), tipos_dict[cmbTipo.get()]
        ):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Lector modificado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo modificar.")

    def eliminar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un lector.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el lector seleccionado?"):
            return
        res = eliminar_lector(id_seleccionado)
        if res == "relacionado":
            messagebox.showerror("Error", "No se puede eliminar. Tiene préstamos asociados.")
        elif res:
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Lector eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo eliminar.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE LECTORES", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=10)

    # Columna 1
    tk.Label(frame, text="Nombre:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=3)
    txtNombre = tk.Entry(frame, width=25)
    txtNombre.grid(row=0, column=1, padx=5, pady=3)

    tk.Label(frame, text="Apellido:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=3)
    txtApellido = tk.Entry(frame, width=25)
    txtApellido.grid(row=1, column=1, padx=5, pady=3)

    tk.Label(frame, text="Identidad:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=3)
    txtIdentidad = tk.Entry(frame, width=25)
    txtIdentidad.grid(row=2, column=1, padx=5, pady=3)

    tk.Label(frame, text="Teléfono:", bg=COLOR_FONDO).grid(row=3, column=0, sticky="w", pady=3)
    txtTelefono = tk.Entry(frame, width=25)
    txtTelefono.grid(row=3, column=1, padx=5, pady=3)

    # Columna 2
    tk.Label(frame, text="Correo:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=(20, 0), pady=3)
    txtCorreo = tk.Entry(frame, width=30)
    txtCorreo.grid(row=0, column=3, padx=5, pady=3)

    tk.Label(frame, text="Dirección:", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=(20, 0), pady=3)
    txtDireccion = tk.Entry(frame, width=30)
    txtDireccion.grid(row=1, column=3, padx=5, pady=3)

    tk.Label(frame, text="Tipo:", bg=COLOR_FONDO).grid(row=2, column=2, sticky="w", padx=(20, 0), pady=3)
    cmbTipo = ttk.Combobox(frame, width=27, state="readonly")
    cmbTipo.grid(row=2, column=3, padx=5, pady=3)

    tk.Label(frame, text="Estado:", bg=COLOR_FONDO).grid(row=3, column=2, sticky="w", padx=(20, 0), pady=3)
    cmbEstado = ttk.Combobox(frame, width=27, state="readonly", values=["Activo", "Inactivo", "Bloqueado"])
    cmbEstado.grid(row=3, column=3, padx=5, pady=3)
    cmbEstado.set("Activo")

    # Botones
    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=8)
    for txt, cmd, col in [("Guardar", guardar, "#7B4B3A"), ("Modificar", modificar, "#8C5B47"),
                          ("Eliminar", eliminar, "#A63D40"), ("Limpiar", limpiar, "#C9B79C")]:
        fg = "black" if txt == "Limpiar" else "white"
        tk.Button(frameBotones, text=txt, bg=col, fg=fg, width=12, relief="flat",
                  font=("Arial", 10, "bold"), command=cmd).pack(side="left", padx=6)

    # Tabla
    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Apellido", "Identidad", "Telefono", "Tipo", "Estado"),
                         show="headings", height=14)
    for col, txt, w in [("ID", "ID", 50), ("Nombre", "Nombre", 130), ("Apellido", "Apellido", 130),
                        ("Identidad", "Identidad", 120), ("Telefono", "Teléfono", 110),
                        ("Tipo", "Tipo", 120), ("Estado", "Estado", 100)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w, anchor="center")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_tipos()
    actualizar_tabla()
