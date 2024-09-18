FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Forcer la réinstallation de numpy pour éviter les incompatibilités binaires
RUN pip install --no-cache-dir --upgrade --force-reinstall numpy

# Télécharger le modèle de langue anglais de spacy
RUN python -m spacy download en_core_web_sm

# Copier le reste de l'application
COPY ./app /app/app

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8080

# Définir les variables d'environnement
ENV PORT=8080
ENV HOST=0.0.0.0

# Commande pour démarrer l'application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]