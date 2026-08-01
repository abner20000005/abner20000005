from modelos.libro import Libro

# Lista temporal
libros = []


def guardar_libro(isbn, titulo, anio, edicion,
                  descripcion, categoria,
                  editorial, autor):

    # Validar que no exista otro libro con el mismo ISBN
    for libro in libros:
        if libro.isbn == isbn:
            return False

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

    return True


def listar_libros():
    return libros


def obtener_libro(indice):

    if 0 <= indice < len(libros):
        return libros[indice]

    return None


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

        libros[indice].isbn = isbn
        libros[indice].titulo = titulo
        libros[indice].anio = anio
        libros[indice].edicion = edicion
        libros[indice].descripcion = descripcion
        libros[indice].categoria = categoria
        libros[indice].editorial = editorial
        libros[indice].autor = autor


def eliminar_libro(indice):

    if 0 <= indice < len(libros):
        libros.pop(indice)