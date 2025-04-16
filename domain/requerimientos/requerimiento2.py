from collections import Counter, defaultdict

class requerimiento2:
    def __init__(self, articulos):
        self.articulos = articulos
        # Inicializar contadores
        self.primer_autor_counter = Counter()
        self.tipo_producto_counter = Counter()
        self.anio_tipo_counter = defaultdict(lambda: Counter())
        self.journal_counter = Counter()
        self.publisher_counter = Counter()

    def procesar_estadisticas(self):
        for art in self.articulos:
            tipo = art.get("ENTRYTYPE", "").lower()  # 'ENTRYTYPE' para el tipo de artículo
            anio = art.get("year", "Desconocido")
            autores = art.get("author", "").split(" and ")
            journal = art.get("journal", None)
            publisher = art.get("publisher", None)

            # Primer autor
            if autores and autores[0]:
                self.primer_autor_counter[autores[0].strip()] += 1

            # Tipo de producto
            self.tipo_producto_counter[tipo] += 1

            # Año por tipo
            self.anio_tipo_counter[anio][tipo] += 1

            # Journal
            if journal:
                self.journal_counter[journal.strip()] += 1

            # Publisher
            if publisher:
                self.publisher_counter[publisher.strip()] += 1

    def mostrar_resultados(self):
        print("\n📌 15 Primeros Autores con Más Apariciones:")
        for autor, count in self.primer_autor_counter.most_common(15):
            print(f" - {autor}: {count} apariciones")

        print("\n📌 Cantidad de Productos por Tipo:")
        for tipo, count in self.tipo_producto_counter.items():
            print(f" - {tipo}: {count} productos")

        print("\n📌 15 Journals con Más Apariciones:")
        for journal, count in self.journal_counter.most_common(15):
            print(f" - {journal}: {count} artículos")

        print("\n📌 15 Publishers con Más Apariciones:")
        for pub, count in self.publisher_counter.most_common(15):
            print(f" - {pub}: {count} productos")

        print("\n📌 Distribución por Año y Tipo de Producto:")
        for anio in sorted(self.anio_tipo_counter.keys()):
            print(f"Año {anio}:")
            for tipo, count in self.anio_tipo_counter[anio].items():
                print(f"  - {tipo}: {count}")