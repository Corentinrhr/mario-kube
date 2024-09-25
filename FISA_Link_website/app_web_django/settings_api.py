from .settings import *

# Désactiver les applications spécifiques au site web
INSTALLED_APPS.remove('main')  # Supprimer l'application web pour le service API
