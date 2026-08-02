import tkinter as tk
from tkinter import ttk

# Colores
COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"
COLOR_CAFE_CLARO = "#8C5B47"
COLOR_ROJO = "#A63D40"
COLOR_BEIGE = "#C9B79C"
COLOR_TEXTO = "#2E2E2E"
COLOR_BLANCO = "#FFFFFF"


class VentanaLectores:

    def __init__(self):

        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Lectores")
        self.ventana.geometry("850x600")
        self.ventana.configure(bg=COLOR_FONDO)

        # ========= TÍTULO =========
        titulo = tk.Label(
            self.ventana,
            text="Gestión de Lectores",
            font=("Arial", 18, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_VINO
        )
        titulo.pack(pady=15)

        # ========= FORMULARIO =========
        formulario = tk.Frame(
            self.ventana,
            bg=COLOR_FONDO
        )
        formulario.pack()

        # Nombre
        tk.Label(
            formulario,
            text="Nombre:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.nombre = tk.Entry(formulario, width=30)
        self.nombre.grid(row=0, column=1)

        # Identidad
        tk.Label(
            formulario,
            text="Identidad:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.identidad = tk.Entry(formulario, width=30)
        self.identidad.grid(row=1, column=1)

        # Teléfono
        tk.Label(
            formulario,
            text="Teléfono:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.telefono = tk.Entry(formulario, width=30)
        self.telefono.grid(row=2, column=1)

        # Correo
        tk.Label(
            formulario,
            text="Correo:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.correo = tk.Entry(formulario, width=30)
        self.correo.grid(row=3, column=1)

        # Tipo de lector
        tk.Label(
            formulario,
            text="Tipo:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.tipo = ttk.Combobox(
            formulario,
            values=["Estudiante", "Docente", "Administrativo", "Otro"],
            state="readonly",
            width=27
        )
        self.tipo.grid(row=4, column=1)

        # Estado
        tk.Label(
            formulario,
            text="Estado:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.estado = ttk.Combobox(
            formulario,
            values=["Activo", "Inactivo"],
            state="readonly",
            width=27
        )
        self.estado.grid(row=5, column=1)

        # ========= BOTONES =========
        botones = tk.Frame(self.ventana, bg=COLOR_FONDO)
        botones.pack(pady=20)

        tk.Button(
            botones,
            text="Guardar",
            bg=COLOR_CAFE,
            fg=COLOR_BLANCO,
            width=12
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            botones,
            text="Editar",
            bg=COLOR_CAFE_CLARO,
            fg=COLOR_BLANCO,
            width=12
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            botones,
            text="Eliminar",
            bg=COLOR_ROJO,
            fg=COLOR_BLANCO,
            width=12
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            botones,
            text="Limpiar",
            bg=COLOR_BEIGE,
            fg=COLOR_TEXTO,
            width=12
        ).grid(row=0, column=3, padx=5)

        # ========= TABLA =========
        self.tabla = ttk.Treeview(
            self.ventana,
            columns=("Nombre", "Identidad", "Teléfono", "Tipo", "Estado"),
            show="headings",
            height=10
        )

        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Identidad", text="Identidad")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("Nombre", width=180)
        self.tabla.column("Identidad", width=150)
        self.tabla.column("Teléfono", width=120)
        self.tabla.column("Tipo", width=120)
        self.tabla.column("Estado", width=100)

        self.tabla.pack(padx=20, pady=15, fill="both", expand=True)

        self.ventana.mainloop()


if __name__ == "__main__":
    VentanaLectores()
