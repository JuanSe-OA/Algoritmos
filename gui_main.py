import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import time
import copy

# Asegura que el path incluya el directorio padre para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importaciones del proyecto (las mismas que en tu código original)
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

class AplicacionAlgoritmos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Procesamiento de Artículos Científicos")
        self.root.geometry("900x700")
        
        # Variables de estado
        self.articles = []
        self.articulos_unicos = []
        self.articulos_duplicados = []
        
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Crear las pestañas
        self.crear_pestana_ordenamiento()
        self.crear_pestana_analisis()
        self.crear_pestana_agrupamiento()
        self.crear_pestana_similitud()
        self.crear_pestana_configuracion()
        
        # Barra de estado
        self.status_bar = tk.Label(root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def actualizar_estado(self, mensaje):
        self.status_bar.config(text=mensaje)
        self.root.update_idletasks()
    
    def crear_pestana_ordenamiento(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Ordenamiento (Req 1-3)")

        # Sección de selección de archivos
        ttk.Label(frame, text="Carpeta con archivos .bib:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_folder = ttk.Entry(frame, width=50)
        self.entry_folder.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Examinar...", command=self.seleccionar_carpeta).grid(row=0, column=2, padx=5, pady=5)

        # Cantidad de artículos (Spinbox corregido)
        ttk.Label(frame, text="Cantidad de artículos a procesar:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.spin_articles = tk.Spinbox(frame, from_=1, to=10000, width=5)
        self.spin_articles.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.spin_articles.delete(0, tk.END)  # Limpiar valor por defecto
        self.spin_articles.insert(0, "100")   # Establecer valor inicial

        # Resto del código permanece igual...
        ttk.Label(frame, text="Algoritmos de ordenamiento:").grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        self.algoritmos_frame = ttk.Frame(frame)
        self.algoritmos_frame.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')

        self.algoritmos_vars = {}
        algoritmos = [
            'timsort', 'quicksort', 'selection_sort', 'heap_sort',
            'comb_sort', 'tree_sort', 'bitonic_sort', 'gnome_sort',
            'binary_insertion_sort', 'radix_sort', 'pigeonhole_sort', 'bucket_sort'
        ]

        for i, algo in enumerate(algoritmos):
            var = tk.BooleanVar(value=True)
            self.algoritmos_vars[algo] = var
            cb = ttk.Checkbutton(self.algoritmos_frame, text=algo, variable=var)
            cb.grid(row=i//3, column=i%3, sticky='w')

        # Botón de ejecución
        ttk.Button(frame, text="Ejecutar Ordenamiento y Análisis", 
                command=self.ejecutar_ordenamiento).grid(row=3, column=0, columnspan=3, pady=10)

        # Área de resultados
        self.resultados_text = scrolledtext.ScrolledText(frame, width=100, height=20)
        self.resultados_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
    
    def crear_pestana_analisis(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Análisis (Req 2-3)")

        # Selección de archivo
        ttk.Label(frame, text="Archivo .bib unificado:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_archivo_unificado = ttk.Entry(frame, width=50)
        self.entry_archivo_unificado.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Examinar...", command=lambda: self.seleccionar_archivo(self.entry_archivo_unificado)).grid(row=0, column=2, padx=5, pady=5)

        # Botones de ejecución
        ttk.Button(frame, text="Ejecutar Análisis Estadístico (Req 2)", 
                command=self.ejecutar_req2).grid(row=1, column=0, columnspan=3, pady=5)
        ttk.Button(frame, text="Ejecutar Análisis de Frecuencias (Req 3)", 
                command=self.ejecutar_req3).grid(row=2, column=0, columnspan=3, pady=5)

        # Área de resultados
        self.analisis_text = scrolledtext.ScrolledText(frame, width=100, height=20)
        self.analisis_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
    
    def crear_pestana_agrupamiento(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Agrupamiento (Req 4)")

        # Selección de archivo
        ttk.Label(frame, text="Archivo .bib unificado:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_agrupamiento = ttk.Entry(frame, width=50)
        self.entry_agrupamiento.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Examinar...", command=lambda: self.seleccionar_archivo(self.entry_agrupamiento)).grid(row=0, column=2, padx=5, pady=5)

        # Opciones de clustering
        ttk.Label(frame, text="Método de clustering:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.clustering_var = tk.StringVar(value="single")  # Valor por defecto: Single Linkage
        ttk.Radiobutton(frame, text="Single Linkage", variable=self.clustering_var, value="single").grid(row=1, column=1, sticky='w')
        ttk.Radiobutton(frame, text="Complete Linkage", variable=self.clustering_var, value="complete").grid(row=1, column=2, sticky='w')

        # Botón de ejecución
        ttk.Button(frame, text="Ejecutar Agrupamiento Jerárquico", 
                command=self.ejecutar_agrupamiento).grid(row=2, column=0, columnspan=3, pady=10)

        # Área de resultados
        self.agrupamiento_text = scrolledtext.ScrolledText(frame, width=100, height=20)
        self.agrupamiento_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        
    def crear_pestana_similitud(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Similitud (Req 5)")

        # Selección de archivo
        ttk.Label(frame, text="Archivo .bib (máx 50 artículos):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_similitud = ttk.Entry(frame, width=50)
        self.entry_similitud.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Examinar...", command=lambda: self.seleccionar_archivo(self.entry_similitud)).grid(row=0, column=2, padx=5, pady=5)

        # Botón de ejecución
        ttk.Button(frame, text="Calcular Similitud con SBERT", 
                command=self.ejecutar_similitud).grid(row=1, column=0, columnspan=3, pady=10)

        # Área de resultados
        self.similitud_text = scrolledtext.ScrolledText(frame, width=100, height=20)
        self.similitud_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
    
    def crear_pestana_configuracion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Configuración")

        # Configuración de rutas de salida
        ttk.Label(frame, text="Carpeta para imágenes de salida:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_output_img = ttk.Entry(frame, width=50)
        self.entry_output_img.grid(row=0, column=1, padx=5, pady=5)
        self.entry_output_img.insert(0, "Algoritmos/imagenes/salidas")  # Ruta por defecto
        ttk.Button(frame, text="Examinar...", command=lambda: self.seleccionar_carpeta(self.entry_output_img)).grid(row=0, column=2, padx=5, pady=5)

        # Botón de guardar configuración
        ttk.Button(frame, text="Guardar Configuración", 
                command=self.guardar_configuracion).grid(row=1, column=0, columnspan=3, pady=10)
    
    def seleccionar_carpeta(self, entry_widget=None):
        folder = filedialog.askdirectory()
        if folder:
            if entry_widget:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, folder)
            else:
                self.entry_folder.delete(0, tk.END)
                self.entry_folder.insert(0, folder)
    
    def seleccionar_archivo(self, entry_widget):
        file = filedialog.askopenfilename(filetypes=[("BibTeX files", "*.bib")])
        if file:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file)
    
    def ordenar_y_medicion(self, articles, metodo_instancia):
        start_time = time.time()
        sorted_articles = metodo_instancia.ordenar(copy.deepcopy(articles))
        end_time = time.time()
        return sorted_articles, end_time - start_time
    
    def ejecutar_ordenamiento(self):
        folder_path = self.entry_folder.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Por favor seleccione una carpeta válida")
            return
        
        try:
            num_articles = int(self.spin_articles.get())
        except ValueError:
            messagebox.showerror("Error", "Cantidad de artículos debe ser un número")
            return
        
        self.actualizar_estado("Leyendo archivos .bib...")
        
        try:
            all_articles = []
            for file in os.listdir(folder_path):
                if file.endswith('.bib'):
                    file_path = os.path.join(folder_path, file)
                    entries = leer_bibtex(file_path)
                    all_articles.extend(normalize_data(entries))
            
            if not all_articles:
                messagebox.showerror("Error", "No se encontraron artículos en los archivos .bib")
                return
            
            self.actualizar_estado("Buscando duplicados...")
            self.articulos_unicos, self.articulos_duplicados = buscar_duplicados(all_articles)
            num_articles = min(num_articles, len(self.articulos_unicos)) if num_articles > 0 else len(self.articulos_unicos)
            articulos_unicos = self.articulos_unicos[:num_articles]
            
            # Filtrar algoritmos seleccionados
            metodos_seleccionados = {nombre: globals()[nombre.title()]() 
                                    for nombre, var in self.algoritmos_vars.items() if var.get()}
            
            if not metodos_seleccionados:
                messagebox.showerror("Error", "Seleccione al menos un algoritmo")
                return
            
            self.actualizar_estado("Ejecutando algoritmos de ordenamiento...")
            mediciones = {}
            for nombre, instancia in metodos_seleccionados.items():
                _, tiempo = self.ordenar_y_medicion(articulos_unicos, instancia)
                mediciones[nombre] = tiempo
                self.resultados_text.insert(tk.END, f"{nombre}: {tiempo:.4f} segundos\n")
                self.resultados_text.see(tk.END)
                self.root.update_idletasks()
            
            self.actualizar_estado("Generando gráfico de tiempos...")
            graficar_tiempos(mediciones, num_articles)
            
            self.actualizar_estado("Guardando resultados...")
            articulos_finales = TimSort().ordenar(articulos_unicos)
            save_bibtex('articulos_unificados.bib', articulos_finales)
            
            duplicados_validos = [d for d in self.articulos_duplicados if d is not None]
            save_bibtex('articulos_duplicados.bib', duplicados_validos)
            
            self.actualizar_estado("Ejecutando requerimiento 2...")
            r2 = requerimiento2(articulos_finales)
            r2.procesar_estadisticas()
            resultados_r2 = r2.mostrar_resultados(return_str=True)
            self.resultados_text.insert(tk.END, "\n=== RESULTADOS REQUERIMIENTO 2 ===\n")
            self.resultados_text.insert(tk.END, resultados_r2)
            
            self.actualizar_estado("Ejecutando requerimiento 3...")
            output_folder = self.entry_output_img.get()
            r3 = requerimiento3(ruta_bibtex=folder_path, carpeta_salida=output_folder)
            r3.analizar_frecuencias()
            r3.guardar_csv_frecuencias()
            r3.generar_nube_palabras()
            r3.generar_grafico_coocurrencia()
            self.resultados_text.insert(tk.END, "\n=== REQUERIMIENTO 3 COMPLETADO ===\n")
            self.resultados_text.insert(tk.END, f"Resultados guardados en: {output_folder}\n")
            
            self.actualizar_estado("Proceso completado")
            messagebox.showinfo("Éxito", "Procesamiento completado correctamente")
            
        except Exception as e:
            self.actualizar_estado("Error")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def ejecutar_req2(self):
        ruta_archivo = self.entry_archivo_unificado.get()
        if not ruta_archivo or not os.path.exists(ruta_archivo):
            messagebox.showerror("Error", "Seleccione un archivo .bib válido")
            return
        
        try:
            self.actualizar_estado("Leyendo archivo .bib...")
            articulos = leer_bibtex(ruta_archivo)
            all_articles = normalize_data(articulos)
            
            self.actualizar_estado("Ejecutando requerimiento 2...")
            r2 = requerimiento2(all_articles)
            r2.procesar_estadisticas()
            resultados_r2 = r2.mostrar_resultados(return_str=True)
            
            self.analisis_text.delete(1.0, tk.END)
            self.analisis_text.insert(tk.END, "=== RESULTADOS REQUERIMIENTO 2 ===\n")
            self.analisis_text.insert(tk.END, resultados_r2)
            
            self.actualizar_estado("Requerimiento 2 completado")
            messagebox.showinfo("Éxito", "Análisis estadístico completado")
            
        except Exception as e:
            self.actualizar_estado("Error")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def ejecutar_req3(self):
        ruta_archivo = self.entry_archivo_unificado.get()
        if not ruta_archivo or not os.path.exists(ruta_archivo):
            messagebox.showerror("Error", "Seleccione un archivo .bib válido")
            return
        
        try:
            output_folder = self.entry_output_img.get()
            
            self.actualizar_estado("Ejecutando requerimiento 3...")
            r3 = requerimiento3(ruta_archivo_unificado=ruta_archivo, carpeta_salida=output_folder)
            r3.analizar_frecuencias()
            r3.guardar_csv_frecuencias()
            r3.generar_nube_palabras()
            r3.generar_grafico_coocurrencia()
            
            self.analisis_text.insert(tk.END, "\n=== REQUERIMIENTO 3 COMPLETADO ===\n")
            self.analisis_text.insert(tk.END, f"Resultados guardados en: {output_folder}\n")
            
            self.actualizar_estado("Requerimiento 3 completado")
            messagebox.showinfo("Éxito", "Análisis de frecuencias completado")
            
        except Exception as e:
            self.actualizar_estado("Error")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def ejecutar_agrupamiento(self):
        ruta_bibtex = self.entry_agrupamiento.get()
        if not ruta_bibtex or not os.path.exists(ruta_bibtex):
            messagebox.showerror("Error", "Seleccione un archivo .bib válido")
            return
        
        try:
            self.actualizar_estado("Leyendo artículos...")
            entradas = leer_bibtex(ruta_bibtex)
            if not entradas:
                messagebox.showerror("Error", "No se encontraron artículos")
                return
            
            self.agrupamiento_text.delete(1.0, tk.END)
            self.agrupamiento_text.insert(tk.END, f"✅ {len(entradas)} artículos encontrados.\n")
            self.root.update_idletasks()
            
            datos_normalizados = normalize_data(entradas)
            abstracts = [d['abstract'] for d in datos_normalizados if d['abstract']]
            
            if not abstracts:
                messagebox.showerror("Error", "No se encontraron abstracts")
                return
            
            self.actualizar_estado("Calculando matriz de similitud...")
            matriz_similitud = calcular_matriz_similitud(abstracts)
            
            metodo = self.clustering_var.get()
            if metodo == "single":
                self.agrupamiento_text.insert(tk.END, "\n🔗 Clustering usando SINGLE linkage\n")
                clustering = SingleLinkageClustering()
                nombre = "Single Linkage"
            else:
                self.agrupamiento_text.insert(tk.END, "\n🔗 Clustering usando COMPLETE linkage\n")
                clustering = CompleteLinkageClustering()
                nombre = "Complete Linkage"
            
            self.actualizar_estado(f"Ejecutando {nombre}...")
            linkage_matrix = clustering.fit(matriz_similitud)
            clustering_obj = ClusteringJerarquico(matriz_similitud)
            clustering_obj.graficar_dendrograma(linkage_matrix, f"Dendrograma - {nombre}")
            
            self.agrupamiento_text.insert(tk.END, f"\n✅ Dendrograma generado para {nombre}\n")
            self.actualizar_estado("Proceso completado")
            messagebox.showinfo("Éxito", f"Agrupamiento {nombre} completado")
            
        except Exception as e:
            self.actualizar_estado("Error")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def ejecutar_similitud(self):
        file_path = self.entry_similitud.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Seleccione un archivo .bib válido")
            return
        
        try:
            self.actualizar_estado("Leyendo artículos...")
            entries = leer_bibtex(file_path)
            data = normalize_data(entries)
            data = [d for d in data if d['abstract']]
            data = data[:50]  # Limitar a 50 artículos
            
            if len(data) < 2:
                messagebox.showerror("Error", "No hay suficientes abstracts válidos (mínimo 2)")
                return
            
            abstracts = [item['abstract'] for item in data]
            etiquetas = [f"Abstract {i+1}" for i in range(len(abstracts))]
            
            self.actualizar_estado("Calculando similitud con SBERT...")
            sim_matrix_sbert = requerimiento5.calcular_similitud_sbert(abstracts)
            
            self.actualizar_estado("Generando visualizaciones...")
            graficar_heatmap_similitud(sim_matrix_sbert)
            graficar_similitud(sim_matrix_sbert, etiquetas, "Gráfico de Similitud - SBERT")
            
            self.similitud_text.delete(1.0, tk.END)
            self.similitud_text.insert(tk.END, "✅ Análisis de similitud completado\n")
            self.similitud_text.insert(tk.END, f"📊 Se procesaron {len(abstracts)} abstracts\n")
            
            self.actualizar_estado("Proceso completado")
            messagebox.showinfo("Éxito", "Análisis de similitud completado")
            
        except Exception as e:
            self.actualizar_estado("Error")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def guardar_configuracion(self):
        # Aquí puedes implementar la lógica para guardar configuraciones persistentes
        messagebox.showinfo("Configuración", "Configuración guardada (implementar lógica real)")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionAlgoritmos(root)
    root.mainloop()