# sentiment-tweet-app

## Description
La société "A..P....." souhaite gérer son image et pouvoir intervenir en cas de tweets négatifs trop nombreux. Ce projet permet de détecter les sentiments des tweets afin de prendre des mesures appropriées.

Ce projet déploie une application FastAPI sur Heroku pour l'analyse de sentiment des tweets. L'application utilise SpaCy pour le traitement du langage naturel et scikit-learn pour les prédictions. Une application Streamlit est également implémentée et permet à un utilisateur d'entrer un tweet et d'obtenir le sentiment prédit par le modèle via l'application FASTAPI déployé sur Heroku.


## Structure du projet

```
model_dep_hero_test/
├── app/
│   ├── main.py          # Application FastAPI
│   ├── model/
│   │   ├── model.py     # Fonction de prédiction utilisant SpaCy
│   │   └── __init__.py
│   └── __init__.py
├── Procfile             # Fichier de configuration pour Heroku
├── .dockerignore        # Fichiers et répertoires à ignorer par Docker
├── heroku.yml           # Fichier de configuration pour le déploiement sur Heroku
├── apli.py              # Application Streamlit pour une utilisation locale
├── app-heroku.py        # Application Streamlit pour utiliser l'application déployée sur Heroku
├── Dockerfile           # Fichier de configuration pour Docker
├── requirements.txt     # Liste des dépendances Python
├── run_tests.sh         # Script pour exécuter les tests unitaires avant de démarrer l'application
├── tests/
│   ├── __init__.py      # Fichier pour traiter le répertoire comme un package
│   └── test_unitaire_app.py # Tests unitaires pour l'application
└── README.md            # Documentation du projet
```



## Déploiement de l'application sur Heroku

Le projet de déploiement a été géré avec Git, permettant de suivre différentes versions des fichiers. Un conteneur Docker a été utilisé pour le déploiement, assurant une cohérence de l'environnement de développement à la production.

L'application a été créée avec le CLI d'Heroku, puis connectée au repository GitHub. Un déploiement automatique a été configuré pour que chaque push vers la branche principale du repository déclenche un nouveau déploiement sur Heroku.

### Utilisation de l'application streamlit

Pour utiliser l'application Streamlit avec l'application déployée sur Heroku, exécutez :
```sh
streamlit run app-heroku.py
```

### Fonction de l'application Streamlit (app-heroku.py)

L'application Streamlit est définie dans `app-heroku.py` et permet aux utilisateurs d'entrer un tweet et de connaître le sentiment du tweet prédit par le modèle : [`tweet_positif`] pour un client content et [`tweet_négatif`] pour un client mécontent.

**NB :** Une application Streamlit [`apli.py`] a été créée pour tester l'application FastAPI en local.

## Tests unitaires

Des tests unitaires ont été mis en place pour vérifier que l'application fonctionne correctement et que le modèle analyse correctement les tweets. Les tests incluent :

- Un test de vérification de l'état de santé de l'application (`/`).
- Un test de prédiction positive pour un tweet positif.
- Un test de prédiction négative pour un tweet négatif.

Les tests sont exécutés automatiquement avant le démarrage de l'application sur Heroku. Si les tests échouent, le déploiement est annulé.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
```



