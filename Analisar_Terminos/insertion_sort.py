def insertion_sort(frecuencias):
    """Ordenamiento por Inserción para diccionarios de frecuencias"""
    items = list(frecuencias.items())
    
    for j in range(1, len(items)):
        llave = items[j]
        i = j - 1
        
        # Ordenamos por frecuencia descendente y término ascendente
        while i >= 0 and (-items[i][1], items[i][0]) > (-llave[1], llave[0]):
            items[i + 1] = items[i]
            i -= 1
        items[i + 1] = llave
    
    return items
