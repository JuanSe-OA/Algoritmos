import pandas as pd
import os
import bibtexparser
import time
import matplotlib.pyplot as plt
import heapq
import copy
from fuzzywuzzy import fuzz
from functools import cmp_to_key
from bibtexparser.bwriter import BibTexWriter



def leer_bibtex(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        bib_database = bibtexparser.load(file)
    return bib_database.entries

def normalize_data(entries):
    normalized = []
    for entry in entries:
        normalized.append({
            'titulo': entry.get('title', '').strip().lower(),
            'autor': entry.get('author', '').strip().lower(),
            'year': entry.get('year', '').strip(),
            'doi': entry.get('doi', '').strip(),
            'raw_data': entry
        })
    return normalized

def buscar_duplicados(articles):
    articulos_unicos = []
    articulos_duplicados = []
    vistos = {}
    
    for article in articles:
        key = (article['titulo'], article['autor'])
        if any(fuzz.ratio(article['titulo'], existing[0]) > 90 for existing in vistos):
            articulos_duplicados.append(article)
        else:
            vistos[key] = True
            articulos_unicos.append(article)
    
    return articulos_unicos, articulos_duplicados


def save_bibtex(filename, articles):
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = [article['raw_data'] for article in articles]  # Mantiene el orden

    # Usar BibTexWriter para controlar la salida
    writer = BibTexWriter()
    writer.order_entries_by = None  # Evita que BibTexWriter reordene los datos
    writer.indent = '    '  # Formateo para mayor claridad

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(writer.write(db))



def obtener_anio_valido(x):
    return int(x['year'].strip()) if x['year'] and x['year'].strip().isdigit() else 9999

def timsort(arr):
    return sorted(arr, key=lambda x: (obtener_anio_valido(x), x['autor']))

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if (obtener_anio_valido(x), x['autor']) < (obtener_anio_valido(pivot), pivot['autor'])]
    middle = [x for x in arr if (obtener_anio_valido(x), x['autor']) == (obtener_anio_valido(pivot), pivot['autor'])]
    right = [x for x in arr if (obtener_anio_valido(x), x['autor']) > (obtener_anio_valido(pivot), pivot['autor'])]
    return quicksort(left) + middle + quicksort(right)

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if (obtener_anio_valido(arr[j]), arr[j]['autor']) < (obtener_anio_valido(arr[min_idx]), arr[min_idx]['autor']):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def heap_sort(arr):
    heap = []
    for item in arr:
        heapq.heappush(heap, (obtener_anio_valido(item), item['autor'], item))
    return [heapq.heappop(heap)[2] for _ in range(len(heap))]

def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted_flag = False

    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True

        for i in range(len(arr) - gap):
            if (obtener_anio_valido(arr[i]), arr[i]['autor']) > (obtener_anio_valido(arr[i + gap]), arr[i + gap]['autor']):
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
    return arr



def tree_sort(arr):
    class Node:
        def __init__(self, key):
            self.left = self.right = None
            self.val = key

    def insert(root, key):
        if root is None:
            return Node(key)
        if (obtener_anio_valido(key), key['autor']) < (obtener_anio_valido(root.val), root.val['autor']):
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
        return root

    def inorder_traversal(root, sorted_list):
        if root:
            inorder_traversal(root.left, sorted_list)
            sorted_list.append(root.val)
            inorder_traversal(root.right, sorted_list)

    if not arr:
        return arr
    root = None
    for item in arr:
        root = insert(root, item)
    sorted_list = []
    inorder_traversal(root, sorted_list)
    return sorted_list


##Funciona bien solo con potencias de dos
def bitonic_sort(arr):
    def compare_and_swap(arr, i, j, direction):
        a, b = (obtener_anio_valido(arr[i]), arr[i]['autor']), (obtener_anio_valido(arr[j]), arr[j]['autor'])
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
            bitonic_sort_recursive(arr, low, k, 1)  # Ascendente
            bitonic_sort_recursive(arr, low + k, k, 0)  # Descendente
            bitonic_merge(arr, low, cnt, direction)

    n = len(arr)
    if n <= 1:
        return arr  # Lista vacía o con un solo elemento ya está ordenada

    bitonic_sort_recursive(arr, 0, n, 1)
    return arr




def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0 or (obtener_anio_valido(arr[index]), arr[index]['autor']) >= (obtener_anio_valido(arr[index - 1]), arr[index - 1]['autor']):
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr


def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        left, right = 0, i - 1
        while left <= right:
            mid = (left + right) // 2
            if (obtener_anio_valido(arr[mid]), arr[mid]['autor']) > (obtener_anio_valido(key), key['autor']):
                right = mid - 1
            else:
                left = mid + 1
        arr = arr[:left] + [key] + arr[left:i] + arr[i+1:]
    return arr

def radix_sort(arr):
    if not arr:
        return arr

    # Obtener el valor máximo de año
    max_anio = max(obtener_anio_valido(item) for item in arr)
    exp = 1

    # Ordenar por año usando Radix Sort
    while max_anio // exp > 0:
        buckets = [[] for _ in range(10)]
        for item in arr:
            num = obtener_anio_valido(item)
            digit_value = (num // exp) % 10
            buckets[digit_value].append(item)
        arr = [item for bucket in buckets for item in bucket]
        exp *= 10

    arr = sorted(arr, key=lambda x: (obtener_anio_valido(x), x['autor']))
    
    return arr



def pigeonhole_sort(arr):
    min_anio = min(obtener_anio_valido(x) for x in arr)
    max_anio = max(obtener_anio_valido(x) for x in arr)

    size = max_anio - min_anio + 1
    holes = [[] for _ in range(size)]

    for item in arr:
        holes[obtener_anio_valido(item) - min_anio].append(item)

    sorted_arr = []
    for hole in holes:
        sorted_arr.extend(sorted(hole, key=lambda x: x['autor']))
    return sorted_arr

def bucket_sort(arr):
    min_anio = min(obtener_anio_valido(x) for x in arr)
    max_anio = max(obtener_anio_valido(x) for x in arr)
    num_buckets = len(arr)
    buckets = [[] for _ in range(num_buckets)]

    for item in arr:
        index = int((obtener_anio_valido(item) - min_anio) * (num_buckets - 1) / (max_anio - min_anio)) if max_anio > min_anio else 0
        buckets[index].append(item)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket, key=lambda x: (obtener_anio_valido(x), x['autor'])))
    return sorted_arr



def ordenar_y_medicion(articles, metodo):
    start_time = time.time()
    metodos = {
        'timsort': timsort,
        'quicksort': quicksort,
        'selection_sort': selection_sort,
        'heap_sort': heap_sort,
        'comb_sort': comb_sort,
        'tree_sort': tree_sort,
        'pigeonhole_sort': pigeonhole_sort,
        'bucket_sort': bucket_sort,
        'bitonic_sort': bitonic_sort,
        'gnome_sort': gnome_sort,
        'binary_insertion_sort': binary_insertion_sort,
        'radix_sort': radix_sort
    }
    
    if metodo not in metodos:
        raise ValueError(f"Método de ordenamiento '{metodo}' no reconocido.")
    
    sorted_articles = metodos[metodo](copy.deepcopy(articles))  # Copia profunda
    end_time = time.time()
    return sorted_articles, end_time - start_time

def graficar_tiempos(mediciones, num_articles):
    metodos = list(mediciones.keys())
    tiempos = list(mediciones.values())

    # Lista de colores para cada algoritmo
    colores = [
        'blue', 'green', 'red', 'purple', 'orange', 'yellow', 'cyan', 'magenta', 
        'gray', 'brown', 'pink', 'lime'
    ]

    # Asegurar que haya suficientes colores
    while len(colores) < len(metodos):
        colores.extend(colores)  # Repetir colores si hay más métodos que colores

    plt.figure(figsize=(12, 6))
    plt.bar(metodos, tiempos, color=colores[:len(metodos)])  # Usar 'color' en lugar de 'colores'
    plt.xlabel('Método de Ordenamiento')
    plt.ylabel('Tiempo (s)')
    plt.title(f'Comparación de Tiempos de Ordenamiento ({num_articles} artículos)')
    plt.xticks(rotation=45, ha='right')  # Rotar etiquetas para mejor visibilidad
    plt.show()

def main(folder_path, num_articles):
    all_articles = []

    # Leer los archivos .bib
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith('.bib'):
            entries = leer_bibtex(file_path)
            all_articles.extend(normalize_data(entries))

    # Buscar duplicados
    articulos_unicos, articulos_duplicados = buscar_duplicados(all_articles)

    ##Si el usuario quiere ordenar todos los articulos
    if num_articles <= 0 or num_articles > len(articulos_unicos):
        num_articles = len(articulos_unicos) 

    # Limitar la cantidad de artículos a ordenar
    articulos_unicos = articulos_unicos[:num_articles]  # Solo usa los primeros 'num_articles'

    # Medir tiempos de ordenamiento
    metodos = ['comb_sort', 'tree_sort', 'pigeonhole_sort', 'bucket_sort', 'bitonic_sort', 
               'gnome_sort', 'binary_insertion_sort', 'radix_sort', 'timsort', 'quicksort', 
               'selection_sort', 'heap_sort']
    
    mediciones = {}
    for metodo in metodos:
        articulos_a_ordenar = articulos_unicos[:]  # Se hace una copia para cada algoritmo
        _, tiempo = ordenar_y_medicion(articulos_a_ordenar, metodo)
        mediciones[metodo] = tiempo

    # Graficar los tiempos
    graficar_tiempos(mediciones, num_articles)

    # Aplicar el ordenamiento final antes de guardar
    articulos_unicos = timsort(articulos_unicos)  # Puedes cambiarlo por otro método
        ##articulos_ordenados = bitonic_sort(articulos_unicos)
    #print("\nDespués de ordenar:")
    #for art in articulos_ordenados:
    #    print(obtener_anio_valido(art), "-", art['autor'])
    # Guardar archivos ordenados
    save_bibtex('articulos_unificados.bib', articulos_unicos)
    save_bibtex('articulos_duplicados.bib', articulos_duplicados)

    print(f"Procesamiento completado con {num_articles} artículos ordenados.")
    print("- articulos_unificados.bib (artículos sin duplicados)")
    print("- articulos_duplicados.bib (artículos repetidos)")

if __name__ == "__main__":
    folder_path = input("Ingrese la ruta de la carpeta con los archivos: ")
    num_articles = int(input("Ingrese la cantidad de artículos a ordenar: "))  # Pedir la cantidad de artículos
    main(folder_path, num_articles)
