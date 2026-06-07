"""
Endpoints de gestion des plannings de PlanifPro.

Ce module définit les routes REST liées aux plannings,
permettant aux professeurs de générer et valider les plannings
et aux élèves de consulter leur planning global.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade

facade = PlanifProFacade()

api = Namespace('plannings', description='Opération de Planning')

generer_model = api.model('GenererPlanning', {
    'classe_id': fields.String(required=True, description='ID de la classe')
})

valider_model = api.model('ValiderPlanning', {
    'planning_id': fields.String(required=True, description='ID du planning à valider')
})

confirmation_model = api.model('ConfirmationPlanning', {
    'confirmation': fields.Boolean(required=True, description='Activer ou désactiver la confirmation')
})


@api.route('/global')
class PlanningsGlobal(Resource):
    """
    Resource pour la gestion des Plannings.

    Fournit l'endpoint pour lister les pplannings.
    """
    @api.response(200, 'Planning affichée')
    @api.response(404, 'Aucun créneau trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Récupérer le planning global de l'utilisateur connecté"""
        utilisateur_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get('role')

        try:
            if role == 'professeur':
                creneaux = facade.obtenir_creneaux_par_professeur(utilisateur_id)
            elif role == 'eleve':
                creneaux = facade.obtenir_creneaux_par_eleve(utilisateur_id)
            
            if not creneaux:
                return {'error': 'Aucun créneau trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return creneaux, 200


@api.route('/generer')
class PlanningGenerer(Resource):
    """
    Resource pour générer les propositions de planning.
    """
    @api.expect(generer_model)
    @api.response(200, '3 propositions générées')
    @api.response(400, 'Voeux insuffisants')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Générer les propositions de planning"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees = api.payload
        classe_id = donnees['classe_id']

        classe = facade.obtenir_classe(classe_id)
        if not classe:
                return {'error': 'Classe introuvable'}, 404

        try:
            genere_planning = facade.generer_planning(classe_id)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return genere_planning, 200


@api.route('/valider')
class PlanningValider(Resource):
    """
    Resource pour valider les propositions de planning.
    """
    @api.expect(valider_model)
    @api.response(200, 'Planning valider')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Planning introuvable')
    @api.response(409, 'Planning déjà validé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self):
        """validé le planning"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees_planning = api.payload
        planning_id = donnees_planning['planning_id']

        planning = facade.obtenir_planning(planning_id)
        if not planning:
            return {'error': 'Planning introuvable'}, 404

        planning_valide = facade.obtenir_planning_valide(planning['classe_id'])
        if planning_valide:
            return {'error': 'Planning déjà validé'}, 409

        try:
            valide_planning = facade.valider_planning(planning_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return valide_planning, 200


@api.route('/<planning_id>')
class PlanningResource(Resource):
    """
    Resource pour les opérations sur un planning spécifique.
    """
    @api.response(200, 'Détail du planning affiché')
    @api.response(404, 'Planning introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, planning_id):
        """Récupérer le détail d'un planning"""
        try:
            planning = facade.obtenir_planning(planning_id)
            if not planning:
                return {'error': 'Planning introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return planning, 200


@api.route('/<planning_id>/creneaux')
class PlanningCreneaux(Resource):
    """
    Resource pour récupérer les créneaux d'un planning.
    """
    @api.response(200, 'Liste des créneaux affichée')
    @api.response(404, 'Aucun créneau trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, planning_id):
        """Récupérer les créneaux d'un planning"""
        try:
            creneaux = facade.obtenir_creneaux_par_planning(planning_id)
            if not creneaux:
                return {'error': 'Aucun créneau trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return creneaux, 200


@api.route('/<planning_id>/confirmation')
class PlanningConfirmation(Resource):
    """
    Resource pour activer ou désactiver la confirmation d'un planning.
    """
    @api.expect(confirmation_model)
    @api.response(200, 'Option confirmation activée/désactivée')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Planning introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, planning_id):
        """Activer ou désactiver la confirmation d'un planning"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        planning = facade.obtenir_planning(planning_id)
        if not planning:
            return {'error': 'Planning introuvable'}, 404

        donnees = api.payload
        try:
            maj_planning = facade.mettre_a_jour_planning(
                planning_id,
                {'confirmation': donnees['confirmation']}
            )
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_planning, 200
