from ..utils import obtener_anio_valido

class PigeonholeSort:
    def ordenar(self, arr):
        min_anio = min(obtener_anio_valido(x) for x in arr)
        max_anio = max(obtener_anio_valido(x) for x in arr)

        size = max_anio - min_anio + 1
        holes = [[] for _ in range(size)]

        for item in arr:
            holes[obtener_anio_valido(item) - min_anio].append(item)

        sorted_arr = []
        for hole in holes:
            sorted_arr.extend(sorted(hole, key=lambda x: x['autor']))
        return sorted_arr