from config.conexion import obtener_conexion
from modelos.categoria import Categoria

def listar_categorias():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Categoria, Nombre, Descripcion FROM Categorias ORDER BY Nombre")
        return [Categoria(f[0], f[1], f[2] or "") for f in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def guardar_categoria(nombre, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Categorias (Nombre, Descripcion) VALUES (?, ?)", (nombre, descripcion))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def modificar_categoria(id_categoria, nombre, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE Categorias SET Nombre = ?, Descripcion = ? WHERE Id_Categoria = ?",
                       (nombre, descripcion, id_categoria))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def eliminar_categoria(id_categoria):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Libros WHERE Id_Categoria = ?", (id_categoria,))
        if cursor.fetchone()[0] > 0:
            return "relacionado"
        cursor.execute("DELETE FROM Categorias WHERE Id_Categoria = ?", (id_categoria,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()