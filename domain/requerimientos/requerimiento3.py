import os
import re
from collections import defaultdict, Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from ..utils import leer_bibtex, normalize_data

class requerimiento3:
    def __init__(self, ruta_bibtex, carpeta_salida='Algoritmos/imagenes/salidas'):
        self.articulos = normalize_data(leer_bibtex(ruta_bibtex))
        self.frecuencias = defaultdict(Counter)
        self.coocurrencias = Counter()
        self.carpeta_salida = carpeta_salida
        os.makedirs(carpeta_salida, exist_ok=True)
        self.categorias_variables = self._cargar_variables()

    def _cargar_variables(self):
        return {
            "Habilidades": [
                "Abstraction", "Algorithm", "Algorithmic thinking", "Coding", "Collaboration", "Cooperation",
                "Creativity", "Critical thinking", "Debug", "Decomposition", "Evaluation", "Generalization",
                "Logic", "Logical thinking", "Modularity", "Patterns recognition", "Problem solving", "Programming"
            ],
            "Conceptos computacionales": [
                "Computationales", "Conditionals", "Control structures", "Directions", "Events", "Funtions",
                "Loops", "Modular structure", "Parallelism", "Sequences", "Software/hardware", "Variables"
            ],
            "Actitudes": [
                "Emotional", "Engagement", "Motivation", "Perceptions", "Persistence", "Self-efficacy", "Self-perceived"
            ],
            "Propiedades psicométricas": [
                "Classical Test Theory - CTT", "Confirmatory Factor Analysis - CFA", "Exploratory Factor Analysis - EFA",
                "Item Response Theory - IRT", "Reliability", "Structural Equation Model - SEM", "Validity"
            ],
            "Herramienta de evaluación": [
                "Beginners Computational Thinking test - BCTt", "Coding Attitudes Survey - ESCAS",
                "Collaborative Computing Observation Instrument", "Competent Computational Thinking test - cCTt",
                "Computational thinking skills test - CTST", "Computational concepts", 
                "Computational Thinking Assessment for Chinese Elementary Students - CTA-CES",
                "Computational Thinking Challenge - CTC", "Computational Thinking Levels Scale - CTLS",
                "Computational Thinking Scale - CTS", "Computational Thinking Skill Levels Scale - CTS",
                "Computational Thinking Test - CTt", "Computational Thinking Test",
                "Computational Thinking Test for Elementary School Students",
                "Computational Thinking Test for Lower Primary - CTtLP",
                "Computational thinking-skill tasks on numbers and arithmetic",
                "Computerized Adaptive Programming Concepts Test - CAPCT", "CT Scale - CTS",
                "Elementary Student Coding Attitudes Survey - ESCAS", "General self-efficacy scale",
                "ICT competency test", "Instrument of computational identity", "KBIT fluid intelligence subtest",
                "Mastery of computational concepts Test and an Algorithmic Test",
                "Multidimensional 21st Century Skills Scale", "Self-efficacy scale", 
                "STEM learning attitude scale", "The computational thinking scale"
            ],
            "Diseño de investigación": [
                "No experimental", "Experimental", "Longitudinal research", "Mixed methods", "Post-test", "Pre-test", "Quasi-experiments"
            ],
            "Nivel de escolaridad": [
                "Upper elementary education - Upper elementary school", "Primary school - Primary education - Elementary school",
                "Early childhood education – Kindergarten - Preschool",
                "Secondary school - Secondary education", "high school - higher education", "University – College"
            ],
            "Medio": [
                "Block programming", "Mobile application", "Pair programming", "Plugged activities", "Programming", "Robotics",
                "Spreadsheet", "STEM", "Unplugged activities"
            ],
            "Estrategia": [
                "Construct-by-self mind mapping", "Construct-on-scaffold mind mapping", "Design-based learning",
                "Evidence-centred design approach", "Gamification", "Reverse engineering pedagogy",
                "Technology-enhanced learning", "Collaborative learning", "Cooperative learning", "Flipped classroom",
                "Game-based learning", "Inquiry-based learning", "Personalized learning", "Problem-based learning",
                "Project-based learning", "Universal design for learning"
            ],
            "Herramienta": [
                "Alice", "Arduino", "Scratch", "ScratchJr", "Blockly Games", "Code.org", "Codecombat",
                "CSUnplugged", "Robot Turtles", "Hello Ruby", "Kodable", "LightbotJr", "KIBO robots", "BEE BOT",
                "CUBETTO", "Minecraft", "Agent Sheets", "Mimo", "Py– Learn", "SpaceChem"
            ]
        }

    def _limpiar_texto(self, texto):
        return re.sub(r'[^a-zA-Z0-9\s\-]', '', texto.lower())

    def analizar_frecuencias(self):
        for art in self.articulos:
            texto = self._limpiar_texto(art['raw_data'].get("abstract", ""))
            if not texto.strip():
                print("❌ Abstract vacío o sin contenido útil:", art.get('raw_data', {}).get('title', 'Sin título'))

            for categoria, variables in self.categorias_variables.items():
                encontrados = []

                for var in variables:
                    sinos = [s.strip().lower() for s in var.split(" - ")]
                    for sin in sinos:
                        if sin in texto:
                            self.frecuencias[categoria][var] += 1
                            encontrados.append(var)
                            break


            # co-ocurrencias
                for i in range(len(encontrados)):
                    for j in range(i + 1, len(encontrados)):
                        self.coocurrencias[(encontrados[i], encontrados[j])] += 1


    def generar_nube_palabras(self):
        for categoria, counter in self.frecuencias.items():
            if len(counter) > 0:  # Solo genera si hay palabras
                wc = WordCloud(width=800, height=400, background_color='white')
                wc.generate_from_frequencies(counter)
                wc.to_file(os.path.join(self.carpeta_salida, f"nube_{categoria}.png"))
            else:
                print(f"⚠️ No se encontraron palabras para la categoría '{categoria}', se omite la nube.")

    # Nube general
        total = Counter()
        for sub in self.frecuencias.values():
            total.update(sub)

        if len(total) > 0:
            wc = WordCloud(width=1000, height=500, background_color='white')
            wc.generate_from_frequencies(total)
            wc.to_file(os.path.join(self.carpeta_salida, f"nube_general.png"))
        else:
            print("⚠️ No se encontraron palabras en general para generar la nube.")


    def generar_grafico_coocurrencia(self):
        G = nx.Graph()
        for (a, b), peso in self.coocurrencias.items():
            G.add_edge(a, b, weight=peso)

        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(G, k=0.5)
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, width=[G[u][v]['weight']*0.2 for u,v in G.edges()])
        nx.draw_networkx_labels(G, pos, font_size=8)
        plt.axis('off')
        plt.title("Co-Word Network (Variables)")
        plt.tight_layout()
        plt.savefig(os.path.join(self.carpeta_salida, "co_word_network.png"))

    def guardar_csv_frecuencias(self):
        for categoria, counter in self.frecuencias.items():
            ruta = os.path.join(self.carpeta_salida, f"frecuencias_{categoria}.csv")
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write("Variable,Frecuencia\n")
                for var, freq in counter.most_common():
                    f.write(f"{var},{freq}\n")

    
    def obtener_tablas_frecuencia(self):
        tablas = {}
        for categoria, counter in self.frecuencias.items():
            df = pd.DataFrame(counter.items(), columns=["Variable", "Frecuencia"])
            df = df.sort_values(by="Frecuencia", ascending=False).reset_index(drop=True)
            tablas[categoria] = df
        return tablas
