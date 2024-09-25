    // Gérer la déconnexion
    document.getElementById('logout-button').addEventListener('click', function(event) {
        event.preventDefault();
        // Supprimer le cookie auth_token côté serveur
        fetch('/api/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(() => {
            // Rediriger vers la page de connexion après déconnexion
            window.location.href = '/';
        });
    });