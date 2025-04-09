def bitonic_sort(frecuencias):
    """Implementación de Bitonic Sort (solo potencia de 2)"""
    items = list(frecuencias.items())
    n = len(items)
    
    def compare_and_swap(arr, i, j, direction):
        a, b = (-arr[i][1], arr[i][0]), (-arr[j][1], arr[j][0])
        if (direction == 1 and a > b) or (direction == 0 and a < b):
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                compare_and_swap(arr, i, i + k, direction)
            bitonic_merge(arr, low, k, direction)
            bitonic_merge(arr, low + k, k, direction)

    def bitonic_sort_recursive(arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_recursive(arr, low, k, 1)
            bitonic_sort_recursive(arr, low + k, k, 0)
            bitonic_merge(arr, low, cnt, direction)

    # Ajustar a potencia de 2
    next_power = 1
    while next_power < n:
        next_power <<= 1
    items += [('', 0)] * (next_power - n)
    
    bitonic_sort_recursive(items, 0, next_power, 1)
    return dict(items[:n])