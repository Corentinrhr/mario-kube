document.addEventListener('DOMContentLoaded', function() {
    // Récupérer le prénom de l'utilisateur
    fetch('/api/dashboard/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            // Afficher le prénom de l'utilisateur
            document.getElementById('prenom').textContent = data.prenom;

            // Afficher les liens
            const linksContainer = document.getElementById('links-container');
            data.links.forEach(link => {
                const linkElement = createLinkElement(link);
                linksContainer.appendChild(linkElement);
            });
        } else {
            alert('Authentification expirée. Veuillez vous reconnecter.');
            window.location.href = '/';
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Une erreur est survenue lors de la récupération des données.');
    });


});

// Fonction pour vérifier si une image existe
function imageExists(imageUrl, callback) {
    const img = new Image();
    img.onload = function() { callback(true); };
    img.onerror = function() { callback(false); };
    img.src = imageUrl;
}

// Fonction pour créer un élément de lien
function createLinkElement(link) {
    const linkDiv = document.createElement('div');
    linkDiv.classList.add('link-card');  // Ajout de la classe pour le style personnalisé

    const imagePath = `/static/images/link-icons/${link.type}.png`;
    const defaultImagePath = `/static/images/link-icons/Firefox.png`;

    imageExists(imagePath, function(exists) {
        const imageToUse = exists ? imagePath : defaultImagePath;

        linkDiv.innerHTML = `
            <img src="${imageToUse}" alt="${link.type}">
            <div class="card-body">
                <h5 class="card-title">${link.title}</h5>
                <p class="card-text">${link.description}</p>
                <a href="${link.url}" class="btn btn-primary">Rejoindre</a>
            </div>
        `;
    });

    return linkDiv;
}



// Fonction pour obtenir le token CSRF
function getCSRFToken() {
    const csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfTokenInput ? csrfTokenInput.value : '';
}
