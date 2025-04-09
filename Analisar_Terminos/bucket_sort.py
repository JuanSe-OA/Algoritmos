def bucket_sort(frecuencias):
    """Implementación de Bucket Sort"""
    items = list(frecuencias.items())
    if not items:
        return {}
    
    min_freq = min(item[1] for item in items)
    max_freq = max(item[1] for item in items)
    num_buckets = len(items)
    buckets = [[] for _ in range(num_buckets)]
    
    for item in items:
        if max_freq == min_freq:
            index = 0
        else:
            index = int((item[1] - min_freq) * (num_buckets - 1) / (max_freq - min_freq))
        buckets[index].append(item)
    
    sorted_items = []
    for bucket in reversed(buckets):
        sorted_items.extend(sorted(bucket, key=lambda x: (-x[1], x[0])))
    
    return dict(sorted_items)