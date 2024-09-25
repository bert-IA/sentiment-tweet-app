import streamlit as st
import requests

# l'URL de votre application Heroku
API_URL = "https://sentiment-app-1-42e90bfa5057.herokuapp.com/predict"

# URL du service Application Insights
APP_INSIGHTS_URL = "http://localhost:8000/app_insights"  # Remplacez par l'URL de votre service Application Insights

def main():
    st.title("Analyse de Sentiment de Tweet")

    # Saisie du tweet par l'utilisateur
    tweet = st.text_area("Entrez votre tweet ici:")

    if st.button("Analyser le sentiment"):
        if tweet:
            # Appel à l'API pour obtenir la prédiction
            response = requests.post(API_URL, json={"text": tweet})
            if response.status_code == 200:
                sentiment = response.json().get("sentiment")
                st.write(f"Le sentiment du tweet est: {sentiment}")

                # Demande de validation de la pertinence de la prédiction
                validation = st.radio("La prédiction est-elle pertinente ?", ["Oui", "Non"])
                if validation == "Non":
                    # Envoi d'une trace au service Application Insights
                    requests.get(APP_INSIGHTS_URL, params={"tweet": tweet, "sentiment": sentiment, "validation": validation})
                    st.write("Merci pour votre retour. Nous avons envoyé une trace pour analyse.")
            else:
                st.write("Erreur lors de l'analyse du sentiment.")
        else:
            st.write("Veuillez entrer un tweet.")

if __name__ == "__main__":
    main()