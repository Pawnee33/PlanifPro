"""
Endpoints de gestion du profil utilisateur de PlanifPro.

Ce module définit les routes REST liées au profil utilisateur,
permettant à tout utilisateur connecté de consulter, modifier
et supprimer son compte.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade

facade = PlanifProFacade()

api = Namespace('utilisateurs', description='Opération Utilisateur')

utilisateur_model = api.model('Utilisateur', {
    'prenom': fields.String(required=True, description='Prénom ultilisateur'),
    'nom': fields.String(required=True, description='Nom ultilisateur'),
    'email': fields.String(description='Email utilisateur'),
    'mot_de_passe': fields.String(description='Mot de passe utilisateur'),
    'role': fields.String(description='Role utilisateur'),
    'token_fcm': fields.String(description='Token FCM utilisateur')
})

parametres_model = api.model('Parametres', {
    'notifications': fields.Boolean(description='Activer/désactiver les notifications'),
    'langue': fields.String(description='Langue de l\'application (fr/en)'),
    'theme': fields.String(description='Thème de l\'application (clair/sombre)')
})


@api.route('/profil')
class Profil(Resource):
    """
    Resource pour la gestion du profil utilisateur.

    Fournit les endpoints pour récupérer, modifier
    et supprimer le profil de l'utilisateur connecté.
    """
    @api.response(200, 'Profil récupéré')
    @api.response(404, 'Utilisateur introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Récupérer le profil de l'utilisateur connecté"""
        utilisateur_id = get_jwt_identity()
        
        try:
            utilisateur = facade.obtenir_utilisateur(utilisateur_id)
            if not utilisateur:
                return {'error': 'Utilisateur introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return utilisateur, 200

    @api.expect(utilisateur_model)
    @api.response(200, 'Profil mis à jour')
    @api.response(404, 'Utilisateur introuvable')
    @api.response(409, 'email déjà utilisé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self):
        """Modifier le profil de l'utilisateur connecté"""
        donnees_utilisateur = api.payload

        utilisateur_id = get_jwt_identity()
        
        utilisateur = facade.obtenir_utilisateur(utilisateur_id)
        if not utilisateur:
            return {'error': 'Utilisateur introuvable'}, 404

        if 'email' in donnees_utilisateur:
            existant = facade.obtenir_utilisateur_par_email(donnees_utilisateur['email'])
            if existant and existant['id'] != utilisateur_id:
                return {'error': 'email déjà utilisé'}, 409
        try:
            maj_utilisateur = facade.mettre_a_jour_utilisateur(utilisateur_id, donnees_utilisateur)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_utilisateur, 200

    @api.response(200, 'Compte supprimé')
    @api.response(404, 'Utilisateur introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self):
        """Supprimer le compte de l'utilisateur connecté"""

        utilisateur_id = get_jwt_identity()
        
        utilisateur = facade.obtenir_utilisateur(utilisateur_id)
        if not utilisateur:
            return {'error': 'Utilisateur introuvable'}, 404
        try:
            facade.supprimer_utilisateur(utilisateur_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Compte supprimé'}, 200

@api.route('/parametres')
class Parametres(Resource):
    """
    Resource pour la gestion des paramètres utilisateur.
    """
    @api.response(200, 'Paramètres récupérés')
    @api.response(404, 'Utilisateur introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Récupérer les paramètres de l'utilisateur connecté"""
        utilisateur_id = get_jwt_identity()
        try:
            utilisateur = facade.obtenir_utilisateur(utilisateur_id)
            if not utilisateur:
                return {'error': 'Utilisateur introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return utilisateur.get('parametres') or {}, 200

    @api.expect(parametres_model)
    @api.response(200, 'Paramètres mis à jour')
    @api.response(400, 'Données invalides')
    @api.response(404, 'Utilisateur introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self):
        """Modifier les paramètres de l'utilisateur connecté"""
        utilisateur_id = get_jwt_identity()
        donnees = api.payload

        utilisateur = facade.obtenir_utilisateur(utilisateur_id)
        if not utilisateur:
            return {'error': 'Utilisateur introuvable'}, 404

        try:
            maj = facade.mettre_a_jour_utilisateur(utilisateur_id, {'parametres': donnees})
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj.get('parametres') or {}, 200


@api.route('/aide')
class Aide(Resource):
    """
    Resource pour l'aide utilisateur.
    """
    @api.response(200, 'Aide affichée')
    @jwt_required()
    def get(self):
        """Récupérer l'aide de l'application"""
        return {
            'version': '1.0',
            'contact': 'support@planifpro.fr',
            'documentation': 'https://planifpro.fr/aide',
            'faq': [
                {'question': 'Comment rejoindre une classe ?', 'reponse': 'Utilisez le code fourni par votre professeur.'},
                {'question': 'Comment soumettre mes vœux ?', 'reponse': 'Rendez-vous dans la section Vœux de votre classe.'},
                {'question': 'Comment exporter mon planning ?', 'reponse': 'Utilisez le bouton Export dans votre planning.'}
            ]
        }, 200
