def timsort(frecuencias):
    """Implementación usando el algoritmo TimSort de Python"""
    return dict(sorted(frecuencias.items(), key=lambda x: (-x[1], x[0])))