import heapq

def heap_sort(frecuencias):
    """Implementación de Heap Sort"""
    items = list(frecuencias.items())
    heap = []
    
    for item in items:
        heapq.heappush(heap, (-item[1], item[0], item))
    
    sorted_items = []
    while heap:
        *_, item = heapq.heappop(heap)
        sorted_items.append(item)
    
    return dict(sorted_items)