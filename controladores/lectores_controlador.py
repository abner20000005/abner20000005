from config.conexion import obtener_conexion
from modelos.lector import Lector

def listar_lectores():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT l.Id_Lector, l.Nombre, l.Apellido, l.Identidad, l.Telefono, l.Correo,
                   l.Direccion, l.Estado, l.Id_TipoLector, t.Nombre_Tipo
            FROM Lectores l
            INNER JOIN TiposLectores t ON l.Id_TipoLector = t.Id_TipoLector
            ORDER BY l.Apellido, l.Nombre
        """)
        return [Lector(*fila) for fila in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def obtener_tipos_lectores():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_TipoLector, Nombre_Tipo FROM TiposLectores ORDER BY Nombre_Tipo")
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()

def guardar_lector(nombre, apellido, identidad, telefono, correo, direccion, estado, id_tipo):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Lector FROM Lectores WHERE Identidad = ?", (identidad,))
        if cursor.fetchone():
            return "duplicado"
        cursor.execute("""
            INSERT INTO Lectores (Nombre, Apellido, Identidad, Telefono, Correo, Direccion, Estado, Id_TipoLector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, identidad, telefono, correo, direccion, estado, id_tipo))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def modificar_lector(id_lector, nombre, apellido, identidad, telefono, correo, direccion, estado, id_tipo):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE Lectores
            SET Nombre=?, Apellido=?, Identidad=?, Telefono=?, Correo=?, Direccion=?, Estado=?, Id_TipoLector=?
            WHERE Id_Lector=?
        """, (nombre, apellido, identidad, telefono, correo, direccion, estado, id_tipo, id_lector))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def eliminar_lector(id_lector):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Prestamos WHERE Id_Lector = ?", (id_lector,))
        if cursor.fetchone()[0] > 0:
            return "relacionado"
        cursor.execute("DELETE FROM Lectores WHERE Id_Lector = ?", (id_lector,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()