"""
Endpoints de gestion du calendrier Google de PlanifPro.

Ce module définit les routes REST liées à l'intégration
Google Calendar, permettant aux utilisateurs d'autoriser
l'accès et d'exporter leurs créneaux.
"""
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # DEV uniquement : autorise OAuth en HTTP local

from flask import request, redirect, session
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from google_auth_oauthlib.flow import Flow
from planifPro.backend.services.facade import PlanifProFacade

# Stockage temporaire des code_verifier PKCE, indexés par state (DEV/MVP)
verifiers_pkce = {}

facade = PlanifProFacade()

api = Namespace('calendrier', description='Opération Google Calendar')

export_model = api.model('Export', {
    'creneau_ids': fields.List(fields.String, required=True, description='IDs des créneaux à exporter')
})

SCOPES = ['https://www.googleapis.com/auth/calendar']

JOURS_VERS_BYDAY = {
    'lundi': 'MO',
    'mardi': 'TU',
    'mercredi': 'WE',
    'jeudi': 'TH',
    'vendredi': 'FR',
    'samedi': 'SA',
    'dimanche': 'SU',
}


@api.route('/auth')
class CalendrierAuth(Resource):
    """
    Resource pour générer l'URL d'autorisation Google OAuth2.
    """
    @api.response(200, 'URL d\'autorisation retournée')
    @api.response(500, 'Erreur génération URL OAuth')
    @jwt_required()
    def get(self):
        """Générer l'URL d'autorisation Google Calendar"""
        try:
            # Crée le flux OAuth2 à partir du fichier JSON de credentials Google
            flow = Flow.from_client_secrets_file(
                os.getenv('GOOGLE_CLIENT_SECRETS'),
                scopes=SCOPES,
                # URL vers laquelle Google redirigera après autorisation
                redirect_uri=os.getenv('GOOGLE_REDIRECT_URI')
            )
            # Génère l'URL de la page d'autorisation Google
            # prompt='consent' force l'affichage de la page même si déjà autorisé
            auth_url, state = flow.authorization_url(prompt='consent')
            # Associe le code_verifier au state pour le retrouver au callback
            verifiers_pkce[state] = flow.code_verifier
        except Exception as e:
            return {'error': 'Erreur génération URL OAuth'}, 500
        # Retourne l'URL au frontend qui redirigera l'utilisateur vers Google
        return {'auth_url': auth_url}, 200


@api.route('/callback')
class CalendrierCallback(Resource):
    """
    Resource pour récupérer le token Google après autorisation.
    """
    @api.response(200, 'Token stocké')
    @api.response(400, 'Code OAuth manquant ou invalide')
    @api.response(500, 'Erreur échange code contre token')
    def get(self):
        """Callback Google OAuth2"""
        try:
            flow = Flow.from_client_secrets_file(
                os.getenv('GOOGLE_CLIENT_SECRETS'),
                scopes=SCOPES,
                redirect_uri=os.getenv('GOOGLE_REDIRECT_URI')
            )
            # Retrouve le code_verifier associé au state
            state_recu = request.args.get('state')
            flow.code_verifier = verifiers_pkce.get(state_recu)
            # Récupère l'URL complète avec le code d'autorisation
            authorization_response = request.url
            flow.fetch_token(authorization_response=authorization_response)

            # Récupère et stocke les credentials
            credentials = flow.credentials
            # Redirige vers le front avec le token dans l'URL
            url_front = os.getenv('FRONTEND_URL', 'http://localhost:5173')
            return redirect(
                f"{url_front}/google-callback?access_token={credentials.token}"
            )
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/export')
class CalendrierExport(Resource):
    """
    Resource pour exporter des créneaux vers Google Calendar.
    """
    @api.expect(export_model)
    @api.response(200, 'Créneaux exportés')
    @api.response(400, 'Aucun créneau sélectionné')
    @api.response(401, 'Access token Google expiré')
    @api.response(404, 'Créneau introuvable')
    @api.response(500, 'Erreur Google Calendar API')
    @jwt_required()
    def post(self):
        """Exporter des créneaux vers Google Calendar"""
        donnees = api.payload
        creneau_ids = donnees.get('creneau_ids', [])

        if not creneau_ids:
            return {'error': 'Aucun créneau sélectionné'}, 400

        # Récupère le token Google depuis le header Authorization
        access_token = request.headers.get('X-Google-Token')
        if not access_token:
            return {'error': 'Access token Google expiré'}, 401

        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials

            # Crée les credentials Google avec le token
            credentials = Credentials(token=access_token)
            # Crée le service Google Calendar
            service = build('calendar', 'v3', credentials=credentials)

            for creneau_id in creneau_ids:
                creneau = facade.obtenir_creneau(creneau_id)
                if not creneau:
                    return {'error': f'Créneau {creneau_id} introuvable'}, 404

                # Le titre dépend du rôle : le prof voit l'élève, l'élève voit le prof
                role = get_jwt().get('role')
                if role == 'professeur':
                    # Côté prof : afficher le nom de l'élève
                    eleve = facade.obtenir_eleve(creneau['eleve_id'])
                    if eleve:
                        titre_cours = f"Cours {creneau['type']} - {eleve['prenom']} {eleve['nom']}"
                    else:
                        titre_cours = f"Cours {creneau['type']}"
                else:
                    # Côté élève : afficher le nom du professeur
                    classe = facade.obtenir_classe(creneau['classe_id'])
                    professeur = facade.obtenir_professeur(classe['professeur_id']) if classe else None
                    if professeur:
                        titre_cours = f"Cours {creneau['type']} - {professeur['prenom']} {professeur['nom']}"
                    else:
                        titre_cours = f"Cours {creneau['type']}"

                # Crée l'événement Google Calendar
                evenement = {
                    'summary': titre_cours,
                    'description': f"Créneau PlanifPro",
                    'start': {
                        'dateTime': f"{creneau['date_debut']}T{creneau['heure_debut']}",
                        'timeZone': 'Europe/Paris'
                    },
                    'end': {
                        'dateTime': f"{creneau['date_debut']}T{creneau['heure_fin']}",
                        'timeZone': 'Europe/Paris'
                    },
                    'recurrence': [
                        f"RRULE:FREQ=WEEKLY;BYDAY={JOURS_VERS_BYDAY[creneau['jour']]};UNTIL={creneau['date_fin'].replace('-', '')}T000000Z"
                    ]
                }
                # Insère l'événement dans Google Calendar
                service.events().insert(
                    calendarId='primary',
                    body=evenement
                ).execute()

        except Exception as e:
            return {'error': 'Erreur Google Calendar API'}, 500
        return {'message': 'Créneaux exportés avec succès'}, 200

    @api.response(200, 'Créneaux supprimés de Google Calendar')
    @api.response(401, 'Access token Google expiré')
    @api.response(500, 'Erreur Google Calendar API')
    @jwt_required()
    def delete(self):
        """Supprimer tous les créneaux PlanifPro de Google Calendar"""
        # Récupère le token Google depuis le header
        access_token = request.headers.get('X-Google-Token')
        if not access_token:
            return {'error': 'Access token Google expiré'}, 401

        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials

            # Crée les credentials Google avec le token
            credentials = Credentials(token=access_token)
            # Crée le service Google Calendar
            service = build('calendar', 'v3', credentials=credentials)

            # Recherche les événements contenant le marqueur PlanifPro
            events_result = service.events().list(
                calendarId='primary',
                q='Créneau PlanifPro',
                maxResults=250,
                singleEvents=False
            ).execute()

            nombre_supprimes = 0
            for event in events_result.get('items', []):
                # Vérifie la description exacte avant de supprimer (sécurité)
                if event.get('description') == 'Créneau PlanifPro':
                    service.events().delete(
                        calendarId='primary',
                        eventId=event['id']
                    ).execute()
                    nombre_supprimes += 1

        except Exception as e:
            return {'error': 'Erreur Google Calendar API'}, 500
        return {'message': f'{nombre_supprimes} créneaux supprimés de Google Calendar'}, 200
