from utils import obtener_anio_valido

class RadixSort:
    def ordenar(self, arr):
        if not arr:
            return arr

        max_anio = max(obtener_anio_valido(item) for item in arr)
        exp = 1

        while max_anio // exp > 0:
            buckets = [[] for _ in range(10)]
            for item in arr:
                num = obtener_anio_valido(item)
                digit_value = (num // exp) % 10
                buckets[digit_value].append(item)
            arr = [item for bucket in buckets for item in bucket]
            exp *= 10

        return sorted(arr, key=lambda x: (obtener_anio_valido(x), x['autor']))