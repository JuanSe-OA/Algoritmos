def bubble_sort(frecuencias):
    """Implementación clásica de Bubble Sort"""
    items = list(frecuencias.items())
    n = len(items)
    
    for i in range(n):
        for j in range(0, n-i-1):
            if (items[j][1] < items[j+1][1]) or \
               (items[j][1] == items[j+1][1] and items[j][0] > items[j+1][0]):
                items[j], items[j+1] = items[j+1], items[j]
    
    return dict(items)