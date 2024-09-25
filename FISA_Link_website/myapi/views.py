from django.http import JsonResponse, HttpResponse # type: ignore
from django.db import connection, DatabaseError # type: ignore
from datetime import datetime
from django.contrib.auth import authenticate # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore
from django.contrib.auth.hashers import check_password # type: ignore
import json
from django.shortcuts import redirect # type: ignore
from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from django.utils.html import format_html # type: ignore
import uuid

@csrf_exempt
def verif_token_user(request):
    auth_token = request.COOKIES.get('auth_token')
    if not auth_token:
        return None
    try:
        # Requête SQL pour récupérer les informations de l'utilisateur à partir du auth_token
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT students.first_name, students.fisa_year, students.id, students.email_tsp
                FROM users 
                INNER JOIN students ON students.id = users.student_id 
                WHERE users.auth_cookie = %s
            """, [auth_token])
            result = cursor.fetchone()
        return result
    except Exception as e:
            return None

def genererate_token(user):
    token = uuid.uuid4().hex
    token_concatene = f"{user}{token}"
    return token_concatene

def envoyer_email_validation(destinataire, token):
    # Construction du lien de validation
    lien_validation = f"https://fisa-link.duckdns.org/api/verify-email/?t={token}"
    
    # Sujet et corps de l'email
    sujet = "[FISA Link] Validation de votre adresse email"
    message_html = f"""
        <html>
        <body>
            <p>Bonjour,</p>
            <p>Merci de vous être inscrit. Veuillez cliquer sur le lien suivant pour valider votre adresse email :</p>
            <p><a href="{lien_validation}">{lien_validation}</a></p>
            <p>Si vous n'avez pas demandé cette vérification, veuillez contacter <a href="mailto:crahier@telecom-sudparis.eu">crahier@telecom-sudparis.eu</a>.</p>
            <p>Cordialement,<br>L'équipe FISA-Link</p>
        </body>
        </html>
    """

    # Envoyer l'email
    send_mail(
        sujet,
        "",  # Le message textuel peut être vide car nous utilisons un format HTML
        settings.DEFAULT_FROM_EMAIL,
        [destinataire],
        html_message=message_html,  # Envoi du message au format HTML
        fail_silently=False,  # Affiche une erreur en cas d'échec
    )

def envoyer_email_inscription_SIF(destinataire, prenom):
    # Sujet et corps de l'email
    sujet = "[FISA Link] Inscription SIF"
    message_html = f"""
        <html>
        <body>
            <p>Bonjour {prenom},</p>
            <p>Votre inscription pour le SIF a bien été prises en compte.</p>
            <p>Pour toutes informations supplémentaires, veuillez contacter <a href="mailto:crahier@telecom-sudparis.eu">crahier@telecom-sudparis.eu</a>.</p>
            <p>Cordialement,<br>L'équipe FISA-Link</p>
        </body>
        </html>
    """

    # Envoyer l'email
    send_mail(
        sujet,
        "",  # Le message textuel peut être vide car nous utilisons un format HTML
        settings.DEFAULT_FROM_EMAIL,
        [destinataire],
        html_message=message_html,  # Envoi du message au format HTML
        fail_silently=False,  # Affiche une erreur en cas d'échec
    )

def envoyer_email_desinscription_SIF(destinataire, prenom):
    # Sujet et corps de l'email
    sujet = "[FISA Link] Désinscription SIF"
    message_html = f"""
        <html>
        <body>
            <p>Bonjour {prenom},</p>
            <p>Votre désinscription pour le SIF a bien été prises en compte.</p>
            <p>Cordialement,<br>L'équipe FISA-Link</p>
        </body>
        </html>
    """

    # Envoyer l'email
    send_mail(
        sujet,
        "",  # Le message textuel peut être vide car nous utilisons un format HTML
        settings.DEFAULT_FROM_EMAIL,
        [destinataire],
        html_message=message_html,  # Envoi du message au format HTML
        fail_silently=False,  # Affiche une erreur en cas d'échec
    )

@csrf_exempt
def get_users(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, is_active, date_joined FROM users")
        rows = cursor.fetchall()
    # Préparez les données pour JSON
    users = [
        {
            "id": row[0],
            "is_active": row[1],
            "date_joined": row[2].isoformat() if isinstance(row[2], datetime) else row[2]
        }
        for row in rows
    ]
    
    return JsonResponse(users, safe=False)

@csrf_exempt
def validate_mail(request) :
    token = request.GET.get('t')
    if token:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id 
                    FROM users  
                    WHERE token = %s
                """, [token])
                id = cursor.fetchone()
                
            if id :
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE users
                        SET is_active = 1
                        WHERE id = %s
                    """, [id])
                return redirect('https://fisa-link.duckdns.org/mail_valide')
            else :
                return JsonResponse({'status': 'error', 'message': 'Lien d\'activation du mail erroné'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        nom = data.get('nom')
        prenom = data.get('prenom')
        try:
            # Requête SQL pour récupérer l'utilisateur et son mot de passe haché
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT users.id, password, is_active 
                    FROM users 
                    INNER JOIN students ON students.id = users.student_id 
                    WHERE email_tsp = %s
                """, [email])
                result = cursor.fetchone()
            if not result :
                try:
                    # Requête SQL pour récupérer l'utilisateur et son mot de passe haché
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT users.id, password, is_active 
                            FROM users 
                            INNER JOIN students ON students.id = users.student_id 
                            WHERE first_name = %s and last_name=%s
                        """, [prenom,nom])
                        result = cursor.fetchone()
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})
            if result:
                db_id, db_hashed_password, is_active = result
                
                # Vérification du mot de passe en utilisant check_password + VERIFIACATION EMAIL
                if check_password(password, db_hashed_password):
                    if is_active:
                        # Créer un token ou identifiant unique pour l'authentification
                        auth_token = get_random_string(32)  # Exemple de génération d'un token aléatoire

                        # Mettre à jour la colonne auth_cookie dans la table users
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                UPDATE users
                                SET auth_cookie = %s
                                WHERE id = %s
                            """, [auth_token, db_id])

                        # Définir une réponse HttpResponse avec un cookie
                        response = HttpResponse(json.dumps({'status': 'success', 'message': 'Connexion réussie!'}), content_type="application/json")

                        # Créer un cookie avec le token d'authentification
                        response.set_cookie(
                            key='auth_token',  # Nom du cookie
                            value=auth_token,  # Valeur du cookie (token généré)
                            max_age=2592000,  # Expiration en secondes (30 jours ici)
                            httponly=True,  # Empêcher JavaScript d'accéder à ce cookie
                            samesite='Lax'  # Améliorer la sécurité en restreignant l'envoi du cookie
                        )

                        return response
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Compte inactif ! Veuillez valider votre compte par email'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Mot de passe incorrect'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Utilisateur non trouvé'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            # Récupérer les données du POST
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            fisa_year = data.get('fisa_year')
            password = data.get('password')

            # Rechercher l'étudiant correspondant
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM students WHERE first_name=%s AND last_name=%s AND fisa_year=%s",
                    [first_name, last_name, fisa_year]
                )
                student_ids = cursor.fetchall()
            if len(student_ids) == 0:
                return JsonResponse({'error': 'Aucun etudiant correspondant trouve.'}, status=404)
            elif len(student_ids) > 1:
                return JsonResponse({'error': 'Plus d un étudiant trouve, verifiez les informations.'}, status=400)

            # Si un étudiant est trouvé, on récupère l'ID
            student_id = student_ids[0][0]

            # Vérifier si un utilisateur existe déjà pour cet étudiant
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id,is_active FROM users WHERE student_id=%s", [student_id]
                )
                existing_user = cursor.fetchone()
            if existing_user:
                user_id, is_active = existing_user
            else:
                user_id, is_active = None, None
                
            if user_id and is_active == 0:
                return JsonResponse({'message': 'Utilisateur enregistré avec succès ! Veuillez valider votre compte avec l email envoyé sur votre compte TSP.'})
            if user_id:
                return JsonResponse({'error': f'Un compte existe deja pour {first_name} {last_name}.'}, status=400)

            # Hacher le mot de passe avec la fonction make_password
            hashed_password = make_password(password)

            token = genererate_token(student_id)
            # Insérer l'utilisateur dans la table users
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (password, student_id, token) VALUES (%s, %s, %s)",
                    [hashed_password, student_id, token]
                )
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT email_tsp FROM students WHERE id=%s", [student_id]
                )
                result = cursor.fetchone()
                
                if result:
                    email_tsp = result[0]  # Accède au premier élément du tuple
                else:
                    return JsonResponse({'error': 'Email non trouvé pour cet étudiant.'}, status=404)

            # Envoie l'email de vérification
            #envoyer_email_validation(email_tsp, token)
            
            return JsonResponse({'message': 'Utilisateur enregistré avec succès ! Veuillez valider votre compte avec l email envoyé sur votre compte TSP (ou si en local UPDATE à 1 is_active de votre compte).'})
        
        except DatabaseError as e:
            return JsonResponse({'error': f'Erreur de base de données : {str(e)}'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erreur de décodage JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Une erreur inattendue est survenue : {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def load_link(fisa_year):
    # Requête SQL pour récupérer les liens
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT data_link.fisa_year, data_link.type, data_link.link, data_link.title, data_link.desc
            FROM data_link 
            WHERE fisa_year = 0 OR fisa_year = %s
            order by fisa_year ASC
        """, [fisa_year])
        # Récupérer tous les résultats
        links = cursor.fetchall()

    # Transformer les résultats en un format dict pour un retour JSON
    links_data = []
    for link in links:
        link_data = {
            'fisa_year': link[0],
            'type': link[1],
            'url': link[2],
            'title': link[3],
            'description': link[4]
        }
        links_data.append(link_data)

    return links_data

@csrf_exempt
def dashboard(request):
    if request.method == 'POST':
        result = verif_token_user(request)

        if result:
            first_name = result[0].title()  # Prénom
            fisa_year = int(result[1])  # Année FISA

            # Récupérer les liens correspondant à l'année FISA
            links = load_link(fisa_year)

            # Retourner les informations de l'utilisateur et les liens
            return JsonResponse({
                'status': 'success',
                'prenom': first_name,
                'links': links,  # Envoi des liens récupérés
            })
        else:
            response = JsonResponse({'status': 'error', 'message': 'Token invalide'})
            response.delete_cookie('auth_token')
            return response
    

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@csrf_exempt
def auto_login(request):
    if request.method == 'POST':
        try:
            auth_token = request.COOKIES.get('auth_token')
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Erreur de récupération du cookie'})
        if auth_token:
            return JsonResponse({'status': 'success', 'message': 'Token valide'})
        return JsonResponse({'status': 'error', 'message': 'Token manquant'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def logout_user(request):
    # Vérifie que la requête est une requête POST
    if request.method == 'POST':
        # Créer une réponse JSON
        response = JsonResponse({'status': 'success', 'message': 'Déconnexion réussie!'})

        # Supprimer le cookie d'authentification en le définissant avec une durée de vie nulle
        response.delete_cookie('auth_token')

        # Retourner la réponse avec le cookie supprimé
        return response

    # Si la méthode n'est pas POST, renvoyer une réponse avec une erreur
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def get_bungalow_infos():
    # Récupère les infos générales sur le SIF
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT first_name, last_name, bungalow, pizza 
                    FROM SIF 
                    INNER JOIN students ON SIF.student_id = students.id 
                """)
                result_sif = cursor.fetchall()  # Utilisez fetchall() pour récupérer toutes les lignes

                # Dictionnaire pour stocker les personnes par bungalow
                list_bungalows = {}

                for row in result_sif:
                    # Assurez-vous que vous décompressez exactement autant d'éléments que la ligne contient
                    if len(row) == 4:
                        first_name, last_name, bungalow, pizza = row
                        unique_name = f"{first_name.title()} {last_name[0].title()}"

                        # Créez une clé pour le bungalow dans le dictionnaire s'il n'existe pas
                        if bungalow not in list_bungalows:
                            list_bungalows[bungalow] = set()

                        # Ajoutez le nom unique à la liste correspondante
                        list_bungalows[bungalow].add(unique_name)
                    else:
                        # Gérer le cas où la ligne n'a pas le nombre attendu d'éléments
                        print(f"Ligne inattendue: {row}")

            # Convertir les ensembles en listes pour la réponse JSON
            return {k: list(v) for k, v in list_bungalows.items()} , unique_name

@csrf_exempt
def get_sif_status(request):
    if request.method == 'POST':
        result = verif_token_user(request)
        if result:
            first_name = result[0].title()  # Prénom
            fisa_year = int(result[1])  # Année FISA
            id_student = int(result[2])  # Id
            #Récupère les infos actuels de l'utilisateur
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT bungalow, pizza 
                    FROM SIF 
                    WHERE student_id = %s
                """, [id_student])
                result_user = cursor.fetchone()
            if result_user:
                sif = True
                user_bungalow, user_pizza = result_user
            else:
                sif = False
                bungalow = None
                pizza = None
                
            list_bungalows_serializable, unique_name = get_bungalow_infos()
            
            # Retourner les infos
            return JsonResponse({
                'status': 'success',
                'sif': sif,
                'bungalow': user_bungalow,
                'pizza': user_pizza,
                'list_bungalows': list_bungalows_serializable,
                'unique_name' : unique_name,
            })
        else:
            response = JsonResponse({'status': 'error', 'message': 'Token invalide'})
            response.delete_cookie('auth_token')
            return response
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@csrf_exempt
def set_sif_status(request):
    if request.method == 'POST':
        result = verif_token_user(request)
        if result:
            first_name = result[0].title()
            fisa_year = int(result[1])
            id_student = int(result[2])
            email_tsp = result[3]
            try:
                data = json.loads(request.body)
                sif_status = data.get('sif_status')
                
                if sif_status not in [True, False]:
                    return JsonResponse({'status': 'error', 'message': 'Invalid sif_status'}, status=400)
                
                if sif_status:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                           SELECT id FROM SIF WHERE student_id=%s
                        """, [id_student])
                        result = cursor.fetchone()
                    if result is None:
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                INSERT INTO SIF (student_id) VALUES (%s)
                            """, [id_student])
                        #envoyer_email_inscription_SIF(email_tsp, first_name)
                    return JsonResponse({'status': 'success', 'message': 'Student status inserted successfully'}, status=200)
                
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                           SELECT id FROM SIF WHERE student_id=%s
                        """, [id_student])
                        result = cursor.fetchone()
                    if result is not None :
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                DELETE FROM SIF WHERE student_id = %s
                            """, [id_student])
                        #envoyer_email_desinscription_SIF(email_tsp, first_name)
                    return JsonResponse({'status': 'success', 'message': 'Student status deleted successfully'}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
            except DatabaseError as e:
                return JsonResponse({'status': 'error', 'message': 'Database error: ' + str(e)}, status=500)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred: ' + str(e)}, status=500)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid token or user not found'}, status=401)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def set_sif_change_pizza(request):
    if request.method == 'POST':
        result = verif_token_user(request)
        if result:
            first_name = result[0].title()
            fisa_year = int(result[1])
            id_student = int(result[2])
            email_tsp = result[3]
            try:
                data = json.loads(request.body)
                sif_status = data.get('sif_status')
                pizza_status = str(data.get('pizza_status'))
                if sif_status:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE SIF
                            SET pizza = %s
                            WHERE student_id = %s;
                        """, [pizza_status, id_student])
                    return JsonResponse({'status': 'success', 'message': 'Pizza choisi id : '+str(id_student)}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Student SIF not found'}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid token or user not found'}, status=401)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def set_sif_change_bungalow(request):
    if request.method == 'POST':
        result = verif_token_user(request)
        if result:
            first_name = result[0].title()
            fisa_year = int(result[1])
            id_student = int(result[2])
            email_tsp = result[3]
            try:
                # Charger les données JSON depuis la requête
                data = json.loads(request.body)
                sif_status = data.get('sif_status')
                try :
                    bungalow_status = int(data.get('bungalow_status'))
                except :
                    bungalow_status = 0
                
                if sif_status:
                    with connection.cursor() as cursor:
                        # Exécuter la requête SQL pour compter les bungalows
                        cursor.execute("""
                            SELECT COUNT(id)
                            FROM SIF
                            WHERE bungalow = %s;
                        """, [bungalow_status])
                        
                        # Récupérer le résultat
                        result = cursor.fetchone()  # Utiliser fetchone() pour obtenir une seule valeur
                        
                        # Extraire la valeur entière du tuple
                        count = result[0] if result else 0

                    if count >= 7:
                        return JsonResponse({'status': 'success', 'message': 'Bungalow plein'}, status=200)

                    # Vérifier les conditions pour la mise à jour
                    nb_bungalow = 7
                    if (fisa_year <= 3 and bungalow_status <= nb_bungalow and bungalow_status != 7) or (fisa_year == 3 and bungalow_status <= nb_bungalow):
                        with connection.cursor() as cursor:
                            # Mettre à jour la table SIF
                            cursor.execute("""
                                UPDATE SIF
                                SET bungalow = %s
                                WHERE student_id = %s;
                            """, [bungalow_status, id_student])
                        
                        return JsonResponse({'status': 'success', 'message': 'Bungalow choisi'}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Choisissez un bungalow dispo'}, status=200)
                
                return JsonResponse({'status': 'error', 'message': 'Student SIF not found'}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
            
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid token or user not found'}, status=401)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_paiement_sif(request):
    if request.method == 'POST':
        result = verif_token_user(request)
        if result:
            paypal_img = "paypal_(2024091695707).jpg"
            paypal_link = "https://paypal.me/Corentinrhr?country.x=FR&locale.x=en_US"
            lydia_img ="lydia_(2024091695707).jpg"
            lydia_link = "https://lydia-app.com/pots?id=65892-sif-2024"
            paylib_number = "07 50 99 23 62"
            paylib_img = "paylib_(2024091695707).jpg"
            return JsonResponse({
                'status': 'success',
                'paypal_img': paypal_img,
                'paypal_link': paypal_link,
                'lydia_img': lydia_img,
                'lydia_link': lydia_link,
                'paylib_img' : paylib_img,
                'paylib_number' : paylib_number
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)