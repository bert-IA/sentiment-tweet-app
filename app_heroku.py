import streamlit as st
import requests

# Remplacez l'URL locale par l'URL de votre application Heroku
API_URL = "https://sentiment-app-1-42e90bfa5057.herokuapp.com/predict"

# Titre de l'application
st.title("Analyse de Sentiment de Tweet")

# Champ de texte pour entrer le tweet
tweet = st.text_area("Entrez votre tweet ici:")

# Bouton pour envoyer le tweet
if st.button("Analyser le sentiment"):
	if tweet:
		# Envoyer le tweet à l'API Heroku
		response = requests.post(API_URL, json={"text": tweet})
		
		if response.status_code == 200:
			# Afficher le sentiment retourné par l'API
			sentiment = response.json().get("sentiment")
			st.write(f"Le sentiment du tweet est: {sentiment}")
		else:
			st.write("Erreur lors de l'analyse du tweet.")
	else:
		st.write("Veuillez entrer un tweet.")