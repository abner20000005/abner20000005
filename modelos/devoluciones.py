"""
Mapea la tabla Devoluciones de la base de datos
"""

class Devolucion:
    def __init__(self, id_devolucion=None, fecha_devolucion=None, dias_retraso=0, multa=0.0, id_prestamo=None):
        self.id_devolucion = id_devolucion
        self.fecha_devolucion = fecha_devolucion
        self.dias_retraso = dias_retraso
        self.multa = multa
        self.id_prestamo = id_prestamo