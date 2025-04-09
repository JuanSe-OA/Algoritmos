def quicksort(frecuencias):
    """Implementación recursiva de Quick Sort"""
    items = list(frecuencias.items())
    
    def _quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if (-x[1], x[0]) < (-pivot[1], pivot[0])]
        middle = [x for x in arr if (-x[1], x[0]) == (-pivot[1], pivot[0])]
        right = [x for x in arr if (-x[1], x[0]) > (-pivot[1], pivot[0])]
        return _quicksort(left) + middle + _quicksort(right)
    
    return dict(_quicksort(items))