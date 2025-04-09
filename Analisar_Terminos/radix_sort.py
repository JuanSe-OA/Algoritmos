def radix_sort(frecuencias):
    """Implementación de Radix Sort"""
    items = list(frecuencias.items())
    if not items:
        return {}
    
    # Ordenar primero alfabéticamente
    items.sort(key=lambda x: x[0])
    
    # Luego por frecuencia con Radix Sort
    max_freq = max(item[1] for item in items)
    exp = 1
    
    while max_freq // exp > 0:
        buckets = [[] for _ in range(10)]
        for item in items:
            digit = (item[1] // exp) % 10
            buckets[digit].append(item)
        items = [item for bucket in reversed(buckets) for item in bucket]
        exp *= 10
    
    return dict(items)