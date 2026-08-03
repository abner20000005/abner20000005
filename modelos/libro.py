class Libro:
    def __init__(self, id_libro, isbn, titulo, anio, edicion, descripcion,
                 id_categoria, categoria, id_editorial, editorial, autor):
        self.id_libro = id_libro
        self.isbn = isbn
        self.titulo = titulo
        self.anio = anio
        self.edicion = edicion
        self.descripcion = descripcion
        self.id_categoria = id_categoria
        self.categoria = categoria
        self.id_editorial = id_editorial
        self.editorial = editorial
        self.autor = autor