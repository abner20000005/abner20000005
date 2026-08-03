class Prestamo:
    def __init__(self, id_prestamo, fecha_prestamo, fecha_limite, estado,
                 id_lector, lector, id_ejemplar, codigo, libro):
        self.id_prestamo = id_prestamo
        self.fecha_prestamo = fecha_prestamo
        self.fecha_limite = fecha_limite
        self.estado = estado
        self.id_lector = id_lector
        self.lector = lector
        self.id_ejemplar = id_ejemplar
        self.codigo = codigo
        self.libro = libro