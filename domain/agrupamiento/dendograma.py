import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt


class ClusteringJerarquico:
    def __init__(self, similitudes, etiquetas):
        self.similitudes = similitudes
        self.etiquetas = etiquetas

    def graficar_dendrograma(self, Z, titulo):
        """
        Genera el dendrograma a partir de la matriz de enlace (Z).
        """
        # Número de observaciones originales (Z tiene n-1 filas)
        num_observaciones = Z.shape[0] + 1

        # Verificamos que las etiquetas estén completas
        if len(self.etiquetas) < num_observaciones:
            raise ValueError("No hay suficientes etiquetas para graficar el dendrograma.")

        etiquetas = self.etiquetas[:num_observaciones]

        plt.figure(figsize=(10, 7))
        dendrogram(Z, labels=etiquetas)
        plt.title(titulo)
        plt.xlabel('Artículos')
        plt.ylabel('Distancia')
        plt.tight_layout()
        plt.show()

