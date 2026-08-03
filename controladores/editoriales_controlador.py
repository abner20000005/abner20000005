from config.conexion import obtener_conexion
from modelos.editorial import Editorial

def listar_editoriales():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Editorial, Nombre, Pais, Telefono FROM Editoriales ORDER BY Nombre")
        return [Editorial(f[0], f[1], f[2] or "", f[3] or "") for f in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def guardar_editorial(nombre, pais, telefono):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Editoriales (Nombre, Pais, Telefono) VALUES (?, ?, ?)",
                       (nombre, pais, telefono))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def modificar_editorial(id_editorial, nombre, pais, telefono):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE Editoriales SET Nombre = ?, Pais = ?, Telefono = ? WHERE Id_Editorial = ?",
                       (nombre, pais, telefono, id_editorial))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def eliminar_editorial(id_editorial):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Libros WHERE Id_Editorial = ?", (id_editorial,))
        if cursor.fetchone()[0] > 0:
            return "relacionado"
        cursor.execute("DELETE FROM Editoriales WHERE Id_Editorial = ?", (id_editorial,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()