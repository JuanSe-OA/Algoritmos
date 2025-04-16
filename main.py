import os
import sys
import time
import copy

sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Sube un nivel y agrega a sys.path

# Importaciones del proyecto
from Algoritmos.domain.metodos_ordenamiento import *
from Algoritmos.domain.utils import leer_bibtex, normalize_data, save_bibtex, buscar_duplicados, graficar_tiempos
from Algoritmos.domain.requerimientos import requerimiento2, requerimiento3


def ordenar_y_medicion(articles, metodo_instancia):
    """Mide el tiempo de ejecución de un método de ordenamiento"""
    start_time = time.time()
    sorted_articles = metodo_instancia.ordenar(copy.deepcopy(articles))
    end_time = time.time()
    return sorted_articles, end_time - start_time



"""def main(folder_path, num_articles):
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
        tiempo = ordenar_y_medicion(articulos_unicos, instancia)
        mediciones[nombre] = tiempo

    # Mostrar resultados
    graficar_tiempos(mediciones, num_articles)

    
    # Guardar resultados finales
    articulos_finales = TimSort().ordenar(articulos_unicos)
    save_bibtex('articulos_unificados.bib', articulos_finales)

    # Filtrar None antes de guardar duplicados
    duplicados_validos = [d for d in articulos_duplicados if d is not None]
    save_bibtex('articulos_duplicados.bib', duplicados_validos)

    #Requerimiento 2
    r2 = requerimiento2(articulos_finales)
    r2.procesar_estadisticas()
    r2.mostrar_resultados()

    #Requerimiento 3
    r3 = requerimiento3(carpeta_salida='Algoritmos/imagenes/salidas')

    r3.analizar_frecuencias()
    r3.guardar_csv_frecuencias()
    r3.generar_nube_palabras()
    r3.generar_grafico_coocurrencia()

if __name__ == "__main__":
    print("=== SISTEMA DE ORDENAMIENTO DE ARTÍCULOS ===")
    folder = input("Ingrese ruta de la carpeta con archivos .bib: ")
    cantidad = int(input("Cantidad de artículos a procesar: "))
    main(folder, cantidad)
"""

def main(ruta_archivo_unificado):
    # Leer y procesar el archivo de artículos unificados
    if not os.path.exists(ruta_archivo_unificado):
        print(f"Error: El archivo {ruta_archivo_unificado} no se encuentra en la ruta especificada.")
        return

    articulos = leer_bibtex(ruta_archivo_unificado)
    all_articles = normalize_data(articulos) 

    # Requerimiento 2
    r2 = requerimiento2(all_articles)
    r2.procesar_estadisticas()
    r2.mostrar_resultados()

    # Requerimiento 3
    r3 = requerimiento3('articulos_unificados.bib')
    r3.analizar_frecuencias()
    r3.guardar_csv_frecuencias()
    r3.generar_nube_palabras()
    r3.generar_grafico_coocurrencia()

if __name__ == "__main__":
    print("=== SISTEMA DE PROCESAMIENTO DE ARTÍCULOS UNIFICADOS ===")
    ruta = input("Ingrese la ruta completa del archivo .bib con los artículos unificados: ")
    main(ruta)