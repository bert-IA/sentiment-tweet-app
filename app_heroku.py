import streamlit as st
import requests

# l'URL l'application Heroku
API_URL = "https://sentiment-app-1-42e90bfa5057.herokuapp.com/predict"

# URL du service Application Insights
APP_INSIGHTS_URL = "http://localhost:8000/app_insights"  


def main():
    st.title("Analyse de Sentiment de Tweet")

    # Initialisation des états
    if 'tweet' not in st.session_state:
        st.session_state.tweet = ""
    if 'sentiment' not in st.session_state:
        st.session_state.sentiment = None
    if 'validation' not in st.session_state:
        st.session_state.validation = None
    if 'continue_tweeting' not in st.session_state:
        st.session_state.continue_tweeting = True

    if not st.session_state.continue_tweeting:
        st.write("Merci d'avoir utilisé l'application.")
        return

    # Saisie du tweet par l'utilisateur
    tweet = st.text_area("Entrez votre tweet ici:", value=st.session_state.tweet)

    if st.button("Analyser le sentiment"):
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

    if st.session_state.sentiment and st.session_state.validation is None:
        # Demande de validation de la pertinence de la prédiction
        if st.button("Oui", key="yes"):
            st.session_state.validation = "Oui"
        if st.button("Non", key="no"):
            st.session_state.validation = "Non"

    if st.session_state.validation:
        if st.session_state.validation == "Non":
            # Envoi d'une trace au service Application Insights
            requests.get(APP_INSIGHTS_URL, params={"tweet": st.session_state.tweet, "sentiment": st.session_state.sentiment, "validation": st.session_state.validation})
            st.write("Merci pour votre retour. Nous avons envoyé une trace pour analyse.")
        else:
            st.write("Merci pour votre retour. La réponse a été prise en compte.")

        # Demande à l'utilisateur s'il veut entrer un autre tweet
        st.write("Voulez-vous entrer un autre tweet ?")
        if st.button("Oui", key="new_tweet_yes"):
            st.session_state.tweet = ""
            st.session_state.sentiment = None
            st.session_state.validation = None
            st.experimental_rerun()
        if st.button("Non", key="new_tweet_no"):
            st.session_state.continue_tweeting = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()