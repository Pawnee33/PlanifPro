"""
Endpoints de gestion des professeurs de PlanifPro.

Ce module définit les routes REST liées aux professeurs,
permettant aux élèves de consulter leurs professeurs
et de rejoindre une classe via un code unique.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade

facade = PlanifProFacade()

api = Namespace('professeurs', description='Opération de Professeur')

professeur_model = api.model('Professeur', {
    'prenom': fields.String(required=True, description='Prénom professeur'),
    'nom': fields.String(required=True, description='Nom professeur'),
    'email': fields.String(description='Email professeur')
})

rejoindre_model = api.model('Rejoindre', {
    'code_unique': fields.String(required=True, description='Code unique de la classe')
})


@api.route('/')
class Professeurs(Resource):
    """
    Resource pour la gestion des professeurs.

    Fournit l'endpoint pour lister les professeurs d'un élève.
    """
    @api.response(200, 'Liste récupéré')
    @api.response(403, 'Rôle incorrect')
    @api.response(404, 'Aucun professeur trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Lister les professeurs de l'élève connecté"""
        eleve_id = get_jwt_identity()
        
        claims = get_jwt()
        if claims.get('role') != 'eleve':
            return {'error': 'Accès réservé aux élèves'}, 403
        
        try:
            tout_professeurs = facade.obtenir_professeurs_par_eleve(eleve_id)
            if not tout_professeurs:
                return {'error': 'Aucun professeur trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return tout_professeurs, 200


@api.route('/rejoindre')
class Rejoindre(Resource):
    """
    Resource pour rejoindre un professeur via un code de classe.
    """
    @api.expect(rejoindre_model)
    @api.response(201, 'Rejoint avec succès')
    @api.response(400, 'données invalides')
    @api.response(403, 'Rôle incorrect')
    @api.response(404, 'Code classe introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Rejoindre une classe via un code unique"""
        claims = get_jwt()
        if claims.get('role') != 'eleve':
            return {'error': 'Accès réservé aux élèves'}, 403

        code_unique = api.payload['code_unique']

        eleve_id = get_jwt_identity()
        
        classe = facade.obtenir_classe_par_code(code_unique)
        if not classe:
            return {'error': 'Code classe introuvable'}, 404

        try:
            facade.ajouter_eleve_classe(classe['id'], eleve_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return classe, 201

@api.route('/<professeur_id>')
class ProfesseurResource(Resource):
    """
    Resource pour les opérations sur un professeur spécifique.
    """
    @api.response(200, 'Professeur récupéré')
    @api.response(403, 'Rôle incorrect')
    @api.response(404, 'Professeur introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, professeur_id):
        """Récupérer le profil d'un professeur"""
        claims = get_jwt()
        if claims.get('role') != 'eleve':
            return {'error': 'Accès réservé aux élèves'}, 403

        try:
            professeur = facade.obtenir_professeur(professeur_id)
            if not professeur:
                return {'error': 'Professeur introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return professeur, 200

    @api.response(200, 'Élève retiré du professeur avec succès')
    @api.response(403, 'Rôle incorrect')
    @api.response(404, 'Professeur introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, professeur_id):
        """Se désinscrire d'un professeur"""
        claims = get_jwt()
        eleve_id = get_jwt_identity()
        if claims.get('role') != 'eleve':
            return {'error': 'Accès réservé aux élèves'}, 403

        try:
            professeur = facade.obtenir_professeur(professeur_id)
            if not professeur:
                return {'error': 'Professeur introuvable'}, 404
            facade.retirer_eleve_classes_professeur(professeur_id, eleve_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Élève retiré du professeur avec succès'}, 200
