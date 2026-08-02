class Ejemplar:

    def __init__(self, id_ejemplar=None, codigo_interno="", libro_id=None,
                 estado_fisico="", ubicacion="", disponible=True,
                 fecha_adquisicion=""):

        self.id_ejemplar = id_ejemplar
        self.codigo_interno = codigo_interno
        self.libro_id = libro_id
        self.estado_fisico = estado_fisico
        self.ubicacion = ubicacion
        self.disponible = disponible
        self.fecha_adquisicion = fecha_adquisicion


    def __str__(self):
        return (
            f"Ejemplar("
            f"{self.codigo_interno}, "
            f"{self.estado_fisico}, "
            f"{self.ubicacion})"
        )