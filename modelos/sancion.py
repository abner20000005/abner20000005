"""
- Representa las entidades 'Sanciones', 'Devoluciones' y 'PagosMultas'.
- Atributos: id_sancion, motivo, monto, estado y la relación con devoluciones atrasadas.
- Mantiene la estructura de penalizaciones y pagos pendientes.
"""
class Sancion:
    def __init__(self, id_sancion, id_lector, motivo, monto, estado="Pendiente", id_devolucion=None):
        self.id_sancion = id_sancion
        self.id_lector = id_lector      # ID del estudiante/usuario
        self.motivo = motivo            # 'Retraso', 'Daño', 'Pérdida'
        self.monto = monto              # Cantidad a pagar (float)
        self.estado = estado            # 'Pendiente' o 'Pagado'
        self.id_devolucion = id_devolucion # Para saber de qué préstamo viene la multa