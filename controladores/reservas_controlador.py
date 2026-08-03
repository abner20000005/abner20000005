from config.conexion import obtener_conexion
from modelos.reserva import Reserva

def listar_reservas():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT r.Id_Reserva, r.Fecha_Reserva, r.Estado,
                   r.Id_Lector, l.Nombre + ' ' + l.Apellido,
                   r.Id_Libro, li.Titulo
            FROM Reservas r
            INNER JOIN Lectores l ON r.Id_Lector = l.Id_Lector
            INNER JOIN Libros li ON r.Id_Libro = li.Id_Libro
            ORDER BY r.Id_Reserva DESC
        """)
        return [Reserva(*f) for f in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def obtener_lectores():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Lector, Nombre + ' ' + Apellido FROM Lectores WHERE Estado = 'Activo' ORDER BY Apellido")
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()

def obtener_libros():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Libro, Titulo FROM Libros ORDER BY Titulo")
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()

def guardar_reserva(fecha, id_lector, id_libro):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO Reservas (Fecha_Reserva, Estado, Id_Lector, Id_Libro)
            VALUES (?, 'Activa', ?, ?)
        """, (fecha, id_lector, id_libro))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def cancelar_reserva(id_reserva):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE Reservas SET Estado = 'Cancelada' WHERE Id_Reserva = ?", (id_reserva,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()