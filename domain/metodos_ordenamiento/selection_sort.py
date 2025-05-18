from ..utils import obtener_anio_valido

class SelectionSort:
    def ordenar(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if (obtener_anio_valido(arr[j]), arr[j]['author']) < (obtener_anio_valido(arr[min_idx]), arr[min_idx]['author']):
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr