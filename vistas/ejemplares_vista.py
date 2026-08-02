import tkinter as tk
from tkinter import ttk
from ejemplares_vista import EjemplarControlador

# Colores
COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"
COLOR_CAFE_CLARO = "#8C5B47"
COLOR_ROJO = "#A63D40"
COLOR_BEIGE = "#C9B79C"
COLOR_TEXTO = "#2E2E2E"
COLOR_BLANCO = "#FFFFFF"


class VentanaEjemplares:

    def __init__(self):

        self.controlador = EjemplarControlador()

        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Ejemplares")
        self.ventana.geometry("700x550")
        self.ventana.configure(bg=COLOR_FONDO)

        # Título
        titulo = tk.Label(
            self.ventana,
            text="Gestión de Ejemplares",
            font=("Arial", 18, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_VINO
        )
        titulo.pack(pady=15)

        # Código interno
        tk.Label(self.ventana, text="Código Interno:", bg=COLOR_FONDO).pack()
        self.codigo = tk.Entry(self.ventana, width=35)
        self.codigo.pack()

        # Libro
        tk.Label(self.ventana, text="ID del Libro:", bg=COLOR_FONDO).pack()
        self.libro = tk.Entry(self.ventana, width=35)
        self.libro.pack()

        # Estado
        tk.Label(self.ventana, text="Estado Físico:", bg=COLOR_FONDO).pack()

        self.estado = ttk.Combobox(
            self.ventana,
            values=["Bueno", "Regular", "Dañado"],
            state="readonly",
            width=32
        )
        self.estado.pack()

        # Ubicación
        tk.Label(self.ventana, text="Ubicación:", bg=COLOR_FONDO).pack()
        self.ubicacion = tk.Entry(self.ventana, width=35)
        self.ubicacion.pack()

        # Disponible
        self.disponible = tk.BooleanVar()
        self.disponible.set(True)

        tk.Checkbutton(
            self.ventana,
            text="Disponible",
            variable=self.disponible,
            bg=COLOR_FONDO
        ).pack(pady=10)

        # Fecha
        tk.Label(self.ventana, text="Fecha de Adquisición:", bg=COLOR_FONDO).pack()
        self.fecha = tk.Entry(self.ventana, width=35)
        self.fecha.pack()

        # Botón guardar
        boton = tk.Button(
            self.ventana,
            text="Guardar",
            bg=COLOR_CAFE,
            fg=COLOR_BLANCO,
            width=15,
            command=self.guardar
        )
        boton.pack(pady=15)

        # Tabla
        self.tabla = ttk.Treeview(
            self.ventana,
            columns=("codigo", "libro", "estado"),
            show="headings",
            height=8
        )

        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("libro", text="Libro")
        self.tabla.heading("estado", text="Estado")

        self.tabla.pack(pady=10)

        self.ventana.mainloop()


    def guardar(self):

        self.controlador.agregar_ejemplar(
            self.codigo.get(),
            self.libro.get(),
            self.estado.get(),
            self.ubicacion.get(),
            self.disponible.get(),
            self.fecha.get()
        )

        self.actualizar_tabla()

        self.codigo.delete(0, tk.END)
        self.libro.delete(0, tk.END)
        self.estado.set("")
        self.ubicacion.delete(0, tk.END)
        self.fecha.delete(0, tk.END)


    def actualizar_tabla(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for ejemplar in self.controlador.obtener_ejemplares():

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    ejemplar.codigo_interno,
                    ejemplar.libro_id,
                    ejemplar.estado_fisico
                )
            )


if __name__ == "__main__":
    VentanaEjemplares()