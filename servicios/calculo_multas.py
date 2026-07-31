"""
- Compara la fecha límite de devolución con la fecha actual o de devolución.
- Calcula automáticamente los días de retraso y el monto total de la multa generada.
"""

 

def calcular_multa_retraso(dias_retraso):
    """Calcula la multa en base a los días de retraso."""
    tarifa_diaria = 15.00 
    return dias_retraso * tarifa_diaria
def calcular_sancion_danio_perdida(precio_libro, nivel_danio):
    """
    Calcula la sanción por daño o pérdida.
    nivel_danio puede ser: 'leve', 'grave', 'perdida'
    """
    if nivel_danio == 'perdida':
        return precio_libro + 50.00 
    elif nivel_danio == 'grave':
        return precio_libro * 0.50 
    elif nivel_danio == 'leve':
        return 30.00 
    else:
        return 0.00