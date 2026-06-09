"""
Endpoints de gestion du calendrier Google de PlanifPro.

Ce module définit les routes REST liées à l'intégration
Google Calendar, permettant aux utilisateurs d'autoriser
l'accès et d'exporter leurs créneaux.
"""
from flask import request, redirect
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from google_auth_oauthlib.flow import Flow
from planifPro.backend.services.facade import PlanifProFacade
import os

facade = PlanifProFacade()

api = Namespace('calendrier', description='Opération Google Calendar')

export_model = api.model('Export', {
    'creneau_ids': fields.List(fields.String, required=True, description='IDs des créneaux à exporter')
})

SCOPES = ['https://www.googleapis.com/auth/calendar']


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
            auth_url, _ = flow.authorization_url(prompt='consent')
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
            # Récupère l'URL complète avec le code d'autorisation
            authorization_response = request.url
            flow.fetch_token(authorization_response=authorization_response)

            # Récupère et stocke les credentials
            credentials = flow.credentials
            # TODO: stocker credentials en BDD plutôt qu'en session
            return {
                'access_token': credentials.token,
                'refresh_token': credentials.refresh_token
            }, 200
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

                # Crée l'événement Google Calendar
                evenement = {
                    'summary': f"Cours {creneau['type']}",
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
                        f"RRULE:FREQ=WEEKLY;UNTIL={creneau['date_fin'].replace('-', '')}T000000Z"
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
