from ..utils import obtener_anio_valido

class CombSort:
    def ordenar(self, arr):
        gap = len(arr)
        shrink = 1.3
        sorted_flag = False

        while not sorted_flag:
            gap = int(gap / shrink)
            if gap <= 1:
                gap = 1
                sorted_flag = True

            for i in range(len(arr) - gap):
                if (obtener_anio_valido(arr[i]), arr[i]['author']) > (obtener_anio_valido(arr[i + gap]), arr[i + gap]['author']):
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    sorted_flag = False
        return arr