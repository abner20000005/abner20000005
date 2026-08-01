import tkinter as tk
from tkinter import ttk
from datetime import date


def guardar_reserva(*args): pass
def listar_reservas(): return []
def cancelar_reserva(id_reserva): pass
def eliminar_reserva(id_reserva): pass


class ReservasVista(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F4EEE8")
        self.pack(fill="both", expand=True)

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        COLOR_VINO = "#6D213C"
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=25,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=COLOR_VINO,
            foreground="white",
            font=("Arial", 10, "bold")
        )

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())

        for reserva in listar_reservas():
            self.tabla.insert(
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
        guardar_reserva(
            self.cmbLector.get(),
            self.cmbLibro.get(),
            self.txtFecha.get()
        )
        self.actualizar_tabla()
        self.limpiar()

    def cancelar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        id_reserva = self.tabla.item(seleccion[0])["values"][0]
        cancelar_reserva(id_reserva)
        self.actualizar_tabla()

    def eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        id_reserva = self.tabla.item(seleccion[0])["values"][0]
        eliminar_reserva(id_reserva)
        self.actualizar_tabla()

    def crear_interfaz(self):
        COLOR_FONDO = "#F4EEE8"
        COLOR_VINO = "#6D213C"

        # TITULO
        tk.Label(
            self,
            text="GESTIÓN DE RESERVAS",
            bg=COLOR_VINO,
            fg="white",
            font=("Arial", 18, "bold"),
            pady=10
        ).pack(fill="x")

        # FORMULARIO
        frame = tk.Frame(self, bg=COLOR_FONDO)
        frame.pack(fill="x", padx=15, pady=15)

        # Columna izquierda
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

        # Columna derecha
        tk.Label(frame, text="Disponibilidad", bg=COLOR_FONDO).grid(row=0, column=2, sticky="nw", padx=(30, 5))
        self.txtDisponibilidad = tk.Text(frame, width=40, height=8)
        self.txtDisponibilidad.grid(row=0, column=3, rowspan=7, padx=5)
        self.txtDisponibilidad.config(state="disabled")

        # BOTONES
        frameBotones = tk.Frame(self, bg=COLOR_FONDO)
        frameBotones.pack(pady=10)

        botones = [
            ("Guardar", "#7B4B3A", self.guardar),
            ("Cancelar Reserva", "#8C5B47", self.cancelar),
            ("Eliminar", "#A63D40", self.eliminar),
            ("Limpiar", "#C9B79C", self.limpiar)
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
                font=("Arial", 10, "bold"),
                command=comando
            ).pack(side="left", padx=6)

        # TABLA
        self.tabla = ttk.Treeview(
            self,
            columns=("ID", "Lector", "Libro", "Fecha", "Orden", "Estado"),
            show="headings",
            height=12
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


# EJECUCIÓN DIRECTA
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Biblioteca 360 - Gestión de Reservas")
    ventana.geometry("1000x650")
    ventana.configure(bg="#F4EEE8")
    ventana.resizable(False, False)
    app = ReservasVista(ventana)
    ventana.mainloop()