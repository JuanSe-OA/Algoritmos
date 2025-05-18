import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt


class ClusteringJerarquico:
    def __init__(self, similitudes):
        self.similitudes = similitudes

    def graficar_dendrograma(self, Z, titulo, ruta_salida=None):
        """
        Genera el dendrograma a partir de la matriz de enlace (Z).
        Si se especifica una ruta, guarda la figura como imagen.
        También devuelve la figura para su visualización en Streamlit.
        """
        num_observaciones = Z.shape[0] + 1
        etiquetas = [f"abstract{i+1}" for i in range(num_observaciones)]

        fig, ax = plt.subplots(figsize=(10, 7))
        dendrogram(Z, labels=etiquetas, ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel('Artículos')
        ax.set_ylabel('Distancia')
        plt.tight_layout()

        if ruta_salida:
            fig.savefig(ruta_salida)  # Guarda la imagen en disco
        return fig
