import tkinter as tk
from tkinter import ttk, messagebox
from controladores.categorias_controlador import *
from controladores.editoriales_controlador import *

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"

def abrir_editoriales_categorias():
    ventana = tk.Toplevel()
    ventana.title("Biblioteca 360 - Editoriales y Categorías")
    ventana.geometry("1000x620")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=24, font=("Arial", 10))
    style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    # ========== CATEGORÍAS ==========
    id_cat = None

    def actualizar_cat():
        tabla_cat.delete(*tabla_cat.get_children())
        for c in listar_categorias():
            tabla_cat.insert("", tk.END, values=(c.id_categoria, c.nombre, c.descripcion))

    def limpiar_cat():
        nonlocal id_cat
        txtCatNombre.delete(0, tk.END)
        txtCatDesc.delete(0, tk.END)
        id_cat = None

    def guardar_cat():
        if not txtCatNombre.get().strip():
            messagebox.showerror("Error", "Debe ingresar el nombre de la categoría.")
            return
        if guardar_categoria(txtCatNombre.get().strip(), txtCatDesc.get().strip()):
            actualizar_cat()
            limpiar_cat()
            messagebox.showinfo("Éxito", "Categoría guardada.")
        else:
            messagebox.showerror("Error", "No se pudo guardar.")

    def seleccionar_cat(event):
        nonlocal id_cat
        sel = tabla_cat.selection()
        if not sel:
            return
        vals = tabla_cat.item(sel[0])["values"]
        id_cat = vals[0]
        txtCatNombre.delete(0, tk.END)
        txtCatNombre.insert(0, vals[1])
        txtCatDesc.delete(0, tk.END)
        txtCatDesc.insert(0, vals[2])

    def modificar_cat():
        if id_cat is None:
            messagebox.showwarning("Aviso", "Seleccione una categoría.")
            return
        if not txtCatNombre.get().strip():
            messagebox.showerror("Error", "Debe ingresar el nombre.")
            return
        if modificar_categoria(id_cat, txtCatNombre.get().strip(), txtCatDesc.get().strip()):
            actualizar_cat()
            limpiar_cat()
            messagebox.showinfo("Éxito", "Categoría modificada.")

    def eliminar_cat():
        if id_cat is None:
            messagebox.showwarning("Aviso", "Seleccione una categoría.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar categoría?"):
            return
        res = eliminar_categoria(id_cat)
        if res == "relacionado":
            messagebox.showerror("Error", "No se puede eliminar. Tiene libros asociados.")
        elif res:
            actualizar_cat()
            limpiar_cat()
            messagebox.showinfo("Éxito", "Categoría eliminada.")

    # ========== EDITORIALES ==========
    id_edi = None

    def actualizar_edi():
        tabla_edi.delete(*tabla_edi.get_children())
        for e in listar_editoriales():
            tabla_edi.insert("", tk.END, values=(e.id_editorial, e.nombre, e.pais, e.telefono))

    def limpiar_edi():
        nonlocal id_edi
        txtEdiNombre.delete(0, tk.END)
        txtEdiPais.delete(0, tk.END)
        txtEdiTel.delete(0, tk.END)
        id_edi = None

    def guardar_edi():
        if not txtEdiNombre.get().strip():
            messagebox.showerror("Error", "Debe ingresar el nombre de la editorial.")
            return
        if guardar_editorial(txtEdiNombre.get().strip(), txtEdiPais.get().strip(), txtEdiTel.get().strip()):
            actualizar_edi()
            limpiar_edi()
            messagebox.showinfo("Éxito", "Editorial guardada.")
        else:
            messagebox.showerror("Error", "No se pudo guardar.")

    def seleccionar_edi(event):
        nonlocal id_edi
        sel = tabla_edi.selection()
        if not sel:
            return
        vals = tabla_edi.item(sel[0])["values"]
        id_edi = vals[0]
        txtEdiNombre.delete(0, tk.END)
        txtEdiNombre.insert(0, vals[1])
        txtEdiPais.delete(0, tk.END)
        txtEdiPais.insert(0, vals[2])
        txtEdiTel.delete(0, tk.END)
        txtEdiTel.insert(0, vals[3])

    def modificar_edi():
        if id_edi is None:
            messagebox.showwarning("Aviso", "Seleccione una editorial.")
            return
        if not txtEdiNombre.get().strip():
            messagebox.showerror("Error", "Debe ingresar el nombre.")
            return
        if modificar_editorial(id_edi, txtEdiNombre.get().strip(), txtEdiPais.get().strip(), txtEdiTel.get().strip()):
            actualizar_edi()
            limpiar_edi()
            messagebox.showinfo("Éxito", "Editorial modificada.")

    def eliminar_edi():
        if id_edi is None:
            messagebox.showwarning("Aviso", "Seleccione una editorial.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar editorial?"):
            return
        res = eliminar_editorial(id_edi)
        if res == "relacionado":
            messagebox.showerror("Error", "No se puede eliminar. Tiene libros asociados.")
        elif res:
            actualizar_edi()
            limpiar_edi()
            messagebox.showinfo("Éxito", "Editorial eliminada.")

    # ========== INTERFAZ ==========
    tk.Label(ventana, text="EDITORIALES Y CATEGORÍAS", bg=COLOR_VINO, fg="white",
             font=("Arial", 16, "bold"), pady=8).pack(fill="x")

    contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    # ----- Izquierda: Categorías -----
    frame_cat = tk.LabelFrame(contenedor, text="Categorías", bg=COLOR_FONDO, font=("Arial", 11, "bold"))
    frame_cat.pack(side="left", fill="both", expand=True, padx=5)

    f1 = tk.Frame(frame_cat, bg=COLOR_FONDO)
    f1.pack(fill="x", padx=8, pady=5)
    tk.Label(f1, text="Nombre:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w")
    txtCatNombre = tk.Entry(f1, width=28)
    txtCatNombre.grid(row=0, column=1, padx=5, pady=3)
    tk.Label(f1, text="Descripción:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w")
    txtCatDesc = tk.Entry(f1, width=28)
    txtCatDesc.grid(row=1, column=1, padx=5, pady=3)

    fb1 = tk.Frame(frame_cat, bg=COLOR_FONDO)
    fb1.pack(pady=5)
    for txt, cmd, col in [("Guardar", guardar_cat, "#7B4B3A"), ("Modificar", modificar_cat, "#8C5B47"),
                          ("Eliminar", eliminar_cat, "#A63D40"), ("Limpiar", limpiar_cat, "#C9B79C")]:
        fg = "black" if txt == "Limpiar" else "white"
        tk.Button(fb1, text=txt, bg=col, fg=fg, width=9, relief="flat",
                  font=("Arial", 9, "bold"), command=cmd).pack(side="left", padx=3)

    tabla_cat = ttk.Treeview(frame_cat, columns=("ID", "Nombre", "Descripcion"), show="headings", height=12)
    tabla_cat.heading("ID", text="ID")
    tabla_cat.heading("Nombre", text="Nombre")
    tabla_cat.heading("Descripcion", text="Descripción")
    tabla_cat.column("ID", width=40, anchor="center")
    tabla_cat.column("Nombre", width=140)
    tabla_cat.column("Descripcion", width=180)
    tabla_cat.pack(fill="both", expand=True, padx=8, pady=5)
    tabla_cat.bind("<<TreeviewSelect>>", seleccionar_cat)

    # ----- Derecha: Editoriales -----
    frame_edi = tk.LabelFrame(contenedor, text="Editoriales", bg=COLOR_FONDO, font=("Arial", 11, "bold"))
    frame_edi.pack(side="right", fill="both", expand=True, padx=5)

    f2 = tk.Frame(frame_edi, bg=COLOR_FONDO)
    f2.pack(fill="x", padx=8, pady=5)
    tk.Label(f2, text="Nombre:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w")
    txtEdiNombre = tk.Entry(f2, width=28)
    txtEdiNombre.grid(row=0, column=1, padx=5, pady=3)
    tk.Label(f2, text="País:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w")
    txtEdiPais = tk.Entry(f2, width=28)
    txtEdiPais.grid(row=1, column=1, padx=5, pady=3)
    tk.Label(f2, text="Teléfono:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w")
    txtEdiTel = tk.Entry(f2, width=28)
    txtEdiTel.grid(row=2, column=1, padx=5, pady=3)

    fb2 = tk.Frame(frame_edi, bg=COLOR_FONDO)
    fb2.pack(pady=5)
    for txt, cmd, col in [("Guardar", guardar_edi, "#7B4B3A"), ("Modificar", modificar_edi, "#8C5B47"),
                          ("Eliminar", eliminar_edi, "#A63D40"), ("Limpiar", limpiar_edi, "#C9B79C")]:
        fg = "black" if txt == "Limpiar" else "white"
        tk.Button(fb2, text=txt, bg=col, fg=fg, width=9, relief="flat",
                  font=("Arial", 9, "bold"), command=cmd).pack(side="left", padx=3)

    tabla_edi = ttk.Treeview(frame_edi, columns=("ID", "Nombre", "Pais", "Telefono"), show="headings", height=12)
    tabla_edi.heading("ID", text="ID")
    tabla_edi.heading("Nombre", text="Nombre")
    tabla_edi.heading("Pais", text="País")
    tabla_edi.heading("Telefono", text="Teléfono")
    tabla_edi.column("ID", width=40, anchor="center")
    tabla_edi.column("Nombre", width=140)
    tabla_edi.column("Pais", width=100, anchor="center")
    tabla_edi.column("Telefono", width=100, anchor="center")
    tabla_edi.pack(fill="both", expand=True, padx=8, pady=5)
    tabla_edi.bind("<<TreeviewSelect>>", seleccionar_edi)

    actualizar_cat()
    actualizar_edi()