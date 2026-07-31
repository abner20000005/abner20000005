"""
- Maneja las consultas e inserciones de libros, autores, editoriales y categorías en la base de datos.
- Ejecuta búsquedas por título, ISBN, autor o categoría.
"""
from modelos.libro import Libro

# Lista temporal que simula la base de datos
libros = []


def guardar_libro(isbn, titulo, anio, edicion,
                  descripcion, categoria,
                  editorial, autor):

    libro = Libro(
        isbn,
        titulo,
        anio,
        edicion,
        descripcion,
        categoria,
        editorial,
        autor
    )

    libros.append(libro)


def listar_libros():
    return libros


def eliminar_libro(indice):

    if 0 <= indice < len(libros):
        libros.pop(indice)


def modificar_libro(indice,
                    isbn,
                    titulo,
                    anio,
                    edicion,
                    descripcion,
                    categoria,
                    editorial,
                    autor):

    if 0 <= indice < len(libros):

        libros[indice] = Libro(
            isbn,
            titulo,
            anio,
            edicion,
            descripcion,
            categoria,
            editorial,
            autor
        )