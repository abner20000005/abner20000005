from config.conexion import obtener_conexion
from modelos.ejemplar import Ejemplar

def listar_ejemplares():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT e.Id_Ejemplar, e.Codigo_Interno, e.Estado_Fisico, e.Ubicacion,
                   e.Disponible, e.Fecha_Adquisicion, e.Id_Libro, l.Titulo
            FROM Ejemplares e
            INNER JOIN Libros l ON e.Id_Libro = l.Id_Libro
            ORDER BY e.Codigo_Interno
        """)
        return [Ejemplar(*f) for f in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
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

def guardar_ejemplar(codigo, estado, ubicacion, disponible, fecha, id_libro):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Ejemplar FROM Ejemplares WHERE Codigo_Interno = ?", (codigo,))
        if cursor.fetchone():
            return "duplicado"
        cursor.execute("""
            INSERT INTO Ejemplares (Codigo_Interno, Estado_Fisico, Ubicacion, Disponible, Fecha_Adquisicion, Id_Libro)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (codigo, estado, ubicacion, disponible, fecha, id_libro))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def modificar_ejemplar(id_ejemplar, codigo, estado, ubicacion, disponible, fecha, id_libro):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE Ejemplares
            SET Codigo_Interno=?, Estado_Fisico=?, Ubicacion=?, Disponible=?, Fecha_Adquisicion=?, Id_Libro=?
            WHERE Id_Ejemplar=?
        """, (codigo, estado, ubicacion, disponible, fecha, id_libro, id_ejemplar))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def eliminar_ejemplar(id_ejemplar):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Prestamos WHERE Id_Ejemplar = ?", (id_ejemplar,))
        if cursor.fetchone()[0] > 0:
            return "relacionado"
        cursor.execute("DELETE FROM Ejemplares WHERE Id_Ejemplar = ?", (id_ejemplar,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()