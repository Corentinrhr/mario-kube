# FISA_Link
Site web Django pour le projet "Architectures distribuées et application web" en FISA à TSP.

# Prérequis 
Version de Docker-compose > 2.0 (vous pouvez vérifiez votre version avec `docker-compose --version`)

# Lancement du projet Django
`sudo docker-compose up --build --remove-orphans`

# Schéma de ma base de données
<p align="center">
    <img src="https://github.com/Corentinrhr/FISA_Link/blob/main/BD/Sch%C3%A9ma_Relationnel_BD.png?raw=true" alt="Base de données">
</p>

# Schéma infra réseau
<p align="center">
    <img src="https://github.com/Corentinrhr/FISA_Link/blob/main/schema_infra_reseau.png?raw=true" alt="Infra res docker">
</p>

# Réponses aux questions

## Fonctionnement de Django

### Affichage de la page index.html
Lorsqu'un utilisateur accède à l'URL `/`, Django reçoit cette requête et cherche une correspondance dans le fichier `urls.py` de l'application `app_web_django`. Ce fichier inclut les `urls.py` des 2 autres applications `main` et `myapi`. Cela redirige ensuite la requête vers une vue située dans `main/views.py` ou `myapi/views.py` selon l'url. Cette vue est responsable de rendre les pages web ou requetes API. En particulier, pour `index.html`, celle-ci est stockée dans le répertoire `templates/index.html`. Une fois le template rendu, la vue renvoie la page HTML au navigateur de l'utilisateur. En plus des fichiers `views.py`, `urls.py` et `index.html`, le fichier `settings.py` est également utile pour indiquer à Django où chercher les templates.

### Configuration de la base de données
La configuration de la base de données que l'on souhaite utiliser dans un projet Django se fait dans le fichier `settings.py`, dans la section nommée `DATABASES`. C'est ici que l'on définit les paramètres nécessaires, comme le type de base de données (par exemple PostgreSQL ou SQLite), l'hôte, le port, le nom de la base de données, ainsi que les informations d'authentification comme l'utilisateur et le mot de passe.

### Configuration du fichier de paramètres
Le fichier principal pour les paramètres est `settings.py`, où sont définis les réglages globaux du projet. Il existe aussi `wsgi.py` ou `asgi.py`, qui permettent de gérer la communication entre le serveur web et Django, jouant le rôle de point d'entrée pour les requêtes. Enfin, le fichier `manage.py` est utilisé pour exécuter diverses commandes Django, tout en prenant en compte les paramètres définis dans `settings.py`.

### Effet des commandes makemigrations et migrate
La commande `python manage.py makemigrations` permet de créer des fichiers de migration basés sur les modifications effectuées dans les modèles de votre projet Django. Ces fichiers sont stockés dans le répertoire `migrations/`. La commande `python manage.py migrate`, quant à elle, applique ces migrations à la base de données, ce qui a pour effet de modifier sa structure en fonction des modèles définis. Pendant ces exécutions, les fichiers dans le dossier `migrations/` sont utilisés, ainsi que la base de données.

## Fonctionnement de Docker

### Commandes Dockerfile
La commande `FROM` dans un Dockerfile spécifie l'image de base à partir de laquelle le conteneur sera construit, comme par exemple `python:3.10`. La commande `RUN` permet d'exécuter des instructions à l'intérieur de l'image, par exemple pour installer des dépendances. `WORKDIR` définit le répertoire de travail à l'intérieur du conteneur, ce qui simplifie l'exécution des commandes dans cet environnement. La commande `EXPOSE` sert à déclarer un port que le conteneur rend accessible, tel que le port 8000. Enfin, `CMD` définit la commande par défaut qui sera exécutée lors du démarrage du conteneur.

### Définition d'un service dans docker-compose.yml
Dans un fichier `docker-compose.yml`, la section `ports: - "80:80"` indique que le port 80 de la machine hôte est redirigé vers le port 80 du conteneur, permettant ainsi un accès à ce service depuis l'extérieur. L'instruction `build: context: . dockerfile: Dockerfile.api` spécifie que l'image doit être construite à partir du fichier `Dockerfile.api` situé dans le répertoire courant. Le paramètre `depends_on: - web - api` définit que ce service dépend du démarrage préalable des services `web` et `api`. Quant à la section `environment`, elle permet de définir des variables d'environnement, telles que les informations de connexion à PostgreSQL, directement dans le fichier `docker-compose.yml`.

### Définition des variables d'environnement
Une méthode courante pour définir des variables d'environnement dans un conteneur est d'utiliser un fichier `.env` qui contient ces variables, ou bien de les spécifier directement dans la section `environment` du fichier `docker-compose.yml`.

### Communication entre les conteneurs (nginx et web)
Lorsque plusieurs conteneurs sont sur le même réseau Docker, comme un conteneur Nginx et un conteneur web avec Django, ils peuvent communiquer en utilisant leurs noms de service. Ainsi, dans ce cas, Nginx peut accéder au serveur web Django via l'URL `http://web:8000`, sans avoir besoin d'utiliser les adresses IP des conteneurs. Cela simplifie la communication et rend le déploiement plus flexible.

# Fonctionnement du site web django
Le site charge une base de données remplies avec un étudiant FISA ayant le droit de s'inscrire sur la page http://localhost/inscription.  <br>
Vous pouvez ainsi vous inscrire avec Prénom : 'Corentin' , Nom : 'R' et Année FISA : '2A'.  <br>
Vous pouvez ensuite vous identifier avec le nom d'utilisateur 'corentin.r' et le mot de passe saisi précédemment et ainsi accéder à FISA Link et à l'inscription au SIF (Séminaire d'intégration FISA).

## Récap liste chemins URL 
### Site Web : <br>
    admin/
    [name='index']
    inscription [name='sign_up']
    mail_valide [name='mail_valide']
    dashboard [name='dashboard']
    sif [name='sif']
### API : <br>
    api/login/ [name='login_user']
    api/sign_up/ [name='register_user']
    api/verify-email/ [name='validate_mail']
    api/dashboard/ [name='dashboard']
    api/logout/ [name='logout']
    api/auto_login/ [name='auto_login']
    api/get_sif_status/ [name='get_sif_status']
    api/set_sif_status/ [name='set_sif_status']
    api/set_sif_change_bungalow/ [name='set_sif_change_bungalow']
    api/set_sif_change_pizza/ [name='set_sif_change_pizza']
    api/get_paiement_sif/ [name='get_paiement_sif']

## Accéder au site web 
http://localhost/

## Essayer l'API du site web
http://localhost/api/dashboard <br>
Note : Vous devriez avoir une erreur "Méthode non autorisée" en y accédant depuis un navigateur.

## Se connecter à la base de données
Se connecter au container mariadb
`mysql -u root -p mysql -h 127.0.0.1 -P 3306 -u root -pFISA_hcajbjaibh672983`

## Remplir la base de données
La base de données utilisée dans le site web : <br>
`USE bd_django;`

Ajouter tout d'abord des années FISA : <br>
`INSERT INTO fisa_years (year, nom_promotion) VALUES (0, 'FISA'),(2, 'Kilo'),(1, 'Lima'),(3, 'Juliet');`

Ajouter des liens à présenter : <br>
```INSERT INTO data_link (fisa_year, type, link, title, `desc`, created_at) VALUES (0, 'WhatsApp', 'https://chat.whatsapp.com/EXnszNls8PN3ivAK2XTlmS', 'Whatsapp de l\'ASINT', 'Le groupe Whatsapp de l\'association sportive de TSP', '2024-09-12 13:16:56'),(0, 'Instagram', 'https://www.instagram.com/fipa_kilo?igsh=Nm8wZmZvN21lcGdn', 'Instagram FISA Kilo (2A)', 'Page Instagram des FISA Kilo. Abonnez-vous !', '2024-09-12 13:33:09'),(0, 'Web', 'https://ecampus.imtbs-tsp.eu/', 'Ecampus', 'Site web d\'accès à l\'espace personnel étudiant. Ici, vous pourrez consulter vos mails, accéder à Moodle, gérer vos impressions...', '2024-09-12 14:44:50'); ```

Pour ajouter un étudiant pouvant se créer un compte sur le site web : <br>
`INSERT INTO students (first_name, last_name, email_tsp, fisa_year) VALUES ('Corentin', 'R', 'corentin.r@telecom-sudparis.eu',2);`

Créer un compte depuis le site web avec un nom et prénom présent dans la table "students" : <br>
`http://localhost/inscription`

Note : Les mots de passe sont hashés c'est pourquoi il faut créer un mot de passe directement sur ce lien ou insérer le hash du mot de passe dans la table "users"

Identifiez-vous sur `http://localhost`, vous devriez être redirigé automatiquement sur : `http://localhost/dashboard`
