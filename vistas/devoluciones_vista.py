"""
- Interfaz para buscar y seleccionar préstamos activos por lector o ejemplar.
- Evaluación e ingreso del estado físico del ejemplar retornado.
- Muestra el cálculo automático de días de retraso y multas generadas si la entrega es fuera de tiempo.
"""

import tkinter as tk
from tkinter import ttk, messagebox

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"
COLOR_CAFE_CLARO = "#8C5B47"
COLOR_ROJO = "#A63D40"
COLOR_BEIGE = "#C9B79C"
COLOR_TEXTO = "#2E2E2E"
COLOR_BLANCO = "#FFFFFF"

FUENTE_TITULO = ("Arial", 18, "bold")
FUENTE_SUBTITULO = ("Arial", 11, "bold")
FUENTE_TEXTO = ("Arial", 10)
FUENTE_BOTON = ("Arial", 10, "bold")


class DevolucionesVista(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.pack(fill="both", expand=True)

        self.configurar_estilos_ttk()
        self.crear_interfaz()

    def configurar_estilos_ttk(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading",
                        background=COLOR_VINO,
                        foreground=COLOR_BLANCO,
                        font=("Arial", 10, "bold"),
                        relief="flat")
        style.configure("Treeview",
                        background=COLOR_BLANCO,
                        foreground=COLOR_TEXTO,
                        fieldbackground=COLOR_BLANCO,
                        rowheight=25,
                        font=FUENTE_TEXTO)
        style.map("Treeview", background=[("selected", COLOR_BEIGE)])

    def crear_interfaz(self):
        header = tk.Frame(self, bg=COLOR_VINO, height=50)
        header.pack(fill="x", side="top")
        lbl_titulo = tk.Label(header, text="GESTIÓN DE DEVOLUCIONES", 
                              fg=COLOR_BLANCO, bg=COLOR_VINO, font=FUENTE_TITULO)
        lbl_titulo.pack(pady=10)

        body = tk.Frame(self, bg=COLOR_FONDO)
        body.pack(fill="both", expand=True, padx=25, pady=15)

        frame_form = tk.LabelFrame(body, text=" Detalle de Devolución ", bg=COLOR_FONDO, 
                                   fg=COLOR_VINO, font=FUENTE_SUBTITULO, padx=15, pady=10)
        frame_form.pack(fill="x", pady=5)

        tk.Label(frame_form, text="Estado Físico del Ejemplar:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_TEXTO).grid(row=0, column=0, sticky="w", pady=5)
        self.combo_estado = ttk.Combobox(frame_form, values=["Bueno", "Regular", "Dañado"], state="readonly", font=FUENTE_TEXTO)
        self.combo_estado.current(0)
        self.combo_estado.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame_form, text="Días de Retraso:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_TEXTO).grid(row=1, column=0, sticky="w", pady=5)
        self.lbl_dias = tk.Label(frame_form, text="0 días", font=FUENTE_SUBTITULO, fg=COLOR_ROJO, bg=COLOR_FONDO)
        self.lbl_dias.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame_form, text="Multa Calculada:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_TEXTO).grid(row=2, column=0, sticky="w", pady=5)
        self.lbl_multa = tk.Label(frame_form, text="L. 0.00", font=FUENTE_SUBTITULO, fg=COLOR_ROJO, bg=COLOR_FONDO)
        self.lbl_multa.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        frame_botones = tk.Frame(body, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)

        btn_guardar = tk.Button(frame_botones, text="Procesar", bg=COLOR_CAFE, fg=COLOR_BLANCO,
                                font=FUENTE_BOTON, width=15, bd=0, cursor="hand2")
        btn_guardar.pack(side="left", padx=5)

        btn_limpiar = tk.Button(frame_botones, text="Limpiar", bg=COLOR_BEIGE, fg=COLOR_TEXTO,
                                font=FUENTE_BOTON, width=15, bd=0, cursor="hand2")
        btn_limpiar.pack(side="left", padx=5)

        tk.Label(body, text="Préstamos Pendientes:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_SUBTITULO).pack(anchor="w", pady=(10, 5))

        columns = ("ID Préstamo", "Lector", "Código Libro", "F. Préstamo", "F. Límite")
        self.tabla = ttk.Treeview(body, columns=columns, show="headings", height=7)
        
        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")
            
        self.tabla.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Biblioteca 360 - Devoluciones")
    root.geometry("850x550")
    app = DevolucionesVista(root)
    root.mainloop()