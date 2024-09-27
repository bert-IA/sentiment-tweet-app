import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
import uuid

# l'URL de l'application Heroku
API_URL = "https://sentiment-app-1-42e90bfa5057.herokuapp.com/predict"

# URL du service Application Insights
INSTRUMENTATION_KEY = "55d1bce9-1674-46cb-bc18-1fda71ab348d"

# Configuration du logger pour envoyer les traces à Application Insights
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Définir le niveau de log à INFO

# Ajouter un handler pour Application Insights
handler = AzureLogHandler(connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}')
logger.addHandler(handler)

# Ajouter un handler pour écrire les logs dans un fichier
file_handler = logging.FileHandler('app_heroku.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_sentiment_analysis(tweet, sentiment, validation):
    log_id = str(uuid.uuid4())
    log_message = f"Tweet: {tweet}, Sentiment: {sentiment}, Validation: {validation}, LogID: {log_id}"
    logger.warning(log_message)

def main():
    st.title("Analyse de Sentiment de Tweet")

    # Initialisation des états de session
    if 'tweet' not in st.session_state:
        st.session_state.tweet = ""
    if 'sentiment' not in st.session_state:
        st.session_state.sentiment = None
    if 'validation' not in st.session_state:
        st.session_state.validation = None
    if 'alert_sent' not in st.session_state:
        st.session_state.alert_sent = False
    if 'another_tweet' not in st.session_state:
        st.session_state.another_tweet = False
    if 'enter_tweet' not in st.session_state:
        st.session_state.enter_tweet = True

    # Demander à l'utilisateur d'entrer un tweet
    if st.session_state.enter_tweet:
        tweet = st.text_area("Entrez votre tweet ici:", value=st.session_state.tweet)
        if st.button("Analyser le sentiment"):
            if tweet:
                # Stocker le tweet dans l'état
                st.session_state.tweet = tweet
                st.session_state.enter_tweet = False
                # Appel à l'API pour obtenir la prédiction
                response = requests.post(API_URL, json={"text": tweet})
                if response.status_code == 200:
                    st.session_state.sentiment = response.json().get("sentiment")
                    st.write(f"Le sentiment du tweet est: {st.session_state.sentiment}")
                else:
                    st.write("Erreur lors de l'analyse du sentiment.")
            else:
                st.write("Veuillez entrer un tweet.")

    # Demander à l'utilisateur si la prédiction est correcte
    if st.session_state.sentiment and st.session_state.validation is None:
        st.write("La prédiction est-elle correcte ?")
        if st.button("Oui", key="yes"):
            st.session_state.validation = "Oui"
        if st.button("Non", key="no"):
            st.session_state.validation = "Non"

    # Afficher un message de remerciement ou envoyer une alerte à Application Insights
    if st.session_state.validation:
        if st.session_state.validation == "Non" and not st.session_state.alert_sent:
            log_sentiment_analysis(st.session_state.tweet, st.session_state.sentiment, st.session_state.validation)
            st.session_state.alert_sent = True
            st.write("Trace envoyée à Application Insights.")
        st.write("Merci pour votre retour. La réponse a été prise en compte.")

        # Réinitialisation des états de session et affichage du bouton pour entrer un autre tweet
        st.session_state.enter_tweet = False
        st.session_state.another_tweet = True

    # Demander à l'utilisateur s'il souhaite entrer un autre tweet
    if st.session_state.another_tweet:
        if st.button("Cliquez ici pour entrer un nouveau tweet"):
            # Réinitialisation des états de session
            st.session_state.tweet = ""
            st.session_state.sentiment = None
            st.session_state.validation = None
            st.session_state.alert_sent = False
            st.session_state.another_tweet = False
            st.session_state.enter_tweet = True
            st.experimental_rerun()

if __name__ == "__main__":
    main()