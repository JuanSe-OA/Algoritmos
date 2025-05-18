import os
import sys
import time
import copy

# Asegura que el path incluya el directorio padre para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importaciones del proyecto
from domain.metodos_ordenamiento import *
from domain.metodos_ordenamiento.binary_insertion_sort import BinaryInsertionSort
from domain.utils import (
    leer_bibtex, normalize_data, save_bibtex, buscar_duplicados,
    graficar_tiempos, extraer_abstracts_bibtex,
    graficar_dendrograma_rq5, graficar_heatmap_similitud, graficar_similitud
)
from domain.requerimientos import requerimiento2, requerimiento3, requerimiento5
from domain.agrupamiento.preprocesamiento import procesar_abstracts
from domain.agrupamiento.similitud import calcular_matriz_similitud
from domain.agrupamiento.dendograma import ClusteringJerarquico
from domain.agrupamiento.clustering_algoritmos import (
    SingleLinkageClustering, CompleteLinkageClustering
)

# -------- FUNCIONES DE REQUERIMIENTOS -------- #

def ordenar_y_medicion(articles, metodo_instancia):
    start_time = time.time()
    sorted_articles = metodo_instancia.ordenar(copy.deepcopy(articles))
    end_time = time.time()
    return sorted_articles, end_time - start_time

def ejecutar_req_1_al_3(folder_path, num_articles):
    all_articles = []
    for file in os.listdir(folder_path):
        if file.endswith('.bib'):
            file_path = os.path.join(folder_path, file)
            entries = leer_bibtex(file_path)
            all_articles.extend(normalize_data(entries))

            # TEMPORAL: inspecciona un artículo para verificar las claves
            if all_articles:
                print("Ejemplo de artículo normalizado:", all_articles[0])


    articulos_unicos, articulos_duplicados = buscar_duplicados(all_articles)
    num_articles = min(num_articles, len(articulos_unicos)) if num_articles > 0 else len(articulos_unicos)
    articulos_unicos = articulos_unicos[:num_articles]

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

    mediciones = {}
    for nombre, instancia in metodos.items():
        _, tiempo = ordenar_y_medicion(articulos_unicos, instancia)
        mediciones[nombre] = tiempo

    graficar_tiempos(mediciones, num_articles)

    articulos_finales = TimSort().ordenar(articulos_unicos)
    save_bibtex('articulos_unificados.bib', articulos_finales)

    duplicados_validos = [d for d in articulos_duplicados if d is not None]
    save_bibtex('articulos_duplicados.bib', duplicados_validos)

    r2 = requerimiento2(articulos_finales)
    r2.procesar_estadisticas()
    r2.mostrar_resultados()

    r3 = requerimiento3(ruta_bibtex='D:/WorkSpaceVisualStudio/Algoritmos/automatizao', carpeta_salida='Algoritmos/imagenes/salidas')
    r3.analizar_frecuencias()
    r3.guardar_csv_frecuencias()
    r3.generar_nube_palabras()
    r3.generar_grafico_coocurrencia()

def ejecutar_req_2_y_3(ruta_archivo_unificado):
    if not os.path.exists(ruta_archivo_unificado):
        print(f"❌ Error: El archivo {ruta_archivo_unificado} no se encuentra.")
        return None

    articulos = leer_bibtex(ruta_archivo_unificado)
    all_articles = normalize_data(articulos)

    r2 = requerimiento2(all_articles)
    r2.procesar_estadisticas()
    r2.mostrar_resultados()

    r3 = requerimiento3(ruta_archivo_unificado)
    r3.analizar_frecuencias()
    r3.guardar_csv_frecuencias()
    r3.generar_nube_palabras()
    r3.generar_grafico_coocurrencia()

    # 🔁 Asegúrate de que este método existe en la clase
    return r3.obtener_tablas_frecuencia()



def ejecutar_agrupamiento_jerarquico():
    ruta_bibtex = input("Ingrese la ruta del archivo .bib con los artículos unificados: ").strip()

    if not os.path.exists(ruta_bibtex):
        print("❌ Ruta inválida.")
        return

    entradas = leer_bibtex(ruta_bibtex)
    if not entradas:
        print("❌ No se encontraron artículos.")
        return

    print(f"✅ {len(entradas)} artículos encontrados.")
    datos_normalizados = normalize_data(entradas)
    abstracts = [d['abstract'] for d in datos_normalizados if d['abstract']]

    if not abstracts:
        print("❌ No se encontraron abstracts.")
        return

    matriz_similitud = calcular_matriz_similitud(abstracts)

    print("\n🔗 Clustering usando SINGLE linkage")
    clustering_single = SingleLinkageClustering()
    linkage_single = clustering_single.fit(matriz_similitud)
    clustering_s = ClusteringJerarquico(matriz_similitud)
    clustering_s.graficar_dendrograma(linkage_single, "Dendrograma - Single Linkage")

    print("\n🔗 Clustering usando COMPLETE linkage")
    clustering_complete = CompleteLinkageClustering()
    linkage_complete = clustering_complete.fit(matriz_similitud)
    clustering_c = ClusteringJerarquico(matriz_similitud)
    clustering_c.graficar_dendrograma(linkage_complete, "Dendrograma - Complete Linkage")


def ejecutar_requerimiento_5(file_path):
    entries = leer_bibtex(file_path)
    data = normalize_data(entries)
    data = [d for d in data if d['abstract']]
    data = data[:50]

    if len(data) < 2:
        print("❌ No hay suficientes abstracts válidos.")
        return

    abstracts = [item['abstract'] for item in data]
    etiquetas = [f"Abstract {i+1}" for i in range(len(abstracts))]

    print("✅ Calculando similitud con SBERT...")
    sim_matrix_sbert = requerimiento5.calcular_similitud_sbert(abstracts)
    graficar_heatmap_similitud(sim_matrix_sbert)
    graficar_similitud(sim_matrix_sbert, etiquetas, "Gráfico de Similitud - SBERT")

# -------- MENÚ PRINCIPAL -------- #

def main():
    while True:
        print("\n=== SISTEMA DE PROCESAMIENTO DE ARTÍCULOS ===")
        print("1. Ordenamiento y análisis (Requerimientos 1 a 3)")
        print("2. Análisis sin ordenamiento (Req 2 y 3)")
        print("3. Agrupamiento jerárquico (Req 4)")
        print("4. Similitud con SBERT (Req 5)")
        print("0. Salir")
        opcion = input("Seleccione una opción (0-4): ").strip()

        if opcion == '1':
            folder = input("Ingrese ruta de la carpeta con archivos .bib: ")
            cantidad = int(input("Cantidad de artículos a procesar: "))
            ejecutar_req_1_al_3(folder, cantidad)
        elif opcion == '2':
            ruta = input("Ingrese la ruta del archivo .bib con los artículos unificados: ")
            ejecutar_req_2_y_3(ruta)
        elif opcion == '3':
            ejecutar_agrupamiento_jerarquico()
        elif opcion == '4':
            ruta = input("Ingrese la ruta del archivo .bib (máx 50 artículos): ")
            ejecutar_requerimiento_5(ruta)
        elif opcion == '0':
            print("👋 Saliendo del sistema.")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()
