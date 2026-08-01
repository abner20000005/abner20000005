"""
- Representa las entidades 'Sanciones', 'Devoluciones' y 'PagosMultas'.
- Atributos: id_sancion, motivo, monto, estado y la relación con devoluciones atrasadas.
- Mantiene la estructura de penalizaciones y pagos pendientes.
"""
class Sancion:
    # Se ajustan los atributos a las columnas exactas de la tabla Sanciones
    def __init__(self, id_sancion, id_lector, motivo, monto, estado="Pendiente"):
        self.id_sancion = id_sancion
        self.id_lector = id_lector      
        self.motivo = motivo            
        self.monto = monto              
        self.estado = estado            

    def __str__(self):
        return f"Sanción {self.id_sancion} | Lector: {self.id_lector} | Motivo: {self.motivo} | Monto: L.{self.monto} | Estado: {self.estado}"