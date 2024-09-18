
import pickle
from pathlib import Path



# Data processing
import warnings
warnings.filterwarnings('ignore')


# Natural Language Processing (NLP)
import re
from nltk.tokenize import TweetTokenizer

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


def predict_pipeline(text) :
    tknz = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    
    # Convertir le texte en minuscules et supprimer les URLs
    tmp = re.sub(r"https?://\S+|www\.\S+", "", text.lower())

    # Tokeniser le texte
    tokens = tknz.tokenize(tmp)

    # Filtrer les tokens de longueur supérieure à 1
    tokens = [w for w in tokens if len(w) > 1]

    # Joindre les tokens en une seule chaîne
    tmp = " ".join(tokens)

    # Prédire la classe avec le modèle
    pred = model.predict([tmp])

   