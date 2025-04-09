import os
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from fuzzywuzzy import fuzz

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