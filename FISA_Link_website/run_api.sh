#!/bin/bash

# Chemin vers le répertoire du projet
PROJECT_DIR="$(dirname "$0")"
cd "$PROJECT_DIR" || { echo "Échec du changement de répertoire vers $PROJECT_DIR"; exit 1; }

# Nom de l'environnement virtuel
ENV_NAME="FISA_Link_py_env"

# Vérifier si l'environnement virtuel existe
if [ ! -d "$ENV_NAME" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv "$ENV_NAME"
fi

# Activer l'environnement virtuel
source "$ENV_NAME/bin/activate"

# Installer les dépendances
echo "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Boucle pour lancer le serveur API
while true
do
    echo "Lancement du serveur API..."
    python ./manage.py makemigrations myapi --settings=app_web_django.settings_api
    python ./manage.py runserver 0.0.0.0:8801 --settings=app_web_django.settings_api
    echo "Le serveur API a crashé. Redémarrage dans 30 secondes..."
    sleep 30
done
