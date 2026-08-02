from modelos.ejemplar import Ejemplar


class EjemplarControlador:

    def __init__(self):
        self.ejemplares = []


    def agregar_ejemplar(self, codigo_interno, libro_id,
                         estado_fisico, ubicacion,
                         disponible, fecha_adquisicion):

        nuevo = Ejemplar(
            codigo_interno=codigo_interno,
            libro_id=libro_id,
            estado_fisico=estado_fisico,
            ubicacion=ubicacion,
            disponible=disponible,
            fecha_adquisicion=fecha_adquisicion
        )

        self.ejemplares.append(nuevo)


    def obtener_ejemplares(self):
        return self.ejemplares


    def buscar_ejemplar(self, codigo):

        for ejemplar in self.ejemplares:
            if ejemplar.codigo_interno == codigo:
                return ejemplar

        return None


    def eliminar_ejemplar(self, codigo):

        ejemplar = self.buscar_ejemplar(codigo)

        if ejemplar:
            self.ejemplares.remove(ejemplar)
            return True

        return False


    def editar_ejemplar(self, codigo,
                        estado_fisico,
                        ubicacion,
                        disponible):

        ejemplar = self.buscar_ejemplar(codigo)

        if ejemplar:

            ejemplar.estado_fisico = estado_fisico
            ejemplar.ubicacion = ubicacion
            ejemplar.disponible = disponible

            return True

        return False