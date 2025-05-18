from ..utils import obtener_anio_valido

class BitonicSort:
    def compare_and_swap(self, arr, i, j, direction):
        a, b = (obtener_anio_valido(arr[i]), arr[i]['author']), (obtener_anio_valido(arr[j]), arr[j]['author'])
        if (direction == 1 and a > b) or (direction == 0 and a < b):
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(self, arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                self.compare_and_swap(arr, i, i + k, direction)
            self.bitonic_merge(arr, low, k, direction)
            self.bitonic_merge(arr, low + k, k, direction)

    def bitonic_sort_recursive(self, arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            self.bitonic_sort_recursive(arr, low, k, 1)
            self.bitonic_sort_recursive(arr, low + k, k, 0)
            self.bitonic_merge(arr, low, cnt, direction)

    def ordenar(self, arr):
        n = len(arr)
        if n <= 1:
            return arr
        self.bitonic_sort_recursive(arr, 0, n, 1)
        return arr