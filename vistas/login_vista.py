"""
- Diseña el formulario con cajas de texto para usuario y contraseña.
- Contiene el botón de 'Iniciar Sesión' que invoca la validación en auth_controlador.py.
"""

import tkinter as tk 

ventana1 = tk.Tk()

ventana1.title("Estructurada 2 - Unicah")
ventana1.geometry("500x500")
ventana1.configure(bg="blue")

texto1=tk.Entry(ventana1)
texto1.pack(pady=40)

texto2=tk.Entry(ventana1)
texto2.pack(pady=20) 

boton1=tk.Button(ventana1, text="LOGIN")
boton1.pack(pady=30)

ventana1.mainloop()
