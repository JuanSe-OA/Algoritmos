import numpy as np
class SingleLinkageClustering:
    def __init__(self):
        self.linkage_matrix = []

    def fit(self, similarity_matrix):
        n = len(similarity_matrix)
        clusters = {i: [i] for i in range(n)}  # Usamos un diccionario para rastrear identificadores únicos
        distances = 1 - similarity_matrix.copy()
        np.fill_diagonal(distances, np.inf)

        current_cluster = n  # Comenzamos a nombrar nuevos clusters a partir de n

        while len(clusters) > 1:
            min_dist = np.inf
            pair = (0, 1)
            keys = list(clusters.keys())

            # Buscar el par de clusters con la menor distancia mínima (single linkage)
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    a, b = keys[i], keys[j]
                    dist = min([distances[x][y] for x in clusters[a] for y in clusters[b]])
                    if dist < min_dist:
                        min_dist = dist
                        pair = (a, b)

            a, b = pair
            new_cluster = clusters[a] + clusters[b]
            self.linkage_matrix.append([a, b, min_dist, len(new_cluster)])

            # Actualizar clusters
            clusters[current_cluster] = new_cluster
            del clusters[a]
            del clusters[b]
            current_cluster += 1

        return np.array(self.linkage_matrix)

# Clustering Jerárquico usando Complete Linkage
class CompleteLinkageClustering:
    def __init__(self):
        self.linkage_matrix = []

    def fit(self, similarity_matrix):
        n = len(similarity_matrix)
        clusters = {i: [i] for i in range(n)}  # Cada índice empieza en su propio cluster
        distances = 1 - similarity_matrix.copy()  # Convertimos la matriz de similitud en una de distancias
        np.fill_diagonal(distances, np.inf)  # Eliminamos la diagonal

        current_cluster = n  # Número total de clusters
        while len(clusters) > 1:
            min_dist = np.inf
            pair = (0, 1)
            keys = list(clusters.keys())

            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    a, b = keys[i], keys[j]
                    dist = max([distances[x][y] for x in clusters[a] for y in clusters[b]])
                    if dist < min_dist:
                        min_dist = dist
                        pair = (a, b)

            a, b = pair
            new_cluster = clusters[a] + clusters[b]
            self.linkage_matrix.append([a, b, min_dist, len(new_cluster)])

            clusters[current_cluster] = new_cluster
            del clusters[a]
            del clusters[b]
            current_cluster += 1

        return np.array(self.linkage_matrix)

