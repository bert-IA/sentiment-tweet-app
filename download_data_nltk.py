import nltk

# Lire le fichier nltk.txt et télécharger les ressources spécifiées
with open('nltk.txt') as f:
    resources = f.read().splitlines()

# Télécharger les ressources dans le répertoire spécifié
for resource in resources:
    nltk.download(resource, download_dir='/usr/local/share/nltk_data')