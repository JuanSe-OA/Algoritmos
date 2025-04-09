def comb_sort(frecuencias):
    """Implementación de Comb Sort"""
    items = list(frecuencias.items())
    gap = len(items)
    shrink = 1.3
    is_sorted = False
    
    while not is_sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            is_sorted = True
        
        for i in range(len(items) - gap):
            if (-items[i][1], items[i][0]) > (-items[i+gap][1], items[i+gap][0]):
                items[i], items[i+gap] = items[i+gap], items[i]
                is_sorted = False
    return dict(items)