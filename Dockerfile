FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copier le fichier nltk.txt et le script de téléchargement
COPY nltk.txt .
COPY download_data_nltk.py .

# Exécuter le script pour télécharger les ressources NLTK
RUN python download_data_nltk.py

# Copier le reste de l'application
COPY ./app /app/app

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8080

# Définir les variables d'environnement
ENV PORT=8080
ENV HOST=0.0.0.0
ENV NLTK_DATA=/usr/local/share/nltk_data

# Commande pour démarrer l'application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]