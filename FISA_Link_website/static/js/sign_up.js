document.addEventListener('DOMContentLoaded', function() {
    // Sélectionner le formulaire d'inscription
    const form = document.querySelector('.login100-form');

    // Ajouter un écouteur d'événement pour le bouton "S'inscrire"
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche le rechargement de la page
        
        // Récupérer les valeurs des champs et supprimer les espaces avant et après
        let nom = document.querySelector('input[name="nom"]').value.trim();
        let prenom = document.querySelector('input[name="prenom"]').value.trim();
        const fisaYear = document.querySelector('select[name="fisa-year"]').value.trim();
        const password = document.querySelector('input[name="pass"]').value.trim();
        const confirmPassword = document.querySelector('input[name="confirm-pass"]').value.trim();

        // Transformer "nom" et "prenom" en minuscules et remplacer les espaces internes par des underscores
        nom = nom.toLowerCase().replace(/\s+/g, '_');
        prenom = prenom.toLowerCase().replace(/\s+/g, '_');

        // Vérification que les champs ne sont pas vides et que les mots de passe correspondent
        if (!nom || !prenom || !fisaYear || !password || !confirmPassword) {
            alert('Tous les champs doivent être remplis.');
            return;
        }

        if (password !== confirmPassword) {
            alert('Les mots de passe ne correspondent pas.');
            return;
        }

        // Créer les données pour la requête
        const data = {
            first_name: prenom,
            last_name: nom,
            fisa_year: fisaYear,
            password: password
        };

        console.log('Données envoyées en POST:', data);
        const csrftokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrftokenElement) {
            console.error('Token CSRF manquant.');
            return;
        }
        const csrftoken = csrftokenElement.value;

        // Envoyer une requête POST à l'API
        fetch('/api/sign_up/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken  // Ajout du token CSRF
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                // Gestion des erreurs HTTP
                return response.text().then(text => {
                    // Affichage du message d'erreur retourné par le serveur ou erreur générique
                    return Promise.reject(new Error(text || 'Une erreur est survenue lors de la requête.'));
                });
            }
            return response.json();
        })
        .then(data => {
            // Traitement des données JSON renvoyées par le serveur
            if (data.message) {
                // Afficher le message de succès
                alert(data.message);
                window.location.href = '/';  // Redirection en cas de succès
            } else if (data.error) {
                // Afficher le message d'erreur
                window.location.href = '/';  
            } else {
                // Gestion de cas inattendus
                alert('Réponse inattendue du serveur.');
            }
        })
        .catch(error => {
            // Gestion des erreurs lors de la requête
            console.error('Erreur:', error);
            alert(`Une erreur est survenue : ${error.message}`);
        });
        
        
    });
});
