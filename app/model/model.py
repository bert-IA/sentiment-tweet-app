
import pickle
from pathlib import Path



# Data processing
import warnings
warnings.filterwarnings('ignore')


# Natural Language Processing (NLP)
import re
import spacy

__version__="0.1.0"
BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/trained_pipeline-{__version__}.pkl","rb") as f :
    model = pickle.load(f)

classes = [
    "tweet_négatif",
    "tweet_positif"
    ]
with open(f"{BASE_DIR}/ponctuations.pkl","rb") as liste :
    ponctuations = pickle.load(liste)

with open(f"{BASE_DIR}/freq5_list.pkl","rb") as freq :
    freq_5= pickle.load(freq)


# Charger le modèle de langue anglais de spacy
nlp = spacy.load("en_core_web_sm")

def predict_pipeline(text):
    # Convertir le texte en minuscules et supprimer les URLs
    tmp = re.sub(r"https?://\S+|www\.\S+", "", text.lower())

    # Tokeniser et lemmatiser le texte
    doc = nlp(tmp)
    tokens = [token.lemma_ for token in doc if len(token) > 1]

    # Joindre les tokens en une seule chaîne
    tmp = " ".join(tokens)

    # Prédire la classe avec le modèle
    pred = model.predict([tmp])

    return classes[pred[0]]

   