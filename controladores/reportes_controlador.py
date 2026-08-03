from config.conexion import obtener_conexion

def libros_disponibles():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT e.Codigo_Interno, l.Titulo, e.Ubicacion, e.Estado_Fisico
            FROM Ejemplares e
            INNER JOIN Libros l ON e.Id_Libro = l.Id_Libro
            WHERE e.Disponible = 1
            ORDER BY l.Titulo
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def libros_prestados():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT e.Codigo_Interno, li.Titulo, l.Nombre + ' ' + l.Apellido,
                   p.Fecha_Prestamo, p.Fecha_Limite
            FROM Prestamos p
            INNER JOIN Ejemplares e ON p.Id_Ejemplar = e.Id_Ejemplar
            INNER JOIN Libros li ON e.Id_Libro = li.Id_Libro
            INNER JOIN Lectores l ON p.Id_Lector = l.Id_Lector
            WHERE p.Estado = 'Prestado'
            ORDER BY p.Fecha_Limite
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def prestamos_atrasados():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT e.Codigo_Interno, li.Titulo, l.Nombre + ' ' + l.Apellido,
                   p.Fecha_Limite, DATEDIFF(DAY, p.Fecha_Limite, GETDATE()) AS Dias_Retraso
            FROM Prestamos p
            INNER JOIN Ejemplares e ON p.Id_Ejemplar = e.Id_Ejemplar
            INNER JOIN Libros li ON e.Id_Libro = li.Id_Libro
            INNER JOIN Lectores l ON p.Id_Lector = l.Id_Lector
            WHERE p.Estado = 'Prestado' AND p.Fecha_Limite < GETDATE()
            ORDER BY Dias_Retraso DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def multas_pendientes():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT l.Nombre + ' ' + l.Apellido, s.Motivo, s.Monto, s.Estado
            FROM Sanciones s
            INNER JOIN Lectores l ON s.Id_Lector = l.Id_Lector
            WHERE s.Estado = 'Pendiente'
            ORDER BY s.Monto DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def libros_mas_solicitados():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT TOP 10 li.Titulo, COUNT(p.Id_Prestamo) AS Veces
            FROM Prestamos p
            INNER JOIN Ejemplares e ON p.Id_Ejemplar = e.Id_Ejemplar
            INNER JOIN Libros li ON e.Id_Libro = li.Id_Libro
            GROUP BY li.Titulo
            ORDER BY Veces DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def total_libros():
    conexion = obtener_conexion()
    if not conexion:
        return 0
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Libros")
        return cursor.fetchone()[0]
    except:
        return 0
    finally:
        conexion.close()

def total_lectores():
    conexion = obtener_conexion()
    if not conexion:
        return 0
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Lectores")
        return cursor.fetchone()[0]
    except:
        return 0
    finally:
        conexion.close()

def total_prestamos_activos():
    conexion = obtener_conexion()
    if not conexion:
        return 0
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Prestamos WHERE Estado = 'Prestado'")
        return cursor.fetchone()[0]
    except:
        return 0
    finally:
        conexion.close()