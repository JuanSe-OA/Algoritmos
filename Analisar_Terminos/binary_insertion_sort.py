def binary_insertion_sort(frecuencias):
    """Implementación de Binary Insertion Sort"""
    items = list(frecuencias.items())
    
    for i in range(1, len(items)):
        key = items[i]
        left, right = 0, i - 1
        
        while left <= right:
            mid = (left + right) // 2
            if (-key[1], key[0]) < (-items[mid][1], items[mid][0]):
                right = mid - 1
            else:
                left = mid + 1
        
        items.insert(left, key)
        del items[i+1]
    
    return dict(items)