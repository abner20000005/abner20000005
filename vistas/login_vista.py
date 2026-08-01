"""
- Diseña el formulario con cajas de texto para usuario y contraseña.
- Contiene el botón de 'Iniciar Sesión' que invoca la validación en auth_controlador.py.
"""
#Hecho por Sary
import tkinter as tk
from tkinter import ttk, messagebox

from controladores.auth_controlador import validar_usuario


#VENTANA

ventana = tk.Tk()
ventana.title("Biblioteca 360 - Iniciar Sesión")
ventana.geometry("400x400")
ventana.configure(bg="#F4EEE8")
ventana.resizable(False, False)

#ESTILOS

COLOR_FONDO = "#F4EEE8"
COLOR_VINO = "#6D213C"
COLOR_CAFE = "#7B4B3A"

#FUNCIONES

def iniciar_sesion():

    usuario = txtUsuario.get()
    contrasena = txtContrasena.get()

    rol = validar_usuario(usuario, contrasena)

    if rol is None:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        return

    messagebox.showinfo("Bienvenido", "Sesión iniciada como: " + rol)

    
    ventana.destroy()

    


def limpiar():

    txtUsuario.delete(0, tk.END)
    txtContrasena.delete(0, tk.END)


#TITULO

tk.Label(
    ventana,
    text="BIBLIOTECA 360",
    bg=COLOR_VINO,
    fg="white",
    font=("Arial",18,"bold"),
    pady=15
).pack(fill="x")

#FORMULARIO

frame = tk.Frame(ventana,bg=COLOR_FONDO)
frame.pack(pady=40)

tk.Label(frame,text="Usuario",bg=COLOR_FONDO,font=("Arial",11)).grid(row=0,column=0,sticky="w",pady=10)
txtUsuario=tk.Entry(frame,width=25)
txtUsuario.grid(row=0,column=1,padx=10)

tk.Label(frame,text="Contraseña",bg=COLOR_FONDO,font=("Arial",11)).grid(row=1,column=0,sticky="w",pady=10)
txtContrasena=tk.Entry(frame,width=25,show="*")
txtContrasena.grid(row=1,column=1,padx=10)

#BOTONES

frameBotones=tk.Frame(ventana,bg=COLOR_FONDO)
frameBotones.pack(pady=20)

tk.Button(
    frameBotones,
    text="Iniciar Sesión",
    bg=COLOR_CAFE,
    fg="white",
    width=14,
    relief="flat",
    font=("Arial",10,"bold"),
    command=iniciar_sesion
).pack(side="left", padx=6)

tk.Button(
    frameBotones,
    text="Limpiar",
    bg="#C9B79C",
    fg="black",
    width=14,
    relief="flat",
    font=("Arial",10,"bold"),
    command=limpiar
).pack(side="left", padx=6)

ventana.mainloop()
