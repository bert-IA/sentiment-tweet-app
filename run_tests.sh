#!/bin/bash
# run_tests.sh
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest tests/

# Si les tests échouent, arrêter le déploiement
if [ $? -ne 0 ]; then
  echo "les tests ont échoué. Déployement annulé."
  exit 1
fi

echo "Tests passed. Proceeding with deployment."
exec "$@"
