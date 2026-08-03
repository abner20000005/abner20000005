from config.conexion import obtener_conexion
from modelos.libro import Libro

def listar_libros():
    conexion = obtener_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT l.Id_Libro, l.ISBN, l.Titulo, l.Anio_Publicacion, l.Numero_Edicion,
                   l.Descripcion, l.Id_Categoria, c.Nombre, l.Id_Editorial, e.Nombre,
                   ISNULL(a.Nombre, '') AS Autor
            FROM Libros l
            INNER JOIN Categorias c ON l.Id_Categoria = c.Id_Categoria
            INNER JOIN Editoriales e ON l.Id_Editorial = e.Id_Editorial
            LEFT JOIN LibrosAutores la ON l.Id_Libro = la.Id_Libro
            LEFT JOIN Autores a ON la.Id_Autor = a.Id_Autor
            ORDER BY l.Titulo
        """)
        libros = []
        for fila in cursor.fetchall():
            libros.append(Libro(*fila))
        return libros
    except Exception as e:
        print(f"Error al listar libros: {e}")
        return []
    finally:
        conexion.close()


def obtener_categorias():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Categoria, Nombre FROM Categorias ORDER BY Nombre")
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()


def obtener_editoriales():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Editorial, Nombre FROM Editoriales ORDER BY Nombre")
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()


def obtener_autores():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Autor, Nombre FROM Autores ORDER BY Nombre")
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()


def guardar_libro(isbn, titulo, anio, edicion, descripcion, id_categoria, id_editorial, id_autor):
    conexion = obtener_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()

        # Verificar si el ISBN ya existe
        cursor.execute("SELECT Id_Libro FROM Libros WHERE ISBN = ?", (isbn,))
        if cursor.fetchone():
            return False

        cursor.execute("""
            INSERT INTO Libros (ISBN, Titulo, Anio_Publicacion, Numero_Edicion, Descripcion, Id_Categoria, Id_Editorial)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (isbn, titulo, anio, edicion, descripcion, id_categoria, id_editorial))

        # Obtener el Id del libro recién insertado
        cursor.execute("SELECT @@IDENTITY")
        id_libro = cursor.fetchone()[0]

        # Guardar relación con el autor
        if id_autor:
            cursor.execute("INSERT INTO LibrosAutores (Id_Libro, Id_Autor) VALUES (?, ?)", (id_libro, id_autor))

        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al guardar libro: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.close()


def modificar_libro(id_libro, isbn, titulo, anio, edicion, descripcion, id_categoria, id_editorial, id_autor):
    conexion = obtener_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE Libros
            SET ISBN = ?, Titulo = ?, Anio_Publicacion = ?, Numero_Edicion = ?,
                Descripcion = ?, Id_Categoria = ?, Id_Editorial = ?
            WHERE Id_Libro = ?
        """, (isbn, titulo, anio, edicion, descripcion, id_categoria, id_editorial, id_libro))

        # Actualizar autor
        cursor.execute("DELETE FROM LibrosAutores WHERE Id_Libro = ?", (id_libro,))
        if id_autor:
            cursor.execute("INSERT INTO LibrosAutores (Id_Libro, Id_Autor) VALUES (?, ?)", (id_libro, id_autor))

        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al modificar libro: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.close()


def eliminar_libro(id_libro):
    conexion = obtener_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM LibrosAutores WHERE Id_Libro = ?", (id_libro,))
        cursor.execute("DELETE FROM Libros WHERE Id_Libro = ?", (id_libro,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar libro: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.close()