"""
Endpoints de gestion des objectifs de PlanifPro.

Ce module définit les routes REST liées aux objectifs,
permettant aux professeurs de soumettre et modifier les objectifs
et aux élèves de consulter les objectifs pour le prochain cours.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade



facade = PlanifProFacade()

api = Namespace('objectifs', description='Opération d\'objectifs')

objectif_model = api.model('Objectif', {
    'eleve_id': fields.String(required=True, description='ID de l\'élève'),
    'creneau_id': fields.String(required=True, description='ID du créneau'),
    'contenu': fields.String(required=True, description='Contenu de l\'objectif'),
    'conseils': fields.String(required=True, description='Conseils données à l\'élève')
})


@api.route('/')
class ObjectifList(Resource):
    """
    Resource pour la gestion des objectifs.

    Fournit l'endpoint pour lister les objectifs des élèves.
    """
    @api.response(200, 'Liste des objectifs affichés')
    @api.response(404, 'Aucune objectif trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Lister les objectifs des élèves du professeur et des élèves connecté"""
        utilisateur_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get('role')

        try:
            if role == 'professeur':
                objectif = facade.obtenir_objectifs_par_professeur(utilisateur_id)
            elif role == 'eleve':
                objectif = facade.obtenir_objectifs_par_eleve(utilisateur_id)
            
            if not objectif:
                return {'error': 'Aucun objectif trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return objectif, 200

    @api.expect(objectif_model)
    @api.response(201, 'objectifs enregistrés et notification FCM élève')
    @api.response(400, 'Contenu vide ou trop long')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Créneau introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Créer un objectif"""
        professeur_id = get_jwt_identity()

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        # Récupère le JSON envoyé par le frontend (classe_id, creneaux_souhaites)
        donnees = api.payload
        # Ajoute l'ID du professeur connecté depuis le JWT (non envoyé par le frontend)
        donnees['professeur_id'] = professeur_id

        creneau = facade.obtenir_creneau(donnees['creneau_id'])
        if not creneau:
            return {'error': 'Créneau introuvable'}, 404

        try:
            objectif = facade.creer_objectif(donnees)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return objectif, 201


@api.route('/<objectif_id>')
class ObjectifResource(Resource):
    """
    Resource pour les opérations sur un objectif spécifique.
    """
    @api.response(200, 'Détail de l\'objectif affichée')
    @api.response(404, 'Objectif introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, objectif_id):
        """Récupérer le détail de l\'objectif"""
        try:
            objectif = facade.obtenir_objectif(objectif_id)
            if not objectif:
                return {'error': 'Objectif introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return objectif, 200

    @api.expect(objectif_model)
    @api.response(200, 'Objectif mis à jour')
    @api.response(400, 'Contenu vide ou trop long')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Objectif introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, objectif_id):
        """Modifier un objectif"""
        donnees_objectif = api.payload

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        objectif = facade.obtenir_objectif(objectif_id)
        if not objectif:
            return {'error': 'Objectif introuvable'}, 404

        try:
            maj_objectif = facade.mettre_a_jour_objectif(objectif_id, donnees_objectif)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_objectif, 200

    @api.response(200, 'Objectif supprimée avec succès')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Objectif introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, objectif_id):
        """Supprimer un objectif"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        try:
            objectif = facade.obtenir_objectif(objectif_id)
            if not objectif:
                return {'error': 'Objectif introuvable'}, 404
            facade.supprimer_objectif(objectif_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Objectif supprimée avec succès'}, 200
