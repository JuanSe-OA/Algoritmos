def selection_sort(frecuencias):
    """Implementación de Selection Sort"""
    items = list(frecuencias.items())
    n = len(items)
    
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if (-items[j][1], items[j][0]) < (-items[min_idx][1], items[min_idx][0]):
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    
    return dict(items)