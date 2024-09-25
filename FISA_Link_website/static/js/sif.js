let isConfirmed = false; // Variable pour suivre l'état de confirmation
const pizzaSelect = document.getElementById('pizza-select');
const sifCheckbox = document.getElementById('sif-checkbox');
const bungalowSelect = document.getElementById('bungalow-select');

//Au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Récupérer le prénom de l'utilisateur
    start();
});

function start (){
    const CSRFtoken = getCSRFToken();
    fetch('/api/dashboard/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFtoken
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
            //Récupérer l'état de la réservation SIF
            getSIFstatus(CSRFtoken);
        } else {
            alert('Authentification expirée. Veuillez vous reconnecter.');
            window.location.href = '/';
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Une erreur est survenue lors de la récupération des données.');
    });

    // Ajouter un écouteur d'événement à la liste déroulante
    pizzaSelect.addEventListener('change', function() {
        const selectedPizza = pizzaSelect.value;  // Valeur de la pizza sélectionnée
        const sifStatus = sifCheckbox.checked;    // True si la checkbox est cochée, False sinon

        // Si aucune pizza n'est sélectionnée, ne pas envoyer la requête
        if (!selectedPizza) {
            return;
        }

        // Appeler la fonction pour envoyer la requête API
        changePizzaStatus(CSRFtoken, sifStatus, selectedPizza);
    });

    // Ajouter un écouteur d'événement à la liste déroulante
    bungalowSelect.addEventListener('change', function() {
        const selectedBungalow = bungalowSelect.value;  // Valeur du bungalow sélectionné
        const sifStatus = sifCheckbox.checked;          // True si la checkbox est cochée, False sinon

        // Si aucun bungalow n'est sélectionné, ne pas envoyer la requête
        if (!selectedBungalow) {
            return;
        }

        // Appeler la fonction pour envoyer la requête API
        changeBungalowStatus(CSRFtoken, sifStatus, selectedBungalow);
    });
}

function getSIFstatus(CSRFtoken) {
    fetch('/api/get_sif_status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFtoken
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
            // Mise à jour de la case à cocher "SIF"
            document.getElementById('sif-checkbox').checked = data.sif;
            
            // Mise à jour de la sélection de pizza
            const pizzaSelect = document.getElementById('pizza-select');
            if (data.pizza) {
                pizzaSelect.value = data.pizza;
            } else {
                pizzaSelect.value = '';
            }
            defaultBungalowOptions();
            // Mise à jour de la sélection de bungalow
            const bungalowSelect = document.getElementById('bungalow-select');
            if (data.bungalow) {
                bungalowSelect.value = data.bungalow;
            } else {
                bungalowSelect.value = '';
            }

            // Ajouter les noms uniques dans chaque bungalow
            const bungalowOptions = bungalowSelect.options;
            for (let i = 0; i < bungalowOptions.length; i++) {
                const option = bungalowOptions[i];
                const bungalowValue = option.value;
                if (data.list_bungalows[bungalowValue]) {
                    option.textContent  += ` (${data.list_bungalows[bungalowValue].join(', ')})`;
                }
            }

            // Afficher les conteneurs si nécessaires
            document.getElementById('sif-inscription-container').style.display = data.sif ? 'block' : 'none';
            if(data.sif){
                insererQRCodes();
            }
        } else {
            alert('Erreur dans la récupération des données de status de réservation SIF.');
        }
    })
    .catch(error => {
        bungalowSelect.value = '';
        pizzaSelect.value = '';
        document.getElementById('sif-checkbox').checked = False;
    });
}

function changeBungalowStatus(CSRFtoken, sifStatus, selectedBungalow) {
    fetch('/api/set_sif_change_bungalow/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFtoken
        },
        body: JSON.stringify({
            'sif_status': sifStatus,
            'bungalow_status': selectedBungalow
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            getSIFstatus(CSRFtoken);
            console.log('Statut Bungalow mis à jour avec succès');
        } else {
            alert(data.message || 'Erreur lors de la mise à jour du bungalow et du statut SIF.');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert(`Une erreur est survenue : ${error.message}`);
    });
}

//Au changement de status de la checkbox
document.getElementById('sif-checkbox').addEventListener('change', function() {
    if (this.checked) {
        // Afficher la modale Bootstrap lorsque la case est cochée
        $('#confirmationModal').modal('show');
    } else {
        $('#confirmUnsubscribeModal').modal('show');
        // Masquer les listes déroulantes si la case est décochée
    }
});

// Événement pour le bouton "Se désinscrire"
document.getElementById('confirm-unsubscribe-button').addEventListener('click', function() {
    isConfirmed = true;
    const CSRFtoken = getCSRFToken();
    change_sif_status(CSRFtoken, false);
    $('#confirmUnsubscribeModal').modal('hide');
    document.getElementById('sif-inscription-container').style.display = 'none';
});

// Fonction pour envoyer la requête API
function changePizzaStatus(CSRFtoken, sifStatus, selectedPizza) {
    fetch('/api/set_sif_change_pizza/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFtoken
        },
        body: JSON.stringify({
            'sif_status': sifStatus,
            'pizza_status': selectedPizza
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            getSIFstatus(CSRFtoken);
            console.log('Statut Pizza mis à jour avec succès');
        } else {
            alert(data.message || 'Erreur lors de la mise à jour de la pizza et du statut SIF.');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert(`Une erreur est survenue : ${error.message}`);
    });
}

function change_sif_status(CSRFtoken, sif_status) {
    fetch('/api/set_sif_status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFtoken
        },
        body: JSON.stringify({
            'sif_status': sif_status
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            console.log(data.message);
            getSIFstatus(getCSRFToken());
        } else {
            alert(data.message || 'Erreur dans la mise à jour des données de status de réservation SIF.');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert(`Une erreur est survenue : ${error.message}`);
    });
}

// Événement pour le bouton "Confirmer" l'inscription
document.getElementById('confirm-button').addEventListener('click', function() {
    isConfirmed = true;

    // Afficher les listes déroulantes lorsque l'utilisateur confirme
    document.getElementById('sif-inscription-container').style.display = 'block';
    $('#confirmationModal').modal('hide');

    // Change SIF participation status à Vrai
    change_sif_status(getCSRFToken(), true);
});

// Fonction réutilisable pour réinitialiser les éléments
function resetModalState() {
    const checkbox = document.getElementById('sif-checkbox');
    // Inverser l'état de la case à cocher
    checkbox.checked = !checkbox.checked;
    document.getElementById('sif-inscription-container').style.display = 'none';
}

// Événement pour le bouton "Annuler"
document.querySelector('.btn-secondary').addEventListener('click', function() {
    isConfirmed = false;
    resetModalState();
    $('#confirmationModal').modal('hide');
});

// Événement lorsque la modale est fermée (par la croix, Esc, ou clic en dehors)
$('#confirmationModal').on('hide.bs.modal', function () {
    // Seulement réinitialiser si la confirmation n'a pas eu lieu
    if (!isConfirmed) {
        resetModalState();
    }
});
$('#confirmUnsubscribeModal').on('hide.bs.modal', function () {
    // Seulement réinitialiser si la confirmation n'a pas eu lieu
    if (!isConfirmed) {
        resetModalState();
        document.getElementById('sif-inscription-container').style.display = 'block';
    }
});

// Fonction pour insérer des options dans le select et supprimer celles existantes
function defaultBungalowOptions() {
    const bungalowSelect = document.getElementById('bungalow-select'); // Récupère l'élément select

    // Efface toutes les options existantes
    bungalowSelect.innerHTML = '';

    // Tableau des options à insérer
    const bungalowOptions = [
        { value: "", text: "Sélectionnez..." },
        { value: "1", text: "Bungalow 1 " },
        { value: "2", text: "Bungalow 2 " },
        { value: "3", text: "Bungalow 3 " },
        { value: "4", text: "Bungalow 4 " },
        { value: "5", text: "Bungalow 5 " },
        { value: "6", text: "Bungalow 6 " },
        { value: "7", text: "Bungalow 7 [Réservé 3A] " }
    ];

    // Ajoute chaque option dans le select
    bungalowOptions.forEach(optionData => {
        const option = document.createElement('option');
        option.value = optionData.value;
        option.textContent = optionData.text;
        bungalowSelect.appendChild(option);
    });
}

// Fonction pour insérer les QR codes et liens dans un conteneur existant
function insererQRCodes() {
    const CSRFtoken = getCSRFToken();  // Récupérer le token CSRF

    // Effectuer la requête POST pour récupérer les données
    fetch('/api/get_paiement_sif/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFtoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('La requête réseau a échoué : ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            // Sélectionner le conteneur existant dans la page
            const container = document.querySelector('.qr-code-container');

            // Vérifier que le conteneur existe
            if (!container) {
                console.error('Le conteneur qr-code-container est introuvable dans la page.');
                return;
            }

            // Vider le conteneur de son contenu actuel
            container.innerHTML = '';  

            // Liste des services et leurs données
            const services = [
                { img: data.paypal_img, link: data.paypal_link, name: 'PayPal' },
                { img: data.lydia_img, link: data.lydia_link, name: 'Lydia' },
                { img: data.paylib_img, link: 'tel:' + data.paylib_number, name: 'Paylib' }
            ];

            services.forEach(service => {
                // Créer un élément pour le lien
                const linkElement = document.createElement('a');
                linkElement.href = service.link;
                linkElement.classList.add('qr-code-link');
            
                // Créer un élément pour l'image
                const imgElement = document.createElement('img');
                imgElement.src = '/static/images/' + service.img;  // Construire l'URL de l'image
                imgElement.alt = service.name + ' QR code';
                imgElement.classList.add('qr-code-image');
            
                // Créer un élément pour le texte
                const textElement = document.createElement('span');
                
                if (service.name === "Paylib") {
                    textElement.innerHTML = "Payer avec PayLib <br>" + data.paylib_number;
                } else {
                    textElement.textContent = 'Payer avec ' + service.name;
                }
                
                textElement.classList.add('qr-code-text');
            
                // Ajouter l'image et le texte à l'intérieur du lien
                linkElement.appendChild(imgElement);
                linkElement.appendChild(textElement);
            
                // Créer un conteneur pour chaque item (image + lien)
                const itemContainer = document.createElement('div');
                itemContainer.classList.add('qr-code-item');
                itemContainer.appendChild(linkElement);
            
                // Ajouter l'item au conteneur principal
                container.appendChild(itemContainer);
            });
            
            
            
        } else {
            // Si la réponse API est un échec
            alert('Authentification expirée. Veuillez vous reconnecter.');
            window.location.href = '/';
        }
    })
    .catch(error => {
        // Gestion des erreurs de requête
        console.error('Erreur:', error);
        alert('Une erreur est survenue lors de la récupération des données.');
    });
}


// Fonction pour obtenir le token CSRF
function getCSRFToken() {
    const csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfTokenInput ? csrfTokenInput.value : '';
}