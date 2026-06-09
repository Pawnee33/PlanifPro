"""
Endpoints de gestion des notifications de PlanifPro.

Ce module définit les routes REST liées aux notifications,
permettant aux professeurs et aux élèves de consulter les notifications.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade



facade = PlanifProFacade()

api = Namespace('notifications', description='Opération de Notification')

token_model = api.model('Token', {
    'token_fcm': fields.String(required=True, description='Token FCM de l\'appareil')
})


@api.route('/')
class NotificationList(Resource):
    """
    Resource pour la gestion des notifications.

    Fournit l'endpoint pour lister les notifications des professeurs et élèves.
    """
    @api.response(200, 'Liste des notifications affichés')
    @api.response(404, 'Aucune notification trouvée')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Lister les notifications des professeurs et des élèves connecté"""
        utilisateur_id = get_jwt_identity()
        try:
            notification = facade.obtenir_notifications_par_utilisateur(utilisateur_id)            
            if not notification:
                return {'error': 'Aucun notification trouvée'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return notification, 200


@api.route('/lire')
class Lire(Resource):
    """
    Resource pour marquer toutes les notifications comme lues.
    """
    @api.response(200, 'Notification mis à jour')
    @api.response(400, 'Données invalides')
    @api.response(404, 'Notifications introuvables')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self):
        """Marquer toutes les notifications comme lues"""
        utilisateur_id = get_jwt_identity()
    
        notifications = facade.obtenir_notifications_non_lues(utilisateur_id)
        if not notifications:
            return {'error': 'Notifications introuvables'}, 404

        try:
            maj_notifications = facade.marquer_toutes_notifications_lue(utilisateur_id)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_notifications, 200


@api.route('/token')
class Token(Resource):
    """
    Resource pour enregister le token FCM.
    """
    @api.expect(token_model)
    @api.response(200, 'Token enregistré')
    @api.response(400, 'Token manquant ou invalide')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Enregister le token FCM"""
        utilisateur_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get('role')
        donnees = api.payload
        token_fcm = donnees['token_fcm']

        try:
            if role == 'professeur':
                maj_token = facade.mettre_a_jour_professeur(utilisateur_id, {'token_fcm': token_fcm})
            elif role == 'eleve':
                maj_token = facade.mettre_a_jour_eleve(utilisateur_id, {'token_fcm': token_fcm})
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_token, 200


@api.route('/<notification_id>')
class NotificationResource(Resource):
    """
    Resource pour les opérations sur un notification spécifique.
    """
    @api.response(200, 'Notification mis à jour')
    @api.response(404, 'Notification introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, notification_id):
        """Marquer une notification comme lue"""        
        notification = facade.obtenir_notification(notification_id)
        if not notification:
            return {'error': 'Notification introuvable'}, 404

        try:
            maj_notification = facade.marquer_notification_lue(notification_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_notification, 200

    @api.response(200, 'Notification supprimée avec succès')
    @api.response(404, 'Notification introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, notification_id):
        """Supprimer un notification"""
        try:
            notification = facade.obtenir_notification(notification_id)
            if not notification:
                return {'error': 'Notification introuvable'}, 404
            facade.supprimer_notification(notification_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Notification supprimée avec succès'}, 200
