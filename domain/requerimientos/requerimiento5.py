from sentence_transformers import SentenceTransformer, util
import numpy as np
from gensim.models import KeyedVectors
from gensim.utils import simple_preprocess
from gensim.downloader import load as gensim_load
from gensim.parsing.preprocessing import STOPWORDS


from sentence_transformers import SentenceTransformer, util
import numpy as np
def calcular_similitud_sbert(abstracts):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(abstracts, convert_to_tensor=True)
    similitudes = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()
    return similitudes



def calcular_similitud_wmd(abstracts):
    print("Cargando vectores GloVe...")
    word_vectors = gensim_load('glove-wiki-gigaword-100')

    print("Preprocesando abstracts...")
    # Eliminar stopwords y preprocesar
    docs = [
        [word for word in simple_preprocess(abs_text) if word not in STOPWORDS]
        for abs_text in abstracts
    ]

    # Filtrar documentos vacíos
    docs = [doc if doc else ['empty'] for doc in docs]

    n = len(docs)
    dist_matrix = np.zeros((n, n))

    print("Calculando distancias WMD...")
    for i in range(n):
        for j in range(i + 1, n):
            try:
                dist = word_vectors.wmdistance(docs[i], docs[j])
                if np.isinf(dist) or np.isnan(dist):
                    dist = 10.0
            except Exception as e:
                print(f"Error entre doc {i} y {j}: {e}")
                dist = 10.0
            dist_matrix[i][j] = dist_matrix[j][i] = dist

    return dist_matrix