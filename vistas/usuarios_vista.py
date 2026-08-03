import tkinter as tk
from tkinter import ttk, messagebox
from controladores.usuarios_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Usuarios")
    ventana.geometry("900x550")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None
    roles_dict = {}

    def cargar_roles():
        cmbRol["values"] = []
        for id_r, nombre in obtener_roles():
            roles_dict[nombre] = id_r
        cmbRol["values"] = list(roles_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for u in listar_usuarios():
            tabla.insert("", tk.END, values=(
                u.id_usuario, u.nombre_usuario, u.contrasena, u.estado, u.nombre_rol
            ))

    def limpiar():
        nonlocal id_seleccionado
        txtUsuario.delete(0, tk.END)
        txtClave.delete(0, tk.END)
        cmbEstado.set("Activo")
        cmbRol.set("")
        id_seleccionado = None

    def validar():
        if not txtUsuario.get().strip():
            messagebox.showerror("Error", "Debe ingresar el nombre de usuario.")
            return False
        if not txtClave.get().strip():
            messagebox.showerror("Error", "Debe ingresar la contraseña.")
            return False
        if not cmbRol.get():
            messagebox.showerror("Error", "Debe seleccionar un rol.")
            return False
        return True

    def guardar():
        if not validar():
            return
        res = guardar_usuario(
            txtUsuario.get().strip(), txtClave.get().strip(),
            cmbEstado.get(), roles_dict[cmbRol.get()]
        )
        if res == "duplicado":
            messagebox.showerror("Error", "Ese nombre de usuario ya existe.")
            return
        if res:
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo guardar.")

    def seleccionar(event):
        nonlocal id_seleccionado
        sel = tabla.selection()
        if not sel:
            return
        vals = tabla.item(sel[0])["values"]
        id_seleccionado = vals[0]
        txtUsuario.delete(0, tk.END)
        txtUsuario.insert(0, vals[1])
        txtClave.delete(0, tk.END)
        txtClave.insert(0, vals[2])
        cmbEstado.set(vals[3])
        cmbRol.set(vals[4])

    def modificar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un usuario.")
            return
        if not validar():
            return
        if modificar_usuario(
            id_seleccionado, txtUsuario.get().strip(), txtClave.get().strip(),
            cmbEstado.get(), roles_dict[cmbRol.get()]
        ):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Usuario modificado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo modificar.")

    def eliminar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un usuario.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el usuario seleccionado?"):
            return
        if eliminar_usuario(id_seleccionado):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo eliminar.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE USUARIOS", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=12)

    tk.Label(frame, text="Usuario:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=4)
    txtUsuario = tk.Entry(frame, width=25)
    txtUsuario.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame, text="Contraseña:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=(15, 0), pady=4)
    txtClave = tk.Entry(frame, width=25)
    txtClave.grid(row=0, column=3, padx=5, pady=4)

    tk.Label(frame, text="Estado:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=4)
    cmbEstado = ttk.Combobox(frame, width=22, state="readonly", values=["Activo", "Inactivo"])
    cmbEstado.grid(row=1, column=1, padx=5, pady=4)
    cmbEstado.set("Activo")

    tk.Label(frame, text="Rol:", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=(15, 0), pady=4)
    cmbRol = ttk.Combobox(frame, width=22, state="readonly")
    cmbRol.grid(row=1, column=3, padx=5, pady=4)

    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=8)
    for txt, cmd, col in [("Guardar", guardar, "#7B4B3A"), ("Modificar", modificar, "#8C5B47"),
                          ("Eliminar", eliminar, "#A63D40"), ("Limpiar", limpiar, "#C9B79C")]:
        fg = "black" if txt == "Limpiar" else "white"
        tk.Button(frameBotones, text=txt, bg=col, fg=fg, width=12, relief="flat",
                  font=("Arial", 10, "bold"), command=cmd).pack(side="left", padx=6)

    tabla = ttk.Treeview(ventana, columns=("ID", "Usuario", "Contraseña", "Estado", "Rol"),
                         show="headings", height=14)
    for col, txt, w in [("ID", "ID", 50), ("Usuario", "Usuario", 180), ("Contraseña", "Contraseña", 150),
                        ("Estado", "Estado", 100), ("Rol", "Rol", 180)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w, anchor="center")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_roles()
    actualizar_tabla()