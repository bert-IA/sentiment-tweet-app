# sentiment-tweet-app

## Description
La société "A..P....." souhaite gérer son image et pouvoir intervenir en cas de tweets négatifs trop nombreux. Ce projet permet de détecter les sentiments des tweets afin de prendre des mesures appropriées.

Ce projet déploie une application FastAPI `main.py` sur Heroku pour l'analyse de sentiment des tweets. L'application utilise le fichier model.py pour analyser un tweet avec SpaCy pour le traitement du langage naturel et scikit-learn pour les prédictions. Une application Streamlit `app_test_heroku.py` est également implémentée et permet à un utilisateur en local d'entrer un tweet et d'obtenir le sentiment prédit par le modèle via l'application FASTAPI déployée. Une demande de validation de la prédiction est executée et les informations sont envoyées sous forme de log à une application Azure insights.


## Structure du projet

```
model_dep_hero_test/
├── app/
│   ├── main.py          # Application FastAPI déployée sur heroku
│   ├── model/
│   │   ├── model.py     # Fonction de prédiction utilisant SpaCy
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── __init__.py      
│   └── test_app.py      # scripts des 3 tests unitaires avant deploiement sur heroku
├── Procfile             # Fichier de configuration pour Heroku
├── .dockerignore        # Fichiers et répertoires à ignorer par Docker
├── heroku.yml           # Fichier de configuration pour le déploiement sur Heroku
├── app_test_local.py    # Application Streamlit pour une utilisation locale
├── app_test_heroku.py   # Reçoit et envoie les donées des tweets à l'application insigths
├── Dockerfile           # Fichier de configuration pour Docker
├── requirements.txt     # Liste des dépendances Python
├── run_tests.sh         # Script pour exécuter les tests unitaires avant de démarrer l'application
└── README.md            # Documentation du projet
```



## Déploiement de l'application sur Heroku

Le projet de déploiement de l'application FASTAPI `main.py` a été géré avec Git, permettant de suivre différentes versions des fichiers. Un conteneur Docker a été utilisé pour le déploiement, assurant une cohérence de l'environnement de développement à la production.

L'application déployée `sentiment-app-1` a été créée avec le CLI d'Heroku, puis connectée au repository GitHub. Un déploiement automatique a été configuré pour que chaque push vers la branche principale du repository déclenche un nouveau déploiement sur Heroku.

Avant que le déploiement soit executé, un test de vérification de la version du modèle, des prédictions correctes d'un tweet positif et d'un tweet négatif est mis en place. En cas d'échec le déploiement de l'applicatin FASTAPI est annulé.

### Utilisation de l'application streamlit

Pour utiliser l'application Streamlit avec l'application déployée sur Heroku, exécutez :
```sh
streamlit run app_test_heroku.py
```

### Fonction de l'application Streamlit (app_test_heroku.py)

L'application Streamlit est définie dans `app_test_heroku.py` et permet aux utilisateurs d'entrer un tweet et de connaître le sentiment du tweet prédit par le modèle : [`tweet_positif`] pour un client content et [`tweet_négatif`] pour un client mécontent.
L'application demande ensuite à l'utilisateur si la prédiction est correcte ou non.
Elle envoie alors un log à l'application Azure insights avec le tweet, le sentiment et un boolean de validation si la prédiction est valide ou non.  

**NB :** Une application Streamlit `apli.py` a été créée pour tester l'application FastAPI local.

## Tests et alertes 
### Précisions sur les tests unitaires avant le déploiement

Des tests unitaires ont été mis en place pour vérifier que l'application fonctionne correctement et que le modèle analyse correctement les tweets. Les tests incluent :

- Un test de vérification de l'état de santé de l'application (`/`).
- Un test de prédiction positive pour un tweet positif.
- Un test de prédiction négative pour un tweet négatif.

Les tests sont exécutés automatiquement avant le démarrage de l'application sur Heroku. Si les tests échouent, le déploiement est annulé.
Ils sont gérés dans le script `run_tests.sh` qui via le package pytest execute le script dans `test_app.py`.

### Configuration des alertes automatiques sur Azure 

Une alerte a été mise en place par l'envoi d'un mail au développeur de l'application en cas de trois tweets négatifs dans un intervalle de 5 minutes.
```



