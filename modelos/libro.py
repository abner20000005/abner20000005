"""
- Representa las entidades 'Libros', 'Autores', 'Editoriales' y 'Categorias'.
- Almacena atributos principales: ISBN, título, año de publicación, edición, categoría y editorial.
- Estructura los datos bibliográficos de la biblioteca.
"""

class Libro:

    def __init__(self, isbn, titulo, anio, edicion,
                 descripcion, categoria, editorial, autor):

        self.isbn = isbn
        self.titulo = titulo
        self.anio = anio
        self.edicion = edicion
        self.descripcion = descripcion
        self.categoria = categoria
        self.editorial = editorial
        self.autor = autor