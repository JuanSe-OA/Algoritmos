import pandas as pd
import os
import rispy
import bibtexparser
from fuzzywuzzy import fuzz

def leer_ris(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        entries = rispy.load(file)
    return entries

def leer_bibtex(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        bib_database = bibtexparser.load(file)
    return bib_database.entries

def normalize_data(entries, source):
    normalized = []
    for entry in entries:
        normalized.append({
            'titulo': entry.get('title', '').strip().lower(),
            'autor': entry.get('author', '').strip().lower(),
            'anio': entry.get('year', '').strip(),
            'doi': entry.get('doi', '').strip(),
            'source': source,
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
    db.entries = [article['raw_data'] for article in articles]
    with open(filename, 'w', encoding='utf-8') as file:
        bibtexparser.dump(db, file)

def save_ris(filename, articles):
    with open(filename, 'w', encoding='utf-8') as file:
        rispy.dump([article['raw_data'] for article in articles], file)

def main(folder_path, output_format):
    all_articles = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith('.ris'):
            entries = leer_ris(file_path)
            all_articles.extend(normalize_data(entries, 'RIS'))
        elif file.endswith('.bib'):  
            entries = leer_bibtex(file_path)
            all_articles.extend(normalize_data(entries, 'BibTeX'))
    
    articulos_unicos, articulos_duplicados = buscar_duplicados(all_articles)
    
    if output_format == 'bib':
        save_bibtex('articulos_unificados.bib', articulos_unicos)
        save_bibtex('articulos_duplicados.bib', articulos_duplicados)
    elif output_format == 'ris':
        save_ris('articulos_unificados.ris', articulos_unicos)
        save_ris('articulos_duplicados.ris', articulos_duplicados)
    
    print("Procesamiento completado. Se generaron los archivos:")
    print(f"- articulos_unificados.{output_format} (artículos sin duplicados)")
    print(f"- articulos_duplicados.{output_format} (artículos repetidos)")

if __name__ == "__main__":
    folder_path = input("Ingrese la ruta de la carpeta con los archivos: ")
    output_format = input("Ingrese el formato de salida (bib/ris): ").strip().lower()
    main(folder_path, output_format)
