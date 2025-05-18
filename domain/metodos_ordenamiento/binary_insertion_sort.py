from ..utils import obtener_anio_valido

class BinaryInsertionSort:
    def ordenar(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            left, right = 0, i - 1
            while left <= right:
                mid = (left + right) // 2
                if (obtener_anio_valido(arr[mid]), arr[mid]['author']) > (obtener_anio_valido(key), key['author']):
                    right = mid - 1
                else:
                    left = mid + 1
            arr = arr[:left] + [key] + arr[left:i] + arr[i+1:]
        return arr