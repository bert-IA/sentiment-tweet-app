import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
from datetime import datetime

# URL de l'application Heroku
API_URL = "https://sentiment-app-1-42e90bfa5057.herokuapp.com/predict"

# URL du service Application Insights
INSTRUMENTATION_KEY = "55d1bce9-1674-46cb-bc18-1fda71ab348d"

# Configurer le logger pour Application Insights
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'))
logger.setLevel(logging.INFO)

def log_sentiment_analysis(tweet, sentiment, validation):
    # Fonction pour envoyer les informations à Application Insights
    properties = {
        "custom_dimensions": {
            "tweet": tweet,
            "sentiment": sentiment,
            "validation": validation,
            "timestamp": datetime.utcnow().isoformat()  # Ajouter un timestamp personnalisé
        }
    }
    logger.info("SentimentAnalysis", extra=properties)
    print(f"Log sent: {properties}")  # Message de débogage

def main():
    st.title("Analyse de Sentiment de Tweet")

    # Initialiser les clés de session_state
    if 'page' not in st.session_state:
        st.session_state.page = 'input'
    if 'tweet_input' not in st.session_state:
        st.session_state.tweet_input = ""
    if 'sentiment_output' not in st.session_state:
        st.session_state.sentiment_output = None
    if 'validation_choice' not in st.session_state:
        st.session_state.validation_choice = None

    if st.session_state.page == 'input':
        tweet_input_page()

def tweet_input_page():
    # Entrer le tweet
    tweet = st.text_input("Entrez votre tweet ici:")

    # Analyser le sentiment
    if st.button("Analyser le sentiment"):
        if tweet:
            # Stocker le tweet dans l'état
            st.session_state.tweet_input = tweet
            # Appel à l'API pour obtenir la prédiction
            response = requests.post(API_URL, json={"text": tweet})
            if response.status_code == 200:
                st.session_state.sentiment_output = response.json().get("sentiment")
                st.write(f"Le sentiment du tweet est: {st.session_state.sentiment_output}")
                st.session_state.validation_choice = None  # Réinitialiser la validation
            else:
                st.write("Erreur lors de l'analyse du sentiment.")
        else:
            st.write("Veuillez entrer un tweet.")

    # Demander si la prédiction est correcte
    if st.session_state.sentiment_output:
        st.write("La prédiction est-elle correcte ?")
        if st.button("Oui"):
            st.session_state.validation_choice = True
            send_info_and_reset()
        if st.button("Non"):
            st.session_state.validation_choice = False
            send_info_and_reset()

def send_info_and_reset():
    # Utiliser des variables locales pour stocker les informations
    tweet = st.session_state.tweet_input
    sentiment = st.session_state.sentiment_output
    validation = st.session_state.validation_choice

    # Réinitialiser les variables de session
    st.session_state.tweet_input = ""
    st.session_state.sentiment_output = None
    st.session_state.validation_choice = None

    # Envoyer les informations à Application Insights
    log_sentiment_analysis(tweet, sentiment, validation)
    st.write("Informations envoyées à Application Insights.")
    st.write("Merci, les informations ont été analysées.")

    # Revenir à la page d'entrée du tweet
    st.experimental_rerun()

if __name__ == "__main__":
    main()