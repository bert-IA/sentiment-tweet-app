import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# l'URL de l'application Heroku
API_URL = "https://sentiment-app-1-42e90bfa5057.herokuapp.com/predict"

# URL du service Application Insights
INSTRUMENTATION_KEY = "55d1bce9-1674-46cb-bc18-1fda71ab348d"

# Configuration du logger pour envoyer les traces à Application Insights
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Définir le niveau de log à INFO
handler = AzureLogHandler(connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}')
logger.addHandler(handler)

def main():
    st.title("Analyse de Sentiment de Tweet")

    # Initialisation des états de session
    if 'tweet' not in st.session_state:
        st.session_state.tweet = ""
    if 'sentiment' not in st.session_state:
        st.session_state.sentiment = None
    if 'validation' not in st.session_state:
        st.session_state.validation = None
    if 'continue_tweeting' not in st.session_state:
        st.session_state.continue_tweeting = True
    if 'logged' not in st.session_state:
        st.session_state.logged = False

    # Vérification si l'utilisateur souhaite continuer à tweeter
    if not st.session_state.continue_tweeting:
        st.write("Merci d'avoir utilisé l'application.")
        return

    # Saisie du tweet par l'utilisateur
    tweet = st.text_area("Entrez votre tweet ici:", value=st.session_state.tweet)

    # Analyse du sentiment lorsque l'utilisateur clique sur le bouton
    if st.button("Analyser le sentiment") and not st.session_state.sentiment:
        if tweet:
            # Stocker le tweet dans l'état
            st.session_state.tweet = tweet
            # Appel à l'API pour obtenir la prédiction
            response = requests.post(API_URL, json={"text": tweet})
            if response.status_code == 200:
                st.session_state.sentiment = response.json().get("sentiment")
                st.write(f"Le sentiment du tweet est: {st.session_state.sentiment}")
            else:
                st.write("Erreur lors de l'analyse du sentiment.")
        else:
            st.write("Veuillez entrer un tweet.")

    # Demande de validation de la pertinence de la prédiction
    if st.session_state.sentiment and st.session_state.validation is None:
        st.write("La prédiction est-elle correcte ?")
        if st.button("Oui", key="yes"):
            st.session_state.validation = "Oui"
        if st.button("Non", key="no"):
            st.session_state.validation = "Non"

    # Traitement de la validation
    if st.session_state.validation:
        if st.session_state.validation == "Non":
            # Envoi d'une trace au service Application Insights
            if not st.session_state.logged:
                logger.warning(f"Tweet: {st.session_state.tweet}, Sentiment: {st.session_state.sentiment}, Validation: {st.session_state.validation}")
                st.session_state.logged = True
            st.write("Merci pour votre retour. Nous avons envoyé une trace pour analyse.")
        else:
            st.write("Merci pour votre retour. La réponse a été prise en compte.")

        # Demande à l'utilisateur s'il veut entrer un autre tweet
        st.write("Voulez-vous entrer un autre tweet ?")
        if st.button("Oui", key="new_tweet_yes"):
            # Réinitialisation des états de session
            st.session_state.tweet = ""
            st.session_state.sentiment = None
            st.session_state.validation = None
            st.session_state.logged = False
            st.session_state.continue_tweeting = True
            st.experimental_rerun()  # Rafraîchir la page
        if st.button("Non", key="new_tweet_no"):
            st.session_state.continue_tweeting = False

if __name__ == "__main__":
    main()