def gnome_sort(frecuencias):
    """Implementación de Gnome Sort"""
    items = list(frecuencias.items())
    index = 0
    
    while index < len(items):
        if index == 0 or (-items[index][1], items[index][0]) >= (-items[index-1][1], items[index-1][0]):
            index += 1
        else:
            items[index], items[index-1] = items[index-1], items[index]
            index -= 1
    
    return dict(items)