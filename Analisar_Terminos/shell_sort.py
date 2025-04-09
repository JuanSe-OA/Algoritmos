def shell_sort(frecuencias):
    items = list(frecuencias.items())
    n = len(items)
    
    incr = n // 2
    while incr > 0:
        for i in range(incr, n):
            temp = items[i]
            j = i
            while j >= incr and (-items[j-incr][1], items[j-incr][0]) > (-temp[1], temp[0]):
                items[j] = items[j-incr]
                j -= incr
            items[j] = temp
        incr = incr // 2
    
    return items