import os
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from fuzzywuzzy import fuzz
from collections import Counter, defaultdict
import matplotlib.pyplot as plt


def leer_bibtex(file_path):
    """Lee archivo BibTeX y devuelve entradas"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return bibtexparser.load(file).entries

def normalize_data(entries):
    """Normaliza los datos de los artículos"""
    return [{
        'titulo': e.get('title', '').strip().lower(),
        'autor': e.get('author', '').strip().lower(),
        'year': e.get('year', '').strip(),
        'doi': e.get('doi', '').strip(),
        'raw_data': e
    } for e in entries]

def save_bibtex(filename, articles):
    """Guarda artículos en archivo BibTeX, filtrando None"""
    db = bibtexparser.bibdatabase.BibDatabase()
    # Filtrar artículos que no son None y tienen raw_data
    db.entries = [a['raw_data'] for a in articles if a is not None and 'raw_data' in a]
    
    writer = BibTexWriter()
    writer.order_entries_by = None
    writer.indent = '    '
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(writer.write(db))

def obtener_anio_valido(x):
    """Obtiene año como entero o devuelve valor por defecto"""
    if isinstance(x, dict):  # Si es un diccionario de artículo
        year_str = x.get('year', '')
    else:  # Si es directamente el valor year
        year_str = x
        
    if year_str and str(year_str).strip().isdigit():
        return int(str(year_str).strip())
    return 9999  # Valor por defecto para años inválidos

def buscar_duplicados(articles):
    """Identifica artículos duplicados usando fuzzy matching"""
    unicos = []
    duplicados = []
    vistos = {}
    
    for article in articles:
        key = (article['titulo'], article['autor'])
        # Verificar si ya existe un artículo similar
        duplicado = False
        for visto_key in vistos:
            if fuzz.ratio(article['titulo'], visto_key[0]) > 90:
                duplicados.append(article)  # Guardar el duplicado real
                duplicado = True
                break
        
        if not duplicado:
            vistos[key] = article
            unicos.append(article)
    
    return unicos, duplicados

def graficar_tiempos(mediciones, num_articles):
    """Genera gráfico de comparación de tiempos"""
    metodos = list(mediciones.keys())
    tiempos = list(mediciones.values())

    plt.figure(figsize=(12, 6))
    bars = plt.bar(metodos, tiempos)
    plt.xlabel('Método de Ordenamiento')
    plt.ylabel('Tiempo (s)')
    plt.title(f'Comparación de Tiempos ({num_articles} artículos)')
    plt.xticks(rotation=45, ha='right')
    
    # Añadir valores en las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

    
def graficar_barh(datos, titulo, xlabel, ylabel, invertido=True):
    """
    Función para graficar barras horizontales.

    :param datos: Diccionario o iterable de tuplas (clave, valor)
    :param titulo: Título del gráfico
    :param xlabel: Etiqueta del eje X
    :param ylabel: Etiqueta del eje Y
    :param invertido: Si se debe invertir el eje Y (opcional, por defecto True)
    """
    claves, valores = zip(*datos)
    plt.figure(figsize=(10, 6))
    plt.barh(claves, valores, color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    if invertido:
        plt.gca().invert_yaxis()  # Invertir el eje Y para tener el más frecuente arriba
    plt.show()

def generar_estadisticas_desde_bib(entries):
    # Asegurarse que entries tiene estructura de diccionario (no lista de 'raw_data' solamente)
    if isinstance(entries[0], dict) and 'raw_data' in entries[0]:
        entries = [e['raw_data'] for e in entries]

    print("\n=== Estadísticas Generadas ===")

    # 1. Primer autor más frecuente (top 15)
    primer_autores = Counter()
    for entry in entries:
        if 'author' in entry:
            primer = entry['author'].split(' and ')[0].strip().lower()
            primer_autores[primer] += 1

    print("\n📌 Top 15 Primeros Autores:")
    for autor, count in primer_autores.most_common(15):
        print(f"  {autor}: {count}")

    # Graficar los autores más frecuentes
    graficar_barh(primer_autores.most_common(15), 'Top 15 Primeros Autores', 'Frecuencia', 'Autor')

    # 2. Año de publicación por tipo de producto
    años_por_tipo = defaultdict(lambda: defaultdict(int))
    for entry in entries:
        tipo = entry.get('ENTRYTYPE', 'otro').lower()
        año = entry.get('year', 'sin año')
        años_por_tipo[tipo][año] += 1

    print("\n📊 Año de Publicación por Tipo de Producto:")
    for tipo, año_dict in años_por_tipo.items():
        print(f"\n🔹 {tipo.title()}:")
        for año, count in sorted(año_dict.items()):
            print(f"    {año}: {count}")

    # Graficar el año de publicación por tipo de producto
    for tipo, año_dict in años_por_tipo.items():
        graficar_barh(sorted(año_dict.items()), 
                      f'Año de Publicación por Tipo de Producto - {tipo.title()}', 
                      'Cantidad', 'Año', invertido=False)

    # 3. Tipo de producto (conteo total)
    tipos = Counter(entry.get('ENTRYTYPE', 'otro').lower() for entry in entries)
    print("\n📦 Cantidad por Tipo de Producto:")
    for tipo, count in tipos.items():
        print(f"  {tipo}: {count}")

    # Graficar el tipo de producto
    graficar_barh(tipos.items(), 'Cantidad por Tipo de Producto', 'Frecuencia', 'Tipo de Producto')

    # 4. Journal más frecuente (top 15)
    journals = Counter(entry.get('journal', 'sin journal').strip().lower() for entry in entries)
    print("\n📚 Top 15 Journals:")
    for journal, count in journals.most_common(15):
        print(f"  {journal}: {count}")

    # Graficar los journals más frecuentes
    graficar_barh(journals.most_common(15), 'Top 15 Journals', 'Frecuencia', 'Journal')

    # 5. Publisher más frecuente (top 15)
    publishers = Counter(entry.get('publisher', 'sin publisher').strip().lower() for entry in entries)
    print("\n🏢 Top 15 Publishers:")
    for pub, count in publishers.most_common(15):
        print(f"  {pub}: {count}")

    # Graficar los publishers más frecuentes
    graficar_barh(publishers.most_common(15), 'Top 15 Publishers', 'Frecuencia', 'Publisher')