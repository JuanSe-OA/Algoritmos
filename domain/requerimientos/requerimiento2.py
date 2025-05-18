from collections import Counter, defaultdict

class requerimiento2:
    def __init__(self, articulos):
        self.articulos = articulos
        self.primer_autor_counter = Counter()
        self.tipo_producto_counter = Counter()
        self.anio_tipo_counter = defaultdict(lambda: Counter())
        self.journal_counter = Counter()
        self.publisher_counter = Counter()

    def procesar_estadisticas(self):
        for art in self.articulos:
            tipo = art.get("ENTRYTYPE", "").lower()
            anio = art.get("year", "Desconocido")
            autores = art.get("author", "").split(" and ")
            journal = art.get("journal", None)
            publisher = art.get("publisher", None)

            if autores and autores[0]:
                self.primer_autor_counter[autores[0].strip()] += 1

            self.tipo_producto_counter[tipo] += 1

            self.anio_tipo_counter[anio][tipo] += 1

            if journal:
                self.journal_counter[journal.strip()] += 1

            if publisher:
                self.publisher_counter[publisher.strip()] += 1

    def mostrar_resultados(self):
        resultado = []

        resultado.append("📌 15 Primeros Autores con Más Apariciones:")
        for autor, count in self.primer_autor_counter.most_common(15):
            resultado.append(f" - {autor}: {count} apariciones")

        resultado.append("\n📌 Cantidad de Productos por Tipo:")
        for tipo, count in self.tipo_producto_counter.items():
            resultado.append(f" - {tipo}: {count} productos")

        resultado.append("\n📌 15 Journals con Más Apariciones:")
        for journal, count in self.journal_counter.most_common(15):
            resultado.append(f" - {journal}: {count} artículos")

        resultado.append("\n📌 15 Publishers con Más Apariciones:")
        for pub, count in self.publisher_counter.most_common(15):
            resultado.append(f" - {pub}: {count} productos")

        resultado.append("\n📌 Distribución por Año y Tipo de Producto:")
        for anio in sorted(self.anio_tipo_counter.keys()):
            resultado.append(f" en  {anio}")
            for tipo, count in self.anio_tipo_counter[anio].items():
                resultado.append(f"  - {tipo}: {count}")

        return "\n".join(resultado)
