from utils import obtener_anio_valido

class GnomeSort:
    def ordenar(self, arr):
        index = 0
        while index < len(arr):
            if index == 0 or (obtener_anio_valido(arr[index]), arr[index]['autor']) >= (obtener_anio_valido(arr[index - 1]), arr[index - 1]['autor']):
                index += 1
            else:
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                index -= 1
        return arr