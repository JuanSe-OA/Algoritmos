import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Descargar recursos
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def limpiar_texto(texto):
    texto = texto.lower()
    tokens = word_tokenize(texto)
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    lematizados = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(lematizados)

def procesar_abstracts(abstracts):
    return [limpiar_texto(abs) for abs in abstracts]
