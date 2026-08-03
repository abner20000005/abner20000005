from config.conexion import obtener_conexion
from modelos.autor import Autor

def listar_autores():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Autor, Nombre, Nacionalidad FROM Autores ORDER BY Nombre")
        return [Autor(fila[0], fila[1], fila[2] or "") for fila in cursor.fetchall()]
    except Exception as e:
        print(f"Error al listar autores: {e}")
        return []
    finally:
        conexion.close()


def guardar_autor(nombre, nacionalidad):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Autores (Nombre, Nacionalidad) VALUES (?, ?)", (nombre, nacionalidad))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al guardar autor: {e}")
        return False
    finally:
        conexion.close()


def modificar_autor(id_autor, nombre, nacionalidad):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE Autores SET Nombre = ?, Nacionalidad = ? WHERE Id_Autor = ?",
                       (nombre, nacionalidad, id_autor))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al modificar autor: {e}")
        return False
    finally:
        conexion.close()


def eliminar_autor(id_autor):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        # Verificar si tiene libros asociados
        cursor.execute("SELECT COUNT(*) FROM LibrosAutores WHERE Id_Autor = ?", (id_autor,))
        if cursor.fetchone()[0] > 0:
            return "relacionado"
        cursor.execute("DELETE FROM Autores WHERE Id_Autor = ?", (id_autor,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar autor: {e}")
        return False
    finally:
        conexion.close()