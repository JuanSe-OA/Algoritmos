import heapq
from ..utils import obtener_anio_valido

class HeapSort:
    def ordenar(self, arr):
        heap = []
        for item in arr:
            # Convertimos a tupla comparable (año, autor, id único)
            heapq.heappush(heap, (
                obtener_anio_valido(item), 
                item['author'], 
                id(item),  # Usamos id() como desempate único
                item  # Mantenemos el artículo original
            ))
        
        sorted_list = []
        while heap:
            # Extraemos solo el artículo (el último elemento de la tupla)
            *_, articulo = heapq.heappop(heap)
            sorted_list.append(articulo)
        return sorted_list