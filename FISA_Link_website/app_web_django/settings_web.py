from .settings import *

# Désactiver l'application API
INSTALLED_APPS.remove('myapi')  # Supprimer l'API des applications pour le site web
