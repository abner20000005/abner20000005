import tkinter as tk
from tkinter import ttk, messagebox
from controladores.libros_controlador import (
    guardar_libro, listar_libros, eliminar_libro, modificar_libro, obtener_libro
)

# Ventana principal
ventana = tk.Tk()
ventana.title("Biblioteca 360 - Gestión de Libros")
ventana.geometry("1000x650")
ventana.configure(bg="#F4EEE8")
ventana.resizable(False, False)

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

# Estilos de la tabla
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=25, font=("Arial", 10))
style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

indice_seleccionado = None

# ---------- FUNCIONES ----------

def actualizar_tabla():
    tabla.delete(*tabla.get_children())
    for libro in listar_libros():
        tabla.insert("", tk.END, values=(
            libro.isbn, libro.titulo, libro.categoria, libro.editorial, libro.autor
        ))

def limpiar():
    global indice_seleccionado
    txtISBN.delete(0, tk.END)
    txtTitulo.delete(0, tk.END)
    txtAnio.delete(0, tk.END)
    txtEdicion.delete(0, tk.END)
    cmbCategoria.set("")
    cmbEditorial.set("")
    cmbAutor.set("")
    txtDescripcion.delete("1.0", tk.END)
    indice_seleccionado = None

def validar_datos():
    if txtISBN.get().strip() == "":
        messagebox.showerror("Error", "Debe ingresar el ISBN.")
        txtISBN.focus()
        return False
    if not txtISBN.get().isdigit():
        messagebox.showerror("Error", "El ISBN solo puede contener números.")
        txtISBN.focus()
        return False
    if txtTitulo.get().strip() == "":
        messagebox.showerror("Error", "Debe ingresar el título.")
        txtTitulo.focus()
        return False
    if txtAnio.get().strip() == "":
        messagebox.showerror("Error", "Debe ingresar el año.")
        txtAnio.focus()
        return False
    if not txtAnio.get().isdigit():
        messagebox.showerror("Error", "El año solo puede contener números.")
        txtAnio.focus()
        return False
    if len(txtAnio.get()) != 4:
        messagebox.showerror("Error", "El año debe tener 4 dígitos.")
        txtAnio.focus()
        return False
    if txtEdicion.get().strip() == "":
        messagebox.showerror("Error", "Debe ingresar la edición.")
        txtEdicion.focus()
        return False
    if cmbCategoria.get() == "":
        messagebox.showerror("Error", "Debe seleccionar una categoría.")
        cmbCategoria.focus()
        return False
    if cmbEditorial.get() == "":
        messagebox.showerror("Error", "Debe seleccionar una editorial.")
        cmbEditorial.focus()
        return False
    if cmbAutor.get() == "":
        messagebox.showerror("Error", "Debe seleccionar un autor.")
        cmbAutor.focus()
        return False
    return True

def guardar():
    if not validar_datos():
        return
    guardado = guardar_libro(
        txtISBN.get(), txtTitulo.get(), txtAnio.get(), txtEdicion.get(),
        txtDescripcion.get("1.0", tk.END).strip(),
        cmbCategoria.get(), cmbEditorial.get(), cmbAutor.get()
    )
    if not guardado:
        messagebox.showerror("Error", "Ya existe un libro con ese ISBN.")
        txtISBN.focus()
        return
    actualizar_tabla()
    limpiar()
    messagebox.showinfo("Éxito", "Libro guardado correctamente.")

def seleccionar_libro(event):
    global indice_seleccionado
    seleccion = tabla.selection()
    if not seleccion:
        return
    indice_seleccionado = tabla.index(seleccion[0])
    libro = obtener_libro(indice_seleccionado)
    if libro is None:
        return
    txtISBN.delete(0, tk.END)
    txtISBN.insert(0, libro.isbn)
    txtTitulo.delete(0, tk.END)
    txtTitulo.insert(0, libro.titulo)
    txtAnio.delete(0, tk.END)
    txtAnio.insert(0, libro.anio)
    txtEdicion.delete(0, tk.END)
    txtEdicion.insert(0, libro.edicion)
    cmbCategoria.set(libro.categoria)
    cmbEditorial.set(libro.editorial)
    cmbAutor.set(libro.autor)
    txtDescripcion.delete("1.0", tk.END)
    txtDescripcion.insert("1.0", libro.descripcion)

def modificar():
    global indice_seleccionado
    if indice_seleccionado is None:
        messagebox.showwarning("Aviso", "Seleccione un libro para modificar.")
        return
    if not validar_datos():
        return
    modificar_libro(
        indice_seleccionado,
        txtISBN.get(), txtTitulo.get(), txtAnio.get(), txtEdicion.get(),
        txtDescripcion.get("1.0", tk.END).strip(),
        cmbCategoria.get(), cmbEditorial.get(), cmbAutor.get()
    )
    actualizar_tabla()
    limpiar()
    messagebox.showinfo("Éxito", "Libro modificado correctamente.")

def eliminar():
    global indice_seleccionado
    if indice_seleccionado is None:
        messagebox.showwarning("Aviso", "Seleccione un libro para eliminar.")
        return
    if not messagebox.askyesno("Confirmar", "¿Desea eliminar el libro seleccionado?"):
        return
    eliminar_libro(indice_seleccionado)
    actualizar_tabla()
    limpiar()
    messagebox.showinfo("Éxito", "Libro eliminado correctamente.")

# ---------- INTERFAZ ----------

tk.Label(ventana, text="GESTIÓN DE LIBROS", bg=COLOR_VINO, fg="white",
         font=("Arial", 18, "bold"), pady=10).pack(fill="x")

frame = tk.Frame(ventana, bg=COLOR_FONDO)
frame.pack(fill="x", padx=15, pady=15)

# Columna izquierda
tk.Label(frame, text="ISBN", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w")
txtISBN = tk.Entry(frame, width=28)
txtISBN.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Título", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w")
txtTitulo = tk.Entry(frame, width=28)
txtTitulo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Año", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w")
txtAnio = tk.Entry(frame, width=10)
txtAnio.grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(frame, text="Edición", bg=COLOR_FONDO).grid(row=3, column=0, sticky="w")
txtEdicion = tk.Entry(frame, width=10)
txtEdicion.grid(row=3, column=1, sticky="w", padx=5, pady=5)

tk.Label(frame, text="Categoría", bg=COLOR_FONDO).grid(row=4, column=0, sticky="w")
cmbCategoria = ttk.Combobox(frame, width=25, state="readonly")
cmbCategoria.grid(row=4, column=1, padx=5, pady=5)

tk.Label(frame, text="Editorial", bg=COLOR_FONDO).grid(row=5, column=0, sticky="w")
cmbEditorial = ttk.Combobox(frame, width=25, state="readonly")
cmbEditorial.grid(row=5, column=1, padx=5, pady=5)

tk.Label(frame, text="Autor", bg=COLOR_FONDO).grid(row=6, column=0, sticky="w")
cmbAutor = ttk.Combobox(frame, width=25, state="readonly")
cmbAutor.grid(row=6, column=1, padx=5, pady=5)

# Columna derecha
tk.Label(frame, text="Descripción", bg=COLOR_FONDO).grid(row=0, column=2, sticky="nw", padx=(30, 5))
txtDescripcion = tk.Text(frame, width=40, height=8)
txtDescripcion.grid(row=0, column=3, rowspan=7, padx=5)

# Botones
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

# Tabla
tabla = ttk.Treeview(ventana, columns=("ISBN", "Titulo", "Categoria", "Editorial", "Autor"),
                     show="headings", height=12)
tabla.heading("ISBN", text="ISBN")
tabla.heading("Titulo", text="Título")
tabla.heading("Categoria", text="Categoría")
tabla.heading("Editorial", text="Editorial")
tabla.heading("Autor", text="Autor")
tabla.column("ISBN", width=120, anchor="center")
tabla.column("Titulo", width=320)
tabla.column("Categoria", width=160, anchor="center")
tabla.column("Editorial", width=180, anchor="center")
tabla.column("Autor", width=180)
tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
tabla.bind("<<TreeviewSelect>>", seleccionar_libro)

actualizar_tabla()
ventana.mainloop()