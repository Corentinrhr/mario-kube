document.getElementById('sif-button').addEventListener('click', function(event) {
    event.preventDefault();

    // Vérifier l'URL actuelle
    if (window.location.pathname === '/sif') {
        window.location.href = '/dashboard';
    } else {
        window.location.href = '/sif';
    }
});
