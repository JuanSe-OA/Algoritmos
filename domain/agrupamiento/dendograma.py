import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt


class ClusteringJerarquico:
    def __init__(self, similitudes):
        self.similitudes = similitudes

    def graficar_dendrograma(self, Z, titulo):
        """
        Genera el dendrograma a partir de la matriz de enlace (Z).
        """
        import matplotlib.pyplot as plt
        from scipy.cluster.hierarchy import dendrogram

        # Número de observaciones originales (Z tiene n-1 filas)
        num_observaciones = Z.shape[0] + 1

        # Generar etiquetas como abstrac1, abstrac2, ...
        etiquetas = [f"abstract{i+1}" for i in range(num_observaciones)]

        plt.figure(figsize=(10, 7))
        dendrogram(Z, labels=etiquetas)
        plt.title(titulo)
        plt.xlabel('Artículos')
        plt.ylabel('Distancia')
        plt.tight_layout()
        plt.show()




