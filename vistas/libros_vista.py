"""
- Formulario para el registro, edición y búsqueda de libros (ISBN, título, categoría, editorial, autores).
- Visualización del catálogo de libros en una tabla con barra de búsqueda y filtros.
- Permite la gestión de los ejemplares físicos vinculados a cada libro y su ubicación.
"""
import tkinter as tk
from tkinter import ttk

from controladores.libros_controlador import (
    guardar_libro,
    listar_libros,
    eliminar_libro,
    modificar_libro
)


#VENTANA

ventana = tk.Tk()
ventana.title("Biblioteca 360 - Gestión de Libros")
ventana.geometry("1000x650")
ventana.configure(bg="#F4EEE8")
ventana.resizable(False, False)

#ESTILOS 

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=25,
    font=("Arial",10)
)

style.configure(
    "Treeview.Heading",
    background=COLOR_VINO,
    foreground="white",
    font=("Arial",10,"bold")
)

#FUNCIONES

def actualizar_tabla():

    tabla.delete(*tabla.get_children())

    for libro in listar_libros():

        tabla.insert(
            "",
            tk.END,
            values=(
                libro.isbn,
                libro.titulo,
                libro.categoria,
                libro.editorial,
                libro.autor
            )
        )


def limpiar():

    txtISBN.delete(0, tk.END)
    txtTitulo.delete(0, tk.END)
    txtAnio.delete(0, tk.END)
    txtEdicion.delete(0, tk.END)

    cmbCategoria.set("")
    cmbEditorial.set("")
    cmbAutor.set("")

    txtDescripcion.delete("1.0", tk.END)

#Función para guardar un libro

def guardar():

    guardar_libro(

        txtISBN.get(),
        txtTitulo.get(),
        txtAnio.get(),
        txtEdicion.get(),
        txtDescripcion.get("1.0", tk.END).strip(),
        cmbCategoria.get(),
        cmbEditorial.get(),
        cmbAutor.get()

    )

    actualizar_tabla()
    limpiar()



#TITULO

tk.Label(
    ventana,
    text="GESTIÓN DE LIBROS",
    bg=COLOR_VINO,
    fg="white",
    font=("Arial",18,"bold"),
    pady=10
).pack(fill="x")

#FORMULARIO

frame = tk.Frame(ventana,bg=COLOR_FONDO)
frame.pack(fill="x",padx=15,pady=15)

#Columna izquierda

tk.Label(frame,text="ISBN",bg=COLOR_FONDO).grid(row=0,column=0,sticky="w")
txtISBN=tk.Entry(frame,width=28)
txtISBN.grid(row=0,column=1,padx=5,pady=5)

tk.Label(frame,text="Título",bg=COLOR_FONDO).grid(row=1,column=0,sticky="w")
txtTitulo=tk.Entry(frame,width=28)
txtTitulo.grid(row=1,column=1,padx=5,pady=5)

tk.Label(frame,text="Año",bg=COLOR_FONDO).grid(row=2,column=0,sticky="w")
txtAnio=tk.Entry(frame,width=10)
txtAnio.grid(row=2,column=1,sticky="w",padx=5,pady=5)

tk.Label(frame,text="Edición",bg=COLOR_FONDO).grid(row=3,column=0,sticky="w")
txtEdicion=tk.Entry(frame,width=10)
txtEdicion.grid(row=3,column=1,sticky="w",padx=5,pady=5)

tk.Label(frame,text="Categoría",bg=COLOR_FONDO).grid(row=4,column=0,sticky="w")
cmbCategoria=ttk.Combobox(frame,width=25)
cmbCategoria.grid(row=4,column=1,padx=5,pady=5)

cmbCategoria["values"] = (
    "Novela",
    "Historia",
    "Ciencia",
    "Tecnología"
)

tk.Label(frame,text="Editorial",bg=COLOR_FONDO).grid(row=5,column=0,sticky="w")
cmbEditorial=ttk.Combobox(frame,width=25)
cmbEditorial.grid(row=5,column=1,padx=5,pady=5)

cmbEditorial["values"] = (
    "Santillana",
    "Pearson",
    "Planeta",
    "Anaya"
)

tk.Label(frame,text="Autor",bg=COLOR_FONDO).grid(row=6,column=0,sticky="w")
cmbAutor=ttk.Combobox(frame,width=25)
cmbAutor.grid(row=6,column=1,padx=5,pady=5)

cmbAutor["values"] = (
    "J.K. Rowling",
    "Gabriel García Márquez",
    "Stephen King",
    "Julio Verne"
)

#Columna derecha

tk.Label(frame,text="Descripción",bg=COLOR_FONDO).grid(row=0,column=2,sticky="nw",padx=(30,5))

txtDescripcion=tk.Text(frame,width=40,height=8)
txtDescripcion.grid(row=0,column=3,rowspan=7,padx=5)

#BOTONES

frameBotones=tk.Frame(ventana,bg=COLOR_FONDO)
frameBotones.pack(pady=10)

botones = [

    ("Guardar", "#7B4B3A", guardar),
    ("Modificar", "#8C5B47", None),
    ("Eliminar", "#A63D40", None),
    ("Limpiar", "#C9B79C", limpiar)

]

for texto, color, comando in botones:

    fg = "white"

    if texto == "Limpiar":
        fg = "black"

    tk.Button(
        frameBotones,
        text=texto,
        bg=color,
        fg=fg,
        width=12,
        relief="flat",
        font=("Arial",10,"bold"),
        command=comando
    ).pack(side="left", padx=6)

#TABLA

tabla=ttk.Treeview(
    ventana,
    columns=("ISBN","Titulo","Categoria","Editorial","Autor"),
    show="headings",
    height=12
)

for c in ("ISBN","Titulo","Categoria","Editorial","Autor"):
    tabla.heading(c,text=c)

tabla.column("ISBN",width=120,anchor="center")
tabla.column("Titulo",width=320)
tabla.column("Categoria",width=160,anchor="center")
tabla.column("Editorial",width=180,anchor="center")
tabla.column("Autor",width=180)

tabla.pack(fill="both",expand=True,padx=15,pady=(0,15))

ventana.mainloop()

