import tkinter as tk
from tkinter import ttk, messagebox
from controladores.autores_controlador import (
    listar_autores, guardar_autor, modificar_autor, eliminar_autor
)

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_autores():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Autores")
    ventana.geometry("700x500")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for autor in listar_autores():
            tabla.insert("", tk.END, values=(autor.id_autor, autor.nombre, autor.nacionalidad))

    def limpiar():
        nonlocal id_seleccionado
        txtNombre.delete(0, tk.END)
        txtNacionalidad.delete(0, tk.END)
        id_seleccionado = None

    def validar():
        if not txtNombre.get().strip():
            messagebox.showerror("Error", "Debe ingresar el nombre del autor.")
            return False
        return True

    def guardar():
        if not validar():
            return
        if guardar_autor(txtNombre.get().strip(), txtNacionalidad.get().strip()):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Autor guardado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo guardar el autor.")

    def seleccionar(event):
        nonlocal id_seleccionado
        seleccion = tabla.selection()
        if not seleccion:
            return
        valores = tabla.item(seleccion[0])["values"]
        id_seleccionado = valores[0]
        txtNombre.delete(0, tk.END)
        txtNombre.insert(0, valores[1])
        txtNacionalidad.delete(0, tk.END)
        txtNacionalidad.insert(0, valores[2])

    def modificar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un autor para modificar.")
            return
        if not validar():
            return
        if modificar_autor(id_seleccionado, txtNombre.get().strip(), txtNacionalidad.get().strip()):
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Autor modificado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo modificar el autor.")

    def eliminar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un autor para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar el autor seleccionado?"):
            return
        resultado = eliminar_autor(id_seleccionado)
        if resultado == "relacionado":
            messagebox.showerror("Error", "No se puede eliminar. El autor tiene libros asociados.")
        elif resultado:
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Autor eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el autor.")

    # Interfaz
    tk.Label(ventana, text="GESTIÓN DE AUTORES", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=20, pady=15)

    tk.Label(frame, text="Nombre:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
    txtNombre = tk.Entry(frame, width=40)
    txtNombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nacionalidad:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
    txtNacionalidad = tk.Entry(frame, width=40)
    txtNacionalidad.grid(row=1, column=1, padx=10, pady=5)

    frameBotones = tk.Frame(ventana, bg=COLOR_FONDO)
    frameBotones.pack(pady=10)

    tk.Button(frameBotones, text="Guardar", bg="#7B4B3A", fg="white", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=guardar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Modificar", bg="#8C5B47", fg="white", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=modificar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Eliminar", bg="#A63D40", fg="white", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=eliminar).pack(side="left", padx=6)
    tk.Button(frameBotones, text="Limpiar", bg="#C9B79C", fg="black", width=12,
              relief="flat", font=("Arial", 10, "bold"), command=limpiar).pack(side="left", padx=6)

    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Nacionalidad"), show="headings", height=12)
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Nacionalidad", text="Nacionalidad")
    tabla.column("ID", width=60, anchor="center")
    tabla.column("Nombre", width=300)
    tabla.column("Nacionalidad", width=200, anchor="center")
    tabla.pack(fill="both", expand=True, padx=20, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    actualizar_tabla()