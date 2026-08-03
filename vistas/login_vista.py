import tkinter as tk
from tkinter import messagebox
from controladores.auth_controlador import iniciar_sesion
from vistas.menu_principal_vista import abrir_menu

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"

def abrir_login():
    ventana = tk.Tk()
    ventana.title("Biblioteca 360 - Inicio de Sesión")
    ventana.geometry("420x320")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    # Centrar ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - 210
    y = (ventana.winfo_screenheight() // 2) - 160
    ventana.geometry(f"+{x}+{y}")

    tk.Label(ventana, text="BIBLIOTECA 360", bg=COLOR_VINO, fg="white",
             font=("Arial", 18, "bold"), pady=15).pack(fill="x")

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=30)

    tk.Label(frame, text="Usuario:", bg=COLOR_FONDO, font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
    txt_usuario = tk.Entry(frame, width=28, font=("Arial", 11))
    txt_usuario.grid(row=0, column=1, padx=10, pady=8)

    tk.Label(frame, text="Contraseña:", bg=COLOR_FONDO, font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
    txt_clave = tk.Entry(frame, width=28, show="*", font=("Arial", 11))
    txt_clave.grid(row=1, column=1, padx=10, pady=8)

    def login():
        usuario = txt_usuario.get().strip()
        clave = txt_clave.get().strip()

        if not usuario or not clave:
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        user = iniciar_sesion(usuario, clave)
        if user:
            ventana.destroy()
            abrir_menu(user)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    tk.Button(ventana, text="Iniciar Sesión", bg=COLOR_CAFE, fg="white",
              font=("Arial", 11, "bold"), width=18, relief="flat",
              command=login).pack(pady=15)

    txt_usuario.focus()
    ventana.bind("<Return>", lambda e: login())
    ventana.mainloop()