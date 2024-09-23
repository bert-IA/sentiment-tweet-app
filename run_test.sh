#!/bin/bash
# run_tests.sh

# Exécuter les tests unitaires
pytest tests/

# Si les tests échouent, arrêter le déploiement
if [ $? -ne 0 ]; then
  echo "les tests ont échoué. Déployement annulé."
  exit 1
fi

# Si les tests réussissent, démarrer l'application
exec "$@"