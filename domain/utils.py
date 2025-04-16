import os
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt



def leer_bibtex(file_path):
    """Lee archivo BibTeX y devuelve entradas"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return bibtexparser.load(file).entries

def normalize_data(entries):
    """Normaliza los datos de los artículos"""
    return [{
        'title': e.get('title', '').strip().lower(),   # Normalizando 'title'
        'author': e.get('author', '').strip().lower(),  # Normalizando 'author'
        'year': e.get('year', '').strip(),              # Normalizando 'year'
        'doi': e.get('doi', '').strip(),                # Normalizando 'doi'
        'journal': e.get('journal', '').strip().lower(), # Normalizando 'journal'
        'publisher': e.get('publisher', '').strip().lower(), # Normalizando 'publisher'
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

