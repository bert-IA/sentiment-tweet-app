
import pickle
from pathlib import Path
import nltk


# Data processing
import warnings
warnings.filterwarnings('ignore')


# Natural Language Processing (NLP)
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer, TweetTokenizer

# Regular expressions
import re

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
    tknz=TweetTokenizer(preserve_case=False,strip_handles=True, reduce_len=True)
    tkn=RegexpTokenizer(r"\w+")

    tmp=text.lower()
    # suppression des adresses mails
    tmp = re.sub(r"https?\S+", "", tmp)
    #suppresion des www.
    tmp = re.sub(r"www.?\S+", "", tmp)
    #suppresion des # et réduction des lettres répétées
    tmp=(tknz.tokenize(tmp))
    tmp =" ".join(tmp)
    tmp = re.sub("[0-9]","", tmp) 
    tmp=re.sub("[_-__-]"," ",tmp)
    # retrait des ponctuations
    tmp=tkn.tokenize(tmp)
    #retrait d'autres caratères spéciaux
    tmp =[char for char in list(tmp) if not (char in ponctuations)]
    
    tmp=[w for w in tmp if w not in freq_5]
    
    
    lemmatizer = WordNetLemmatizer()
    tmp=[lemmatizer.lemmatize(w) for w in tmp]
        
    tmp=[w for w in tmp if len(w)>1]
    
    tmp=" ".join(tmp)

    pred=model.predict([tmp])
    
    return classes[pred[0]]