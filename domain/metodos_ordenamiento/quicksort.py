from ..utils import obtener_anio_valido

class QuickSort:
    def ordenar(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr)//2]
        left = [x for x in arr if (obtener_anio_valido(x), x['autor']) < (obtener_anio_valido(pivot), pivot['autor'])]
        middle = [x for x in arr if (obtener_anio_valido(x), x['autor']) == (obtener_anio_valido(pivot), pivot['autor'])]
        right = [x for x in arr if (obtener_anio_valido(x), x['autor']) > (obtener_anio_valido(pivot), pivot['autor'])]
        return self.ordenar(left) + middle + self.ordenar(right)