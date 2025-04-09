import os
import time
import copy
from timsort import TimSort
from quicksort import QuickSort
from selection_sort import SelectionSort
from heap_sort import HeapSort
from comb_sort import CombSort
from tree_sort import TreeSort
from bitonic_sort import BitonicSort
from gnome_sort import GnomeSort
from binary_insertion_sort import BinaryInsertionSort
from radix_sort import RadixSort
from pigeonhole_sort import PigeonholeSort
from bucket_sort import BucketSort
from utils import leer_bibtex, normalize_data, save_bibtex,buscar_duplicados,graficar_tiempos,generar_estadisticas_desde_bib

def ordenar_y_medicion(articles, metodo_instancia):
    """Mide el tiempo de ejecución de un método de ordenamiento"""
    start_time = time.time()
    sorted_articles = metodo_instancia.ordenar(copy.deepcopy(articles))
    end_time = time.time()
    return sorted_articles, end_time - start_time



def main(folder_path, num_articles):
    # Leer y procesar archivos
    all_articles = []
    for file in os.listdir(folder_path):
        if file.endswith('.bib'):
            file_path = os.path.join(folder_path, file)
            entries = leer_bibtex(file_path)
            all_articles.extend(normalize_data(entries))

    # Filtrar duplicados
    articulos_unicos, articulos_duplicados = buscar_duplicados(all_articles)
    num_articles = min(num_articles, len(articulos_unicos)) if num_articles > 0 else len(articulos_unicos)
    articulos_unicos = articulos_unicos[:num_articles]

    # Configurar todos los métodos
    metodos = {
        'timsort': TimSort(),
        'quicksort': QuickSort(),
        'selection_sort': SelectionSort(),
        'heap_sort': HeapSort(),
        'comb_sort': CombSort(),
        'tree_sort': TreeSort(),
        'bitonic_sort': BitonicSort(),
        'gnome_sort': GnomeSort(),
        'binary_insertion_sort': BinaryInsertionSort(),
        'radix_sort': RadixSort(),
        'pigeonhole_sort': PigeonholeSort(),
        'bucket_sort': BucketSort()
    }

    # Ejecutar y medir cada método (VERSIÓN CORREGIDA)
    mediciones = {}
    for nombre, instancia in metodos.items():
        _, tiempo = ordenar_y_medicion(articulos_unicos, instancia)
        mediciones[nombre] = tiempo

    # Mostrar resultados
    graficar_tiempos(mediciones, num_articles)
    
    # Guardar resultados finales
    articulos_finales = TimSort().ordenar(articulos_unicos)
    save_bibtex('articulos_unificados.bib', articulos_finales)

    # Filtrar None antes de guardar duplicados
    duplicados_validos = [d for d in articulos_duplicados if d is not None]
    save_bibtex('articulos_duplicados.bib', duplicados_validos)

    #Generar_estadisticas
    generar_estadisticas_desde_bib(articulos_unicos)

    print(f"\nProcesamiento completado. Artículos ordenados: {num_articles}")
    print(f"- Total métodos evaluados: {len(metodos)}")
    print(f"- Tiempo mínimo: {min(mediciones.values()):.6f}s")
    print(f"- Tiempo máximo: {max(mediciones.values()):.6f}s")

if __name__ == "__main__":
    print("=== SISTEMA DE ORDENAMIENTO DE ARTÍCULOS ===")
    folder = input("Ingrese ruta de la carpeta con archivos .bib: ")
    cantidad = int(input("Cantidad de artículos a procesar: "))
    main(folder, cantidad)