class Reserva:
    def __init__(self, id_reserva, lector, libro, fecha_reserva, orden_espera, estado="Activa"):
        self.id_reserva = id_reserva
        self.lector = lector
        self.libro = libro
        self.fecha_reserva = fecha_reserva
        self.orden_espera = orden_espera
        self.estado = estado
