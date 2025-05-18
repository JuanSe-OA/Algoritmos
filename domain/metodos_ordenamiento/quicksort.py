from ..utils import obtener_anio_valido

class QuickSort:
    def ordenar(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr)//2]
        left = [x for x in arr if (obtener_anio_valido(x), x['author']) < (obtener_anio_valido(pivot), pivot['author'])]
        middle = [x for x in arr if (obtener_anio_valido(x), x['author']) == (obtener_anio_valido(pivot), pivot['author'])]
        right = [x for x in arr if (obtener_anio_valido(x), x['author']) > (obtener_anio_valido(pivot), pivot['author'])]
        return self.ordenar(left) + middle + self.ordenar(right)