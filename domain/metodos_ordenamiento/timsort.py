from ..utils import obtener_anio_valido

class TimSort:
    def ordenar(self, arr):
        return sorted(arr, key=lambda x: (obtener_anio_valido(x), x['autor']))