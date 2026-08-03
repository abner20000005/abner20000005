import tkinter as tk
from tkinter import ttk, messagebox
from controladores.libros_controlador import (
    listar_libros, obtener_categorias, obtener_editoriales,
    obtener_autores, guardar_libro, modificar_libro, eliminar_libro
)

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_libros():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Gestión de Libros")
    ventana.geometry("1000x650")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    id_seleccionado = None
    categorias_dict = {}
    editoriales_dict = {}
    autores_dict = {}

    # ----- Funciones -----
    def cargar_combos():
        cmbCategoria["values"] = []
        cmbEditorial["values"] = []
        cmbAutor["values"] = []

        for id_cat, nombre in obtener_categorias():
            categorias_dict[nombre] = id_cat
            cmbCategoria["values"] = list(categorias_dict.keys())

        for id_edi, nombre in obtener_editoriales():
            editoriales_dict[nombre] = id_edi
            cmbEditorial["values"] = list(editoriales_dict.keys())

        for id_aut, nombre in obtener_autores():
            autores_dict[nombre] = id_aut
            cmbAutor["values"] = list(autores_dict.keys())

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for libro in listar_libros():
            tabla.insert("", tk.END, values=(
                libro.id_libro, libro.isbn, libro.titulo,
                libro.categoria, libro.editorial, libro.autor
            ))

    def limpiar():
        nonlocal id_seleccionado
        txtISBN.delete(0, tk.END)
        txtTitulo.delete(0, tk.END)
        txtAnio.delete(0, tk.END)
        txtEdicion.delete(0, tk.END)
        cmbCategoria.set("")
        cmbEditorial.set("")
        cmbAutor.set("")
        txtDescripcion.delete("1.0", tk.END)
        id_seleccionado = None

    def validar():
        if not txtISBN.get().strip():
            messagebox.showerror("Error", "Debe ingresar el ISBN.")
            return False
        if not txtTitulo.get().strip():
            messagebox.showerror("Error", "Debe ingresar el título.")
            return False
        if not txtAnio.get().strip().isdigit() or len(txtAnio.get()) != 4:
            messagebox.showerror("Error", "El año debe ser un número de 4 dígitos.")
            return False
        if not txtEdicion.get().strip():
            messagebox.showerror("Error", "Debe ingresar la edición.")
            return False
        if not cmbCategoria.get():
            messagebox.showerror("Error", "Debe seleccionar una categoría.")
            return False
        if not cmbEditorial.get():
            messagebox.showerror("Error", "Debe seleccionar una editorial.")
            return False
        if not cmbAutor.get():
            messagebox.showerror("Error", "Debe seleccionar un autor.")
            return False
        return True

    def guardar():
        if not validar():
            return
        ok = guardar_libro(
            txtISBN.get().strip(),
            txtTitulo.get().strip(),
            int(txtAnio.get()),
            int(txtEdicion.get()),
            txtDescripcion.get("1.0", tk.END).strip(),
            categorias_dict[cmbCategoria.get()],
            editoriales_dict[cmbEditorial.get()],
            autores_dict[cmbAutor.get()]
        )
        if not ok:
            messagebox.showerror("Error", "Ya existe un libro con ese ISBN.")
            return
        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Éxito", "Libro guardado correctamente.")

    def seleccionar(event):
        nonlocal id_seleccionado
        seleccion = tabla.selection()
        if not seleccion:
            return
        item = tabla.item(seleccion[0])
        valores = item["values"]
        id_seleccionado = valores[0]

        # Buscar el libro completo
        for libro in listar_libros():
            if libro.id_libro == id_seleccionado:
                txtISBN.delete(0, tk.END)
                txtISBN.insert(0, libro.isbn)
                txtTitulo.delete(0, tk.END)
                txtTitulo.insert(0, libro.titulo)
                txtAnio.delete(0, tk.END)
                txtAnio.insert(0, libro.anio if libro.anio else "")
                txtEdicion.delete(0, tk.END)
                txtEdicion.insert(0, libro.edicion if libro.edicion else "")
                cmbCategoria.set(libro.categoria)
                cmbEditorial.set(libro.editorial)
                cmbAutor.set(libro.autor)
                txtDescripcion.delete("1.0", tk.END)
                txtDescripcion.insert("1.0", libro.descripcion if libro.descripcion else "")
                break

    def modificar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un libro para modificar.")
            return
        if not validar():
            return
        modificar_libro(
            id_seleccionado,
            txtISBN.get().strip(),
            txtTitulo.get().strip(),
            int(txtAnio.get()),
            int(txtEdicion.get()),
            txtDescripcion.get("1.0", tk.END).strip(),
            categorias_dict[cmbCategoria.get()],
            editoriales_dict[cmbEditorial.get()],
            autores_dict[cmbAutor.get()]
        )
        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Éxito", "Libro modificado correctamente.")

    def eliminar():
        if id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un libro para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar el libro seleccionado?"):
            return
        eliminar_libro(id_seleccionado)
        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Éxito", "Libro eliminado correctamente.")

    # ----- Interfaz -----
    tk.Label(ventana, text="GESTIÓN DE LIBROS", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="x", padx=15, pady=15)

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

    tk.Label(frame, text="Descripción", bg=COLOR_FONDO).grid(row=0, column=2, sticky="nw", padx=(30, 5))
    txtDescripcion = tk.Text(frame, width=40, height=8)
    txtDescripcion.grid(row=0, column=3, rowspan=7, padx=5)

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

    tabla = ttk.Treeview(ventana, columns=("ID", "ISBN", "Titulo", "Categoria", "Editorial", "Autor"),
                         show="headings", height=12)
    for col, texto, ancho in [("ID", "ID", 50), ("ISBN", "ISBN", 110), ("Titulo", "Título", 280),
                               ("Categoria", "Categoría", 140), ("Editorial", "Editorial", 160), ("Autor", "Autor", 160)]:
        tabla.heading(col, text=texto)
        tabla.column(col, width=ancho, anchor="center" if col != "Titulo" else "w")
    tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_combos()
    actualizar_tabla()