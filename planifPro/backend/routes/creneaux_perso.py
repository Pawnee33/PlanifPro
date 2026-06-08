"""
Endpoints de gestion des créneaux personnels de PlanifPro.

Ce module définit les routes REST liées aux créneaux personnels,
permettant aux professeurs et élèves d'ajouter et gérer leurs
créneaux personnels dans leur calendrier.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade

facade = PlanifProFacade()

api = Namespace('creneaux_perso', description='Opération de Creneau Personnel')

creneau_perso_model = api.model('Creneau', {
    'titre': fields.String(required=True, description='Titre de la programmation'),
    'description': fields.String(description='Description de la programmation'),
    'jour': fields.String(required=True, description='Jour de la programmation'),
    'heure_debut': fields.String(required=True, description='Heure de début de la programmation'),
    'heure_fin': fields.String(required=True, description='Heure de fin de la programmation')
})

deplacer_model = api.model('DeplacerCreneau', {
    'jour': fields.String(required=True, description='Nouveau jour'),
    'heure_debut': fields.String(required=True, description='Nouvelle heure de début'),
    'heure_fin': fields.String(required=True, description='Nouvelle heure de fin')
})


@api.route('/')
class CreneauPersoList(Resource):
    """
    Resource pour la gestion des Créneaux personnels.

    Fournit l'endpoint pour lister les créneaux personnels.
    """
    @api.response(200, 'Créneaux personnels affichés')
    @api.response(404, 'Aucun créneau personnel trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Récupérer les créneaux personnels de l'utilisateur connecté"""
        utilisateur_id = get_jwt_identity()

        try:
            creneaux = facade.obtenir_creneaux_perso_par_utilisateur(utilisateur_id)
            if not creneaux:
                return {'error': 'Aucun créneau personnel trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return creneaux, 200

    @api.expect(creneau_perso_model)
    @api.response(201, 'Créneau créé')
    @api.response(400, 'Donnés invalides')
    @api.response(409, 'Chevauchement avec un créneau existant')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Créer un créneau manuellement"""
        utilisateur_id = get_jwt_identity()
        donnees = api.payload
        donnees['utilisateur_id'] = utilisateur_id

        try:
            creneau = facade.creer_creneau_perso(donnees)
        except ValueError as e:
            if 'chevauchement' in str(e).lower():
                return {'error': str(e)}, 409
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return creneau, 201


@api.route('/import')
class CreneauxImport(Resource):
    """
    Resource pour import des créneaux.
    """
    @api.response(200, 'Créneaux importés')
    @api.response(400, 'Token Google invalide')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Importer les créneaux depuis Google Calendar"""
        # TODO: implémenter l'import Google Calendar
        pass


@api.route('/<creneau_perso_id>')
class CreneauResource(Resource):
    """
    Resource pour les opérations sur un créneau spécifique.
    """
    @api.response(200, 'Détail du créneau affiché')
    @api.response(404, 'Créneau introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, creneau_perso_id):
        """Récupérer le détail d'un créneau"""
        try:
            creneau = facade.obtenir_creneau_perso(creneau_perso_id)
            if not creneau:
                return {'error': 'Créneau introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return creneau, 200

    @api.expect(creneau_perso_model)
    @api.response(200, 'Créneau modifié')
    @api.response(400, 'Données invalide')
    @api.response(404, 'Créneau introuvable')
    @api.response(409, 'Chevauchement avec un créneau existant')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, creneau_perso_id):
        """Modifier un créneau personnel"""
        donnees_creneau = api.payload
        
        creneau = facade.obtenir_creneau_perso(creneau_perso_id)
        if not creneau:
            return {'error': 'Créneau introuvable'}, 404

        try:
            modifie_creneau = facade.mettre_a_jour_creneau_perso(creneau_perso_id, donnees_creneau)
        except ValueError as e:
            if 'chevauchement' in str(e).lower():
                return {'error': str(e)}, 409
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return modifie_creneau, 200

    @api.response(200, 'Créneau supprimée avec succès')
    @api.response(404, 'Créneau introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, creneau_perso_id):
        """Supprimer un créneau personnel"""
        try:
            creneau = facade.obtenir_creneau_perso(creneau_perso_id)
            if not creneau:
                return {'error': 'Créneau introuvable'}, 404
            facade.supprimer_creneau_perso(creneau_perso_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Créneau supprimée avec succès'}, 200


@api.route('/<creneau_perso_id>/deplacer')
class DeplacerCreneau(Resource):
    """
    Resource pour déplacer un créneau personnel.
    """
    @api.expect(deplacer_model)
    @api.response(200, 'Créneau déplacé')
    @api.response(400, 'Nouveau créneau invalide')
    @api.response(404, 'Créneau introuvable')
    @api.response(409, 'Chevauchement avec un créneau existant')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, creneau_perso_id):
        """Déplacer un créneau"""
        creneau = facade.obtenir_creneau_perso(creneau_perso_id)
        if not creneau:
            return {'error': 'Créneau introuvable'}, 404

        donnees = api.payload
        try:
            deplacer = facade.mettre_a_jour_creneau_perso(creneau_perso_id, donnees)
        except ValueError as e:
            if 'chevauchement' in str(e).lower():
                return {'error': str(e)}, 409
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return deplacer, 200
