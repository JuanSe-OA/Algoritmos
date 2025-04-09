import os
import time
import bibtexparser
import matplotlib.pyplot as plt
from tabulate import tabulate

# Importar todos los métodos de ordenamiento
from bubble_sort import bubble_sort
from cocktail_shaker_sort import cocktail_shaker_sort
from timsort import timsort
from quicksort import quicksort
from selection_sort import selection_sort
from insertion_sort import insertion_sort
from shell_sort import shell_sort
from heap_sort import heap_sort
from comb_sort import comb_sort
from tree_sort import tree_sort
from bitonic_sort import bitonic_sort
from gnome_sort import gnome_sort
from binary_insertion_sort import binary_insertion_sort
from radix_sort import radix_sort
from pigeonhole_sort import pigeonhole_sort
from bucket_sort import bucket_sort

# Términos a analizar
TERMINOS = [
    "Abstraction", "Motivation", "Algorithm", "Persistence", "Coding", "Block",
    "Creativity", "Mobile application", "Logic", "Programming", "Conditionals",
    "Robotic", "Loops", "Scratch"
]

def contar_frecuencias(abstract):
    """Cuenta la frecuencia de cada término en un abstract"""
    if not abstract:
        return {term: 0 for term in TERMINOS}
    
    abstract_lower = abstract.lower()
    return {term: abstract_lower.count(term.lower()) for term in TERMINOS}

def leer_archivos_bib(folder_path):
    """Lee todos los archivos .bib en la carpeta especificada"""
    all_entries = []
    for file in os.listdir(folder_path):
        if file.endswith('.bib'):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as bib_file:
                bib_database = bibtexparser.load(bib_file)
                all_entries.extend(bib_database.entries)
    return all_entries

def procesar_articulos(entries):
    """Procesa los artículos y cuenta frecuencias de términos"""
    articulos = []
    for entry in entries:
        abstract = entry.get('abstract', '') or entry.get('summary', '') or ''
        articulos.append({
            'titulo': entry.get('title', '').strip(),
            'frecuencias': contar_frecuencias(abstract.strip()),
            'raw_data': entry
        })
    return articulos

def sumar_frecuencias(articulos):
    """Suma las frecuencias de todos los artículos"""
    frecuencias_totales = {term: 0 for term in TERMINOS}
    for articulo in articulos:
        for term, count in articulo['frecuencias'].items():
            frecuencias_totales[term] += count
    return frecuencias_totales

def mostrar_tabla(frecuencias, metodo):
    """Muestra tabla de frecuencias"""
    items = sorted(frecuencias.items(), key=lambda x: (-x[1], x[0]))
    print(f"\nResultados para {metodo}:")
    print(tabulate(items, headers=["Término", "Frecuencia"], tablefmt="grid"))

def graficar_resultados(frecuencias, metodo, tiempo):
    """Genera gráfico de barras"""
    items = sorted(frecuencias.items(), key=lambda x: (-x[1], x[0]))
    terms = [t[0] for t in items]
    counts = [t[1] for t in items]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(terms, counts)
    plt.xlabel('Términos')
    plt.ylabel('Frecuencia')
    plt.title(f'Frecuencia de términos ({metodo}) - Tiempo: {tiempo:.6f}s')
    plt.xticks(rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

def ejecutar_metodo(frecuencias, nombre_metodo, funcion_ordenamiento):
    """Ejecuta y mide el tiempo de un método"""
    start_time = time.time()
    resultado = funcion_ordenamiento(frecuencias.copy())
    tiempo = time.time() - start_time
    return resultado, tiempo

def main():
    """Función principal"""
    folder_path = input("Ingrese la ruta de la carpeta con archivos .bib: ")
    
    # Procesar archivos
    entries = leer_archivos_bib(folder_path)
    articulos = procesar_articulos(entries)
    frecuencias = sumar_frecuencias(articulos)
    
    # Mostrar frecuencias totales
    mostrar_tabla(frecuencias, "Frecuencias Totales")
    
    # Métodos de ordenamiento disponibles (16 en total)
    metodos = {
        'Bubble Sort': bubble_sort,
        'Cocktail Shaker Sort': cocktail_shaker_sort,
        'TimSort': timsort,
        'Quick Sort': quicksort,
        'Selection Sort': selection_sort,
        'Insertion Sort': insertion_sort,
        'ShellSort': shell_sort,
        'Heap Sort': heap_sort,
        'Comb Sort': comb_sort,
        'Tree Sort': tree_sort,
        'Bitonic Sort': bitonic_sort,
        'Gnome Sort': gnome_sort,
        'Binary Insertion Sort': binary_insertion_sort,
        'Radix Sort': radix_sort,
        'Pigeonhole Sort': pigeonhole_sort,
        'Bucket Sort': bucket_sort
    }
    
    # Ejecutar y comparar métodos
    tiempos = {}
    for nombre, funcion in metodos.items():
        print(f"\nEjecutando {nombre}...")
        resultado, tiempo = ejecutar_metodo(frecuencias, nombre, funcion)
        tiempos[nombre] = tiempo
        mostrar_tabla(dict(resultado), nombre)
        graficar_resultados(dict(resultado), nombre, tiempo)
    
    # Mostrar comparación de tiempos
    print("\n=== Comparación de tiempos ===")
    print(tabulate(
        sorted(tiempos.items(), key=lambda x: x[1]),
        headers=['Método', 'Tiempo (s)'],
        tablefmt='grid'
    ))
    
    # Gráfico comparativo mejorado para 16 métodos
    plt.figure(figsize=(16, 8))
    metodos_ordenados = sorted(tiempos.keys(), key=lambda x: tiempos[x])
    tiempos_ordenados = [tiempos[m] for m in metodos_ordenados]
    
    bars = plt.barh(metodos_ordenados, tiempos_ordenados, color='skyblue')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Algoritmo')
    plt.title('Comparación de tiempos de ejecución (16 algoritmos)')
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2,
                f'{width:.6f}', ha='left', va='center')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()