"""
Maneja la lógica de registro de devoluciones, cálculo de retraso/multas
y actualización del estado de préstamos y ejemplares.
"""
from datetime import datetime, date
from config.conexion import conectar  


TARIFA_MULTA_POR_DIA = 10.00 

def obtener_prestamos_activos():
    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT p.Id_Prestamo, l.Nombre + ' ' + l.Apellido AS Lector, 
               e.Codigo_Interno, p.Fecha_Prestamo, p.Fecha_Limite, p.Id_Ejemplar
        FROM Prestamos p
        INNER JOIN Lectores l ON p.Id_Lector = l.Id_Lector
        INNER JOIN Ejemplares e ON p.Id_Ejemplar = e.Id_Ejemplar
        WHERE p.Estado = 'Activo'
    """
    cursor.execute(query)
    prestamos = cursor.fetchall()
    conn.close()
    return prestamos

def calcular_dias_y_multa(fecha_limite):
    """
    Calcula cuántos días de retraso hay a la fecha de hoy y la multa generada.
    """
    hoy = date.today()
    if isinstance(fecha_limite, str):
        fecha_limite = datetime.strptime(fecha_limite, "%Y-%m-%d").date()
        
    dias_retraso = (hoy - fecha_limite).days
    
    if dias_retraso > 0:
        multa = dias_retraso * TARIFA_MULTA_POR_DIA
    else:
        dias_retraso = 0
        multa = 0.0
        
    return dias_retraso, multa

def registrar_devolucion(id_prestamo, id_ejemplar, estado_fisico, dias_retraso, multa):
    """
    Registra la devolución en la BD y actualiza el préstamo y el ejemplar.
    """
    conn = conectar()
    cursor = conn.cursor()
    hoy = date.today()

    try:
        query_devolucion = """
            INSERT INTO Devoluciones (Fecha_Devolucion, Dias_Retraso, Multa, Id_Prestamo)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(query_devolucion, (hoy, dias_retraso, multa, id_prestamo))

        query_prestamo = "UPDATE Prestamos SET Estado = 'Finalizado' WHERE Id_Prestamo = ?"
        cursor.execute(query_prestamo, (id_prestamo,))

        query_ejemplar = """
            UPDATE Ejemplares 
            SET Disponible = 1, Estado_Fisico = ? 
            WHERE Id_Ejemplar = ?
        """
        cursor.execute(query_ejemplar, (estado_fisico, id_ejemplar))

        conn.commit()
        return True, "Devolución registrada exitosamente."

    except Exception as e:
        conn.rollback()
        return False, f"Error al procesar la devolución: {str(e)}"
    finally:
        conn.close()