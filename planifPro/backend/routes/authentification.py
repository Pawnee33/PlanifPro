from flask_restx import Namespace, Resource, fields
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade

facade = PlanifProFacade()

api = Namespace('authentification', description='Opération d\'authentification')

connexion_model = api.model('connexion', {
    'email': fields.String(required=True, description='Utilisateur email'),
    'mot_de_passe': fields.String(required=True, description='Utilisateur mot de passe')
})

inscription_model = api.model('Inscription', {
    'role': fields.String(required=True, description='Rôle de l\'utilisateur (professeur ou eleve)'),
    'prenom': fields.String(required=True),
    'nom': fields.String(required=True),
    'email': fields.String(required=True),
    'mot_de_passe': fields.String(required=True),
})

@api.route('/inscription')
class Inscription(Resource):
    @api.expect(inscription_model, validate=True)
    @api.response(201, 'Utilisateur a été créé avec succès')
    @api.response(400, 'Données invalides')
    @api.response(409, 'Adresse e-mail déjà utilisé')
    @api.response(500, 'Erreur interne du serveur')
    def post(self):
        """Enregistrer un nouvel utilisateur (point de terminaison public)"""
        donnees = api.payload

        existant = facade.obtenir_utilisateur_par_email(donnees['email'])
        if existant:
            return {'error': 'Adresse e-mail déjà utilisé'}, 409

        try:
            if donnees['role'] == 'professeur':
                nouveau_utilisateur = facade.creer_professeur(donnees)
            elif donnees['role'] == 'eleve':
                nouveau_utilisateur = facade.creer_eleve(donnees)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

        return {
            'id': nouveau_utilisateur['id'],
            'message': 'Utilisateur a été créé avec succès'
        }, 201


@api.route('/connexion')
class Connexion(Resource):
    @api.expect(connexion_model)
    @api.response(200, 'Connexion réussie')
    @api.response(401, 'Identifiants invalides')
    @api.response(500, 'Erreur interne du serveur')
    def post(self):
        """Authentifier l'utilisateur et renvoyer un jeton JWT"""
        credentials = api.payload

        utilisateur = facade.obtenir_utilisateur_objet_par_email(credentials['email'])
        if not utilisateur or not utilisateur.verify_password(credentials['mot_de_passe']):
            return {'error': 'Identifiants non valides'}, 401
        try:
            access_token = create_access_token(
                identity=str(utilisateur.id),
                additional_claims={"role": utilisateur.role}
                )
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

        # Le token part dans un cookie httpOnly, plus dans le corps de la réponse
        reponse = jsonify({'role': utilisateur.role, 'message': 'Connexion réussie'})
        set_access_cookies(reponse, access_token)
        return reponse


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Un route protégé qui nécessite un jeton JWT valide """
        current_utilisateur = get_jwt_identity()
        claims = get_jwt()

        role = claims["role"]

        return {
            "message": f"Hello utilisateur {current_utilisateur}",
            "role": role
        }, 200

@api.route('/deconnexion')
class Deconnexion(Resource):
    @api.response(200, 'Déconnexion réussie')
    def post(self):
        """Déconnecter l'utilisateur en effaçant le cookie JWT"""
        reponse = jsonify({'message': 'Déconnexion réussie'})
        unset_jwt_cookies(reponse)   # efface le cookie côté navigateur
        return reponse
