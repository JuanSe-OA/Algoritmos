import os
import sys
import time
import copy

sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Sube un nivel y agrega a sys.path

# Importaciones del proyecto
from Algoritmos.domain.metodos_ordenamiento import *
from Algoritmos.domain.utils import leer_bibtex, normalize_data, save_bibtex, buscar_duplicados, graficar_tiempos,extraer_abstracts_bibtex,graficar_dendrograma_rq5,graficar_heatmap_similitud,graficar_similitud
from Algoritmos.domain.requerimientos import requerimiento2, requerimiento3,requerimiento5
from Algoritmos.domain.agrupamiento.preprocesamiento import procesar_abstracts
from Algoritmos.domain.agrupamiento.similitud import calcular_matriz_similitud
from Algoritmos.domain.agrupamiento.dendograma import ClusteringJerarquico
from Algoritmos.domain.agrupamiento.clustering_algoritmos import (
    SingleLinkageClustering,
    CompleteLinkageClustering
)

"""def ordenar_y_medicion(articles, metodo_instancia):
    Mide el tiempo de ejecución de un método de ordenamiento
    start_time = time.time()
    sorted_articles = metodo_instancia.ordenar(copy.deepcopy(articles))
    end_time = time.time()
    return sorted_articles, end_time - start_time
"""

#MAIN CON LA IMPLEMETANCIÓN DEL REQUERIMIENTO 1 HASTA EL 3*
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

#MAIN CON LOS REQUERIMIENTOS DEL 2 Y 3, SIN USO DEL BOT
""""
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
    r3 = requerimiento3(ruta_archivo_unificado)
    r3.analizar_frecuencias()
    r3.guardar_csv_frecuencias()
    r3.generar_nube_palabras()
    r3.generar_grafico_coocurrencia()
    
if __name__ == "__main__":
    print("=== SISTEMA DE PROCESAMIENTO DE ARTÍCULOS UNIFICADOS ===")
    ruta = input("Ingrese la ruta completa del archivo .bib con los artículos unificados: ")
    main(ruta)
"""
#MAIN SEGUIMIENTO 2



def main():
    ruta_bibtex = input("Ingrese la ruta completa del archivo .bib con los artículos unificados: ").strip()

    if not os.path.exists(ruta_bibtex):
        print("❌ Error: La ruta al archivo .bib no es válida.")
        return

    # Leer las entradas completas desde el archivo .bib
    entradas = leer_bibtex(ruta_bibtex)

    if not entradas:
        print("❌ No se encontraron artículos en el archivo.")
        return

    print(f"✅ {len(entradas)} artículos encontrados.")

    # Normalizar datos
    datos_normalizados = normalize_data(entradas)

    # Extraer abstracts y etiquetas
    abstracts = [d['abstract'] for d in datos_normalizados if d['abstract']]


    if not abstracts:
        print("❌ No se encontraron abstracts.")
        return

    # Calcular matriz de similitud
    matriz_similitud = calcular_matriz_similitud(abstracts)

    # Clustering jerárquico - Single Linkage
    print("\n🔗 Clustering usando SINGLE linkage")
    clustering_single = SingleLinkageClustering()
    linkage_single = clustering_single.fit(matriz_similitud)
    clustering_s = ClusteringJerarquico(matriz_similitud)
    clustering_s.graficar_dendrograma(linkage_single, "Dendrograma - Single Linkage")

    # Clustering jerárquico - Complete Linkage
    print("\n🔗 Clustering usando COMPLETE linkage")
    clustering_complete = CompleteLinkageClustering()
    linkage_complete = clustering_complete.fit(matriz_similitud)
    clustering_c = ClusteringJerarquico(matriz_similitud)
    clustering_c.graficar_dendrograma(linkage_complete, "Dendrograma - Complete Linkage")


if __name__ == "__main__":
    print("=== AGRUPAMIENTO JERÁRQUICO DE ABSTRACTS ===")
    main()
    

"""""
#MAIN REQUERIMIENTO 5
def main(file_path):
    # Leer y normalizar datos
    entries = leer_bibtex(file_path)
    data = normalize_data(entries)

    # Filtrar artículos sin abstract
    data = [d for d in data if d['abstract']]
    
    # Limitar a los 50 primeros artículos
    data = data[:50]

    if len(data) < 2:
        print("No hay suficientes abstracts válidos para calcular similitud.")
        return

    # Extraer abstracts
    abstracts = [item['abstract'] for item in data]
    etiquetas = [f"Abstract {i+1}" for i in range(len(abstracts))]

    # --- SBERT ---
    print("Calculando similitud con SBERT...")
    sim_matrix_sbert = requerimiento5.calcular_similitud_sbert(abstracts)
    dist_matrix_sbert = 1 - sim_matrix_sbert
    graficar_dendrograma_rq5(dist_matrix_sbert, etiquetas, titulo="Similitud de Abstracts - SBERT")

    # --- WMD ---
    print("Calculando similitud con WMD (puede tardar unos minutos)...")
    dist_matrix_wmd = requerimiento5.calcular_similitud_wmd(abstracts)
    graficar_dendrograma_rq5(dist_matrix_wmd, etiquetas, titulo="Similitud de Abstracts - WMD")


if __name__ == "__main__":
    file_path = input("Ruta al archivo BibTeX: ")
    main(file_path)
"""""