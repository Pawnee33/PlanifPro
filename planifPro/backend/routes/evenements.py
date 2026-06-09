"""
Endpoints de gestion des événements de PlanifPro.

Ce module définit les routes REST liées aux événements,
permettant aux professeurs de soumettre et modifier des événements
et aux élèves de consulter les événements pour y participer.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade



facade = PlanifProFacade()

api = Namespace('evenements', description='Opération Evenement')

evenement_model = api.model('Evenement', {
    'titre': fields.String(required=True, description='Titre de l\'événement'),
    'description': fields.String(required=True, description='Description de l\'événement'),
    'date_heure': fields.String(required=True, description='Date et heure de l\'événement'),
    'destinataires': fields.Raw(required=True, description='Les destinataires qui participeront à l\'événement')
})


@api.route('/')
class EvenementList(Resource):
    """
    Resource pour la gestion des événements.

    Fournit l'endpoint pour lister les événements des professeurs.
    """
    @api.response(200, 'Liste des événements affichés')
    @api.response(404, 'Aucune événement trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Lister les événements des professeurs et des élèves connecté"""
        utilisateur_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get('role')

        try:
            if role == 'professeur':
                evenement = facade.obtenir_evenements_par_professeur(utilisateur_id)
            elif role == 'eleve':
                evenement = facade.obtenir_evenements_par_eleve(utilisateur_id)
            
            if not evenement:
                return {'error': 'Aucun événement trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return evenement, 200

    @api.expect(evenement_model)
    @api.response(201, 'Événement créé et notification FCM')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe ou élève introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Créer un événement"""
        professeur_id = get_jwt_identity()

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        # Récupère le JSON envoyé par le frontend (classe_id, creneaux_souhaites)
        donnees = api.payload
        # Ajoute l'ID du professeur connecté depuis le JWT (non envoyé par le frontend)
        donnees['professeur_id'] = professeur_id

        try:
            evenement = facade.creer_evenement(donnees)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return evenement, 201


@api.route('/<evenement_id>')
class EvenementResource(Resource):
    """
    Resource pour les opérations sur un événement spécifique.
    """
    @api.response(200, 'Détail de l\'événement affichée')
    @api.response(404, 'Événement introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, evenement_id):
        """Récupérer le détail de l\'événement"""
        try:
            evenement = facade.obtenir_evenement(evenement_id)
            if not evenement:
                return {'error': 'Événement introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return evenement, 200

    @api.expect(evenement_model)
    @api.response(200, 'Événement mis à jour')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Événement introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, evenement_id):
        """Modifier un Événement"""
        donnees_evenement = api.payload

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        evenement = facade.obtenir_evenement(evenement_id)
        if not evenement:
            return {'error': 'Événement introuvable'}, 404

        try:
            maj_evenement = facade.mettre_a_jour_evenement(evenement_id, donnees_evenement)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_evenement, 200

    @api.response(200, 'Événement supprimée avec succès')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Événement introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, evenement_id):
        """Supprimer un événement"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        try:
            evenement = facade.obtenir_evenement(evenement_id)
            if not evenement:
                return {'error': 'Événement introuvable'}, 404
            facade.supprimer_evenement(evenement_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Événement supprimée avec succès'}, 200
