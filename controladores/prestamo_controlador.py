"""
- Registra nuevos préstamos verificando previamente la disponibilidad del ejemplar y el límite del lector.
- Procesa devoluciones, actualizando el estado del ejemplar a disponible.
"""
from datetime import date, timedelta


class Ejemplar:
    def __init__(self, id_ejemplar, isbn):
        self.id_ejemplar = id_ejemplar
        self.isbn = isbn
        self.estado = "disponible"



class Prestamo:
    def __init__(self, id_prestamo, id_lector, ejemplar):
        self.id_prestamo = id_prestamo
        self.id_lector = id_lector
        self.ejemplar = ejemplar
        self.fecha_prestamo = date.today()
        self.fecha_limite = self.fecha_prestamo + timedelta(days=7)
        self.estado = "activo"


prestamos = []


MAX_PRESTAMOS = 3



def contar_prestamos(id_lector):
    contador = 0
    for p in prestamos:
        if p.id_lector == id_lector and p.estado == "activo":
            contador += 1
    return contador



def registrar_prestamo(id_lector, ejemplar):


    if ejemplar.estado != "disponible":
        print("no se puede prestar, ya esta ocupado")
        return

    
    if contar_prestamos(id_lector) >= MAX_PRESTAMOS:
        print("el lector ya tiene muchos prestamos")
        return

    nuevo = Prestamo(len(prestamos)+1, id_lector, ejemplar)
    prestamos.append(nuevo)

    
    ejemplar.estado = "prestado"

    print("prestamo hecho ")



def devolver_libro(id_prestamo):

    for p in prestamos:
        if p.id_prestamo == id_prestamo and p.estado == "activo":
            p.estado = "devuelto"
            p.ejemplar.estado = "disponible"
            print("libro devuelto ")
            return

    print("no se encontro el prestamo")