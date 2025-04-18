from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def calcular_matriz_similitud(documentos):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documentos)
    similitud = cosine_similarity(tfidf_matrix)
    return similitud
