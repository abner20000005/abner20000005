from config.conexion import obtener_conexion
from modelos.prestamo import Prestamo

def listar_prestamos():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.Id_Prestamo, p.Fecha_Prestamo, p.Fecha_Limite, p.Estado,
                   p.Id_Lector, l.Nombre + ' ' + l.Apellido,
                   p.Id_Ejemplar, e.Codigo_Interno, li.Titulo
            FROM Prestamos p
            INNER JOIN Lectores l ON p.Id_Lector = l.Id_Lector
            INNER JOIN Ejemplares e ON p.Id_Ejemplar = e.Id_Ejemplar
            INNER JOIN Libros li ON e.Id_Libro = li.Id_Libro
            ORDER BY p.Id_Prestamo DESC
        """)
        return [Prestamo(*f) for f in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def obtener_lectores_activos():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT Id_Lector, Nombre + ' ' + Apellido
            FROM Lectores WHERE Estado = 'Activo' ORDER BY Apellido
        """)
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()

def obtener_ejemplares_disponibles():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT e.Id_Ejemplar, e.Codigo_Interno + ' - ' + l.Titulo
            FROM Ejemplares e
            INNER JOIN Libros l ON e.Id_Libro = l.Id_Libro
            WHERE e.Disponible = 1 AND e.Estado_Fisico NOT IN ('Perdido', 'Dañado')
            ORDER BY e.Codigo_Interno
        """)
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()

def guardar_prestamo(fecha_prestamo, fecha_limite, id_lector, id_ejemplar):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO Prestamos (Fecha_Prestamo, Fecha_Limite, Estado, Id_Lector, Id_Ejemplar)
            VALUES (?, ?, 'Prestado', ?, ?)
        """, (fecha_prestamo, fecha_limite, id_lector, id_ejemplar))
        # Marcar ejemplar como no disponible
        cursor.execute("UPDATE Ejemplares SET Disponible = 0 WHERE Id_Ejemplar = ?", (id_ejemplar,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.close()

def anular_prestamo(id_prestamo, id_ejemplar):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE Prestamos SET Estado = 'Anulado' WHERE Id_Prestamo = ?", (id_prestamo,))
        cursor.execute("UPDATE Ejemplares SET Disponible = 1 WHERE Id_Ejemplar = ?", (id_ejemplar,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()