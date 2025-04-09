def cocktail_shaker_sort(frecuencias):
    """Implementación de Cocktail Shaker Sort (Bubble Sort bidireccional)"""
    items = list(frecuencias.items())
    n = len(items)
    swapped = True
    start = 0
    end = n-1
    
    while swapped:
        swapped = False
        
        # Ida (izquierda a derecha)
        for i in range(start, end):
            if (items[i][1] < items[i+1][1]) or \
               (items[i][1] == items[i+1][1] and items[i][0] > items[i+1][0]):
                items[i], items[i+1] = items[i+1], items[i]
                swapped = True
        
        if not swapped:
            break
            
        swapped = False
        end -= 1
        
        # Vuelta (derecha a izquierda)
        for i in range(end-1, start-1, -1):
            if (items[i][1] < items[i+1][1]) or \
               (items[i][1] == items[i+1][1] and items[i][0] > items[i+1][0]):
                items[i], items[i+1] = items[i+1], items[i]
                swapped = True
        
        start += 1
    
    return dict(items)