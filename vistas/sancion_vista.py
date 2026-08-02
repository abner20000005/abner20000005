import tkinter as tk
from tkinter import ttk, messagebox
from controladores.sanciones_controlador import SancionesControlador

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

class SancionesVista:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Sanciones y Pagos")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        
        # Aplicar el color de fondo a la ventana principal
        self.root.configure(bg=COLOR_FONDO)
        
        # Instanciar el controlador
        self.controlador = SancionesControlador()

        # Configurar un poco el estilo de los menús desplegables (Combobox)
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("TCombobox", fieldbackground=COLOR_BLANCO, background=COLOR_BEIGE)

        self.construir_interfaz()

    def construir_interfaz(self):
        # --- TÍTULO PRINCIPAL ---
        lbl_titulo = tk.Label(self.root, text="Gestión de Sanciones", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_VINO)
        lbl_titulo.pack(pady=20)

        # --- SECCIÓN 1: REGISTRO DE PAGOS ---
        # Usamos COLOR_BEIGE como fondo del contenedor para que resalte
        frame_pago = tk.Frame(self.root, bg=COLOR_BEIGE, bd=2, relief="groove")
        frame_pago.pack(padx=25, pady=10, fill="x")

        lbl_sub_pago = tk.Label(frame_pago, text="Registrar Pago de Multa", font=FUENTE_SUBTITULO, bg=COLOR_BEIGE, fg=COLOR_VINO)
        lbl_sub_pago.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame_pago, text="ID de la Sanción:", font=FUENTE_TEXTO, bg=COLOR_BEIGE, fg=COLOR_TEXTO).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_id_sancion = tk.Entry(frame_pago, font=FUENTE_TEXTO, bg=COLOR_BLANCO, fg=COLOR_TEXTO)
        self.entry_id_sancion.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_pago, text="ID del Lector:", font=FUENTE_TEXTO, bg=COLOR_BEIGE, fg=COLOR_TEXTO).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_id_lector_pago = tk.Entry(frame_pago, font=FUENTE_TEXTO, bg=COLOR_BLANCO, fg=COLOR_TEXTO)
        self.entry_id_lector_pago.grid(row=2, column=1, padx=10, pady=5)

        # Botón con colores de la paleta
        btn_pagar = tk.Button(frame_pago, text="Registrar Pago", font=FUENTE_BOTON, bg=COLOR_CAFE, fg=COLOR_BLANCO, 
                              activebackground=COLOR_CAFE_CLARO, activeforeground=COLOR_BLANCO, 
                              relief="flat", cursor="hand2", command=self.procesar_pago)
        btn_pagar.grid(row=3, column=0, columnspan=2, pady=15, ipadx=20, ipady=5)


        # --- SECCIÓN 2: GENERAR SANCIÓN (Daño o Pérdida) ---
        frame_generar = tk.Frame(self.root, bg=COLOR_BEIGE, bd=2, relief="groove")
        frame_generar.pack(padx=25, pady=10, fill="x")

        lbl_sub_sancion = tk.Label(frame_generar, text="Reportar Daño o Pérdida", font=FUENTE_SUBTITULO, bg=COLOR_BEIGE, fg=COLOR_VINO)
        lbl_sub_sancion.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame_generar, text="ID del Lector:", font=FUENTE_TEXTO, bg=COLOR_BEIGE, fg=COLOR_TEXTO).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_id_lector_sancion = tk.Entry(frame_generar, font=FUENTE_TEXTO, bg=COLOR_BLANCO, fg=COLOR_TEXTO)
        self.entry_id_lector_sancion.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_generar, text="Nivel de Daño:", font=FUENTE_TEXTO, bg=COLOR_BEIGE, fg=COLOR_TEXTO).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.combo_danio = ttk.Combobox(frame_generar, values=["leve", "grave", "perdida"], state="readonly", font=FUENTE_TEXTO)
        self.combo_danio.grid(row=2, column=1, padx=10, pady=5)
        self.combo_danio.current(0) # Selecciona 'leve' por defecto

        tk.Label(frame_generar, text="Precio del Libro (L):", font=FUENTE_TEXTO, bg=COLOR_BEIGE, fg=COLOR_TEXTO).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_precio = tk.Entry(frame_generar, font=FUENTE_TEXTO, bg=COLOR_BLANCO, fg=COLOR_TEXTO)
        self.entry_precio.grid(row=3, column=1, padx=10, pady=5)

        # Botón usando COLOR_ROJO para advertir que es una acción de sanción/bloqueo
        btn_generar = tk.Button(frame_generar, text="Generar Sanción y Bloquear", font=FUENTE_BOTON, bg=COLOR_ROJO, fg=COLOR_BLANCO, 
                                activebackground=COLOR_VINO, activeforeground=COLOR_BLANCO, 
                                relief="flat", cursor="hand2", command=self.procesar_sancion)
        btn_generar.grid(row=4, column=0, columnspan=2, pady=15, ipadx=10, ipady=5)


    # --- FUNCIONES DE LOS BOTONES ---

    def procesar_pago(self):
        id_sancion = self.entry_id_sancion.get()
        id_lector = self.entry_id_lector_pago.get()

        if not id_sancion or not id_lector:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa el ID de la sanción y del lector.")
            return

        try:
            exito = self.controlador.registrar_pago(int(id_sancion), int(id_lector))
            if exito:
                messagebox.showinfo("Éxito", "Pago registrado correctamente.\nSe verificó el estado de bloqueo del lector.")
                self.entry_id_sancion.delete(0, tk.END)
                self.entry_id_lector_pago.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo registrar el pago. Verifica los IDs ingresados.")
        except ValueError:
            messagebox.showerror("Error de formato", "Los IDs deben ser números enteros.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar el pago: {e}")

    def procesar_sancion(self):
        id_lector = self.entry_id_lector_sancion.get()
        nivel_danio = self.combo_danio.get()
        precio = self.entry_precio.get()

        if not id_lector or not precio:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa el ID del lector y el precio del libro.")
            return

        try:
            motivo = 'Pérdida' if nivel_danio == 'perdida' else 'Daño'
            self.controlador.generar_sancion(
                id_lector=int(id_lector), 
                motivo=motivo, 
                precio_libro=float(precio), 
                nivel_danio=nivel_danio
            )
            messagebox.showinfo("Sanción Aplicada", f"Se ha generado la multa por {motivo}.\nEl lector ha sido bloqueado temporalmente.")
            
            self.entry_id_lector_sancion.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error de formato", "Verifica que el ID sea número entero y el precio un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar la sanción: {e}")
