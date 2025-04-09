from utils import obtener_anio_valido

class BucketSort:
    def ordenar(self, arr):
        min_anio = min(obtener_anio_valido(x) for x in arr)
        max_anio = max(obtener_anio_valido(x) for x in arr)
        num_buckets = len(arr)
        buckets = [[] for _ in range(num_buckets)]

        for item in arr:
            index = int((obtener_anio_valido(item) - min_anio) * (num_buckets - 1) / (max_anio - min_anio)) if max_anio > min_anio else 0
            buckets[index].append(item)

        sorted_arr = []
        for bucket in buckets:
            sorted_arr.extend(sorted(bucket, key=lambda x: (obtener_anio_valido(x), x['autor'])))
        return sorted_arr