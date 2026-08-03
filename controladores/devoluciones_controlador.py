from config.conexion import obtener_conexion
from modelos.devolucion import Devolucion
from datetime import datetime

def listar_devoluciones():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT d.Id_Devolucion, d.Fecha_Devolucion, d.Dias_Retraso, d.Multa,
                   d.Id_Prestamo, l.Nombre + ' ' + l.Apellido, li.Titulo, e.Codigo_Interno
            FROM Devoluciones d
            INNER JOIN Prestamos p ON d.Id_Prestamo = p.Id_Prestamo
            INNER JOIN Lectores l ON p.Id_Lector = l.Id_Lector
            INNER JOIN Ejemplares e ON p.Id_Ejemplar = e.Id_Ejemplar
            INNER JOIN Libros li ON e.Id_Libro = li.Id_Libro
            ORDER BY d.Id_Devolucion DESC
        """)
        return [Devolucion(*f) for f in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def obtener_prestamos_activos():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.Id_Prestamo,
                   e.Codigo_Interno + ' - ' + li.Titulo + ' (' + l.Nombre + ' ' + l.Apellido + ')',
                   p.Fecha_Limite, p.Id_Ejemplar
            FROM Prestamos p
            INNER JOIN Lectores l ON p.Id_Lector = l.Id_Lector
            INNER JOIN Ejemplares e ON p.Id_Ejemplar = e.Id_Ejemplar
            INNER JOIN Libros li ON e.Id_Libro = li.Id_Libro
            WHERE p.Estado = 'Prestado'
            ORDER BY p.Id_Prestamo
        """)
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()

def registrar_devolucion(id_prestamo, id_ejemplar, fecha_limite, fecha_devolucion, monto_diario=10):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        # Calcular días de retraso
        f_limite = datetime.strptime(str(fecha_limite)[:10], "%Y-%m-%d")
        f_dev = datetime.strptime(str(fecha_devolucion)[:10], "%Y-%m-%d")
        dias = (f_dev - f_limite).days
        dias_retraso = max(0, dias)
        multa = dias_retraso * monto_diario

        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO Devoluciones (Fecha_Devolucion, Dias_Retraso, Multa, Id_Prestamo)
            VALUES (?, ?, ?, ?)
        """, (fecha_devolucion, dias_retraso, multa, id_prestamo))

        cursor.execute("UPDATE Prestamos SET Estado = 'Devuelto' WHERE Id_Prestamo = ?", (id_prestamo,))
        cursor.execute("UPDATE Ejemplares SET Disponible = 1 WHERE Id_Ejemplar = ?", (id_ejemplar,))

        # Si hay multa, crear sanción
        if multa > 0:
            cursor.execute("SELECT Id_Lector FROM Prestamos WHERE Id_Prestamo = ?", (id_prestamo,))
            id_lector = cursor.fetchone()[0]
            cursor.execute("""
                INSERT INTO Sanciones (Motivo, Monto, Estado, Id_Lector)
                VALUES (?, ?, 'Pendiente', ?)
            """, (f"Retraso de {dias_retraso} día(s) en préstamo #{id_prestamo}", multa, id_lector))

        conexion.commit()
        return True, dias_retraso, multa
    except Exception as e:
        print(f"Error: {e}")
        conexion.rollback()
        return False, 0, 0
    finally:
        conexion.close()