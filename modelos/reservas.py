import tkinter as tk
from tkinter import ttk
from datetime import date

import tkinter as tk
from tkinter import ttk
from datetime import date

def guardar_reserva(*args): pass
def listar_reservas(): return []
def cancelar_reserva(id_reserva): pass
def eliminar_reserva(id_reserva): pass


#VENTANA

ventana = tk.Tk()
ventana.title("Biblioteca 360 - Gestión de Reservas")




#VENTANA

ventana = tk.Tk()
ventana.title("Biblioteca 360 - Gestión de Reservas")
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

    for reserva in listar_reservas():

        tabla.insert(
            "",
            tk.END,
            values=(
                reserva.id_reserva,
                reserva.lector,
                reserva.libro,
                reserva.fecha_reserva,
                reserva.orden_espera,
                reserva.estado
            )
        )


def limpiar():

    cmbLector.set("")
    cmbLibro.set("")

    txtFecha.config(state="normal")
    txtFecha.delete(0, tk.END)
    txtFecha.insert(0, str(date.today()))
    txtFecha.config(state="readonly")

    txtOrden.config(state="normal")
    txtOrden.delete(0, tk.END)
    txtOrden.config(state="readonly")

    txtDisponibilidad.config(state="normal")
    txtDisponibilidad.delete("1.0", tk.END)
    txtDisponibilidad.config(state="disabled")


#Función para guardar una reserva

def guardar():

    guardar_reserva(

        cmbLector.get(),
        cmbLibro.get(),
        txtFecha.get()

    )

    actualizar_tabla()
    limpiar()


#Función para cancelar la reserva seleccionada

def cancelar():

    seleccion = tabla.selection()

    if not seleccion:
        return

    id_reserva = tabla.item(seleccion[0])["values"][0]

    cancelar_reserva(id_reserva)

    actualizar_tabla()


#Función para eliminar la reserva seleccionada

def eliminar():

    seleccion = tabla.selection()

    if not seleccion:
        return

    id_reserva = tabla.item(seleccion[0])["values"][0]

    eliminar_reserva(id_reserva)

    actualizar_tabla()


#TITULO

tk.Label(
    ventana,
    text="GESTIÓN DE RESERVAS",
    bg=COLOR_VINO,
    fg="white",
    font=("Arial",18,"bold"),
    pady=10
).pack(fill="x")

#FORMULARIO

frame = tk.Frame(ventana,bg=COLOR_FONDO)
frame.pack(fill="x",padx=15,pady=15)

#Columna izquierda

tk.Label(frame,text="Lector",bg=COLOR_FONDO).grid(row=0,column=0,sticky="w")
cmbLector=ttk.Combobox(frame,width=25)
cmbLector.grid(row=0,column=1,padx=5,pady=5)

cmbLector["values"] = (
    "Lector 1",
    "Lector 2",
    "Lector 3"
)

tk.Label(frame,text="Libro",bg=COLOR_FONDO).grid(row=1,column=0,sticky="w")
cmbLibro=ttk.Combobox(frame,width=25)
cmbLibro.grid(row=1,column=1,padx=5,pady=5)

cmbLibro["values"] = (
    "Libro 1",
    "Libro 2",
    "Libro 3"
)

tk.Label(frame,text="Fecha Reserva",bg=COLOR_FONDO).grid(row=2,column=0,sticky="w")
txtFecha=tk.Entry(frame,width=15)
txtFecha.grid(row=2,column=1,sticky="w",padx=5,pady=5)
txtFecha.insert(0, str(date.today()))
txtFecha.config(state="readonly")

tk.Label(frame,text="Orden de Espera",bg=COLOR_FONDO).grid(row=3,column=0,sticky="w")
txtOrden=tk.Entry(frame,width=10)
txtOrden.grid(row=3,column=1,sticky="w",padx=5,pady=5)
txtOrden.config(state="readonly")

tk.Label(frame,text="Estado",bg=COLOR_FONDO).grid(row=4,column=0,sticky="w")
txtEstado=tk.Entry(frame,width=15)
txtEstado.grid(row=4,column=1,sticky="w",padx=5,pady=5)
txtEstado.insert(0,"Activa")
txtEstado.config(state="readonly")

#Columna derecha

tk.Label(frame,text="Disponibilidad",bg=COLOR_FONDO).grid(row=0,column=2,sticky="nw",padx=(30,5))

txtDisponibilidad=tk.Text(frame,width=40,height=8)
txtDisponibilidad.grid(row=0,column=3,rowspan=7,padx=5)
txtDisponibilidad.config(state="disabled")

#BOTONES

frameBotones=tk.Frame(ventana,bg=COLOR_FONDO)
frameBotones.pack(pady=10)

botones = [

    ("Guardar", "#7B4B3A", guardar),
    ("Cancelar Reserva", "#8C5B47", cancelar),
    ("Eliminar", "#A63D40", eliminar),
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
        width=14,
        relief="flat",
        font=("Arial",10,"bold"),
        command=comando
    ).pack(side="left", padx=6)

#TABLA

tabla=ttk.Treeview(
    ventana,
    columns=("ID","Lector","Libro","Fecha","Orden","Estado"),
    show="headings",
    height=12
)

for c in ("ID","Lector","Libro","Fecha","Orden","Estado"):
    tabla.heading(c,text=c)

tabla.column("ID",width=60,anchor="center")
tabla.column("Lector",width=200)
tabla.column("Libro",width=250)
tabla.column("Fecha",width=120,anchor="center")
tabla.column("Orden",width=100,anchor="center")
tabla.column("Estado",width=120,anchor="center")

tabla.pack(fill="both",expand=True,padx=15,pady=(0,15))

ventana.mainloop()
