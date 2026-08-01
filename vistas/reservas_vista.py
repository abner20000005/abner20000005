import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from controladores.reservas_controlador import (
    listar_reservas_db, guardar_reserva_db, 
    cancelar_reserva_db, eliminar_reserva_db
)

# Estilos estandarizados del proyecto
COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"
COLOR_CAFE_CLARO = "#8C5B47"
COLOR_ROJO = "#A63D40"
COLOR_BEIGE = "#C9B79C"


class ReservasVista(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.pack(fill="both", expand=True)

        self.configurar_estilos()
        self.crear_interfaz()
        self.actualizar_tabla()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", background=COLOR_VINO, foreground="white", font=("Arial", 10, "bold"))

    def crear_interfaz(self):
        # Título
        tk.Label(
            self, text="GESTIÓN DE RESERVAS", bg=COLOR_VINO, fg="white", 
            font=("Arial", 18, "bold"), pady=10
        ).pack(fill="x")

        # Formulario
        frame = tk.Frame(self, bg=COLOR_FONDO)
        frame.pack(fill="x", padx=15, pady=15)

        # Columna Izquierda
        tk.Label(frame, text="Lector", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w")
        self.cmbLector = ttk.Combobox(frame, width=25)
        self.cmbLector.grid(row=0, column=1, padx=5, pady=5)
        self.cmbLector["values"] = ("Lector 1", "Lector 2", "Lector 3")

        tk.Label(frame, text="Libro", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w")
        self.cmbLibro = ttk.Combobox(frame, width=25)
        self.cmbLibro.grid(row=1, column=1, padx=5, pady=5)
        self.cmbLibro["values"] = ("Libro 1", "Libro 2", "Libro 3")

        tk.Label(frame, text="Fecha Reserva", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w")
        self.txtFecha = tk.Entry(frame, width=15)
        self.txtFecha.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.txtFecha.insert(0, str(date.today()))
        self.txtFecha.config(state="readonly")

        tk.Label(frame, text="Orden de Espera", bg=COLOR_FONDO).grid(row=3, column=0, sticky="w")
        self.txtOrden = tk.Entry(frame, width=10)
        self.txtOrden.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.txtOrden.config(state="readonly")

        tk.Label(frame, text="Estado", bg=COLOR_FONDO).grid(row=4, column=0, sticky="w")
        self.txtEstado = tk.Entry(frame, width=15)
        self.txtEstado.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.txtEstado.insert(0, "Activa")
        self.txtEstado.config(state="readonly")

        # Columna Derecha
        tk.Label(frame, text="Disponibilidad", bg=COLOR_FONDO).grid(row=0, column=2, sticky="nw", padx=(30, 5))
        self.txtDisponibilidad = tk.Text(frame, width=40, height=8)
        self.txtDisponibilidad.grid(row=0, column=3, rowspan=7, padx=5)
        self.txtDisponibilidad.config(state="disabled")

        # Botones
        frameBotones = tk.Frame(self, bg=COLOR_FONDO)
        frameBotones.pack(pady=10)

        botones = [
            ("Guardar", COLOR_CAFE, self.guardar),
            ("Cancelar Reserva", COLOR_CAFE_CLARO, self.cancelar),
            ("Eliminar", COLOR_ROJO, self.eliminar),
            ("Limpiar", COLOR_BEIGE, self.limpiar)
        ]

        for texto, color, comando in botones:
            fg = "black" if texto == "Limpiar" else "white"
            tk.Button(
                frameBotones, text=texto, bg=color, fg=fg, width=14, relief="flat",
                font=("Arial", 10, "bold"), command=comando, cursor="hand2"
            ).pack(side="left", padx=6)

        # Tabla
        self.tabla = ttk.Treeview(
            self, columns=("ID", "Lector", "Libro", "Fecha", "Orden", "Estado"),
            show="headings", height=10
        )

        for c in ("ID", "Lector", "Libro", "Fecha", "Orden", "Estado"):
            self.tabla.heading(c, text=c)

        self.tabla.column("ID", width=60, anchor="center")
        self.tabla.column("Lector", width=200)
        self.tabla.column("Libro", width=250)
        self.tabla.column("Fecha", width=120, anchor="center")
        self.tabla.column("Orden", width=100, anchor="center")
        self.tabla.column("Estado", width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # Métodos de la vista
    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for r in listar_reservas_db():
            self.tabla.insert("", "end", values=(
                r.id_reserva, r.lector, r.libro, r.fecha_reserva, r.orden_espera, r.estado
            ))

    def limpiar(self):
        self.cmbLector.set("")
        self.cmbLibro.set("")

        self.txtFecha.config(state="normal")
        self.txtFecha.delete(0, tk.END)
        self.txtFecha.insert(0, str(date.today()))
        self.txtFecha.config(state="readonly")

        self.txtOrden.config(state="normal")
        self.txtOrden.delete(0, tk.END)
        self.txtOrden.config(state="readonly")

        self.txtDisponibilidad.config(state="normal")
        self.txtDisponibilidad.delete("1.0", tk.END)
        self.txtDisponibilidad.config(state="disabled")

    def guardar(self):
        if not self.cmbLector.get() or not self.cmbLibro.get():
            messagebox.showwarning("Campos Vacíos", "Seleccione un lector y un libro.")
            return

        if guardar_reserva_db(self.cmbLector.get(), self.cmbLibro.get(), self.txtFecha.get()):
            messagebox.showinfo("Éxito", "Reserva registrada.")
            self.actualizar_tabla()
            self.limpiar()

    def cancelar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una reserva de la tabla.")
            return

        id_reserva = self.tabla.item(seleccion[0])["values"][0]
        if cancelar_reserva_db(id_reserva):
            messagebox.showinfo("Éxito", "Reserva cancelada.")
            self.actualizar_tabla()

    def eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una reserva de la tabla.")
            return

        id_reserva = self.tabla.item(seleccion[0])["values"][0]
        if eliminar_reserva_db(id_reserva):
            messagebox.showinfo("Éxito", "Reserva eliminada.")
            self.actualizar_tabla()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Biblioteca 360 - Gestión de Reservas")
    root.geometry("1000x650")
    app = ReservasVista(root)
    root.mainloop()