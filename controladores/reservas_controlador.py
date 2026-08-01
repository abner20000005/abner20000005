from config.conexion import conectar
from modelos.reservas import Reserva

def listar_reservas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
            SELECT R.Id_Reserva, L.Nombre + ' ' + L.Apellido, B.Titulo, 
                   R.Fecha_Reserva, R.Orden_Espera, R.Estado
            FROM Reservas R
            JOIN Lectores L ON R.Id_Lector = L.Id_Lector
            JOIN Libros B ON R.Id_Libro = B.Id_Libro
        """
        cursor.execute(query)
        registros = cursor.fetchall()
        conn.close()
        
        return [Reserva(*row) for row in registros]
    except Exception as e:
        print("Error al listar reservas:", e)
        return []

def guardar_reserva(id_lector, id_libro, fecha):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Reservas (Id_Lector, Id_Libro, Fecha_Reserva, Estado)
            VALUES (?, ?, ?, 'Activa')
        """, (id_lector, id_libro, fecha))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error al guardar reserva:", e)

def cancelar_reserva(id_reserva):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE Reservas SET Estado = 'Cancelada' WHERE Id_Reserva = ?", (id_reserva,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error al cancelar reserva:", e)

def eliminar_reserva(id_reserva):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Reservas WHERE Id_Reserva = ?", (id_reserva,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error al eliminar reserva:", e)