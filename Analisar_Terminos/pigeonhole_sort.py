def pigeonhole_sort(frecuencias):
    """Implementación de Pigeonhole Sort"""
    items = list(frecuencias.items())
    if not items:
        return {}
    
    min_freq = min(item[1] for item in items)
    max_freq = max(item[1] for item in items)
    size = max_freq - min_freq + 1
    holes = [[] for _ in range(size)]
    
    for item in items:
        holes[item[1] - min_freq].append(item)
    
    sorted_items = []
    for i in range(size-1, -1, -1):
        sorted_items.extend(sorted(holes[i], key=lambda x: x[0]))
    
    return dict(sorted_items)