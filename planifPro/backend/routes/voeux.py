"""
Endpoints de gestion des vœux de PlanifPro.

Ce module définit les routes REST liées aux vœux,
permettant aux élèves de soumettre et modifier leurs vœux
et aux professeurs de consulter les statuts et relancer
les élèves en attente.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade
from planifPro.backend.services.fcm_service import envoyer_notification


facade = PlanifProFacade()

api = Namespace('voeux', description='Opération Voeu')

voeu_model = api.model('Voeu', {
    'classe_id': fields.String(required=True, description='ID de la classe'),
    'creneaux_souhaites': fields.Raw(required=True, description='Créneaux souhaités')
})

relancer_model = api.model('Relancer', {
    'classe_id': fields.String(required=True, description='ID de la classe'),
    'eleve_ids': fields.List(fields.String, required=True, description='IDs des élèves à relancer')
})


@api.route('/')
class VoeuxList(Resource):
    """
    Resource pour la gestion des voeux.

    Fournit l'endpoint pour lister les voeux des élèves.
    """
    @api.response(200, 'Liste des voeux affichée')
    @api.response(404, 'Aucune voeu trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Lister les voeux des élèves du professeur et des élèves connecté"""
        utilisateur_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get('role')

        try:
            if role == 'professeur':
                voeux = facade.obtenir_voeux_par_professeur(utilisateur_id)
            elif role == 'eleve':
                voeux = facade.obtenir_voeux_par_eleve(utilisateur_id)
            
            if not voeux:
                return {'error': 'Aucun vœu trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return voeux, 200

    @api.expect(voeu_model)
    @api.response(201, 'Voeux enregistrés')
    @api.response(400, 'Nombre de voeux insuffisant ou jours minimum non respectés')
    @api.response(403, 'Accès réservé aux élèves')
    @api.response(409, 'Planning déjà généré')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Soumettre les voeux des élèves"""
        eleve_id = get_jwt_identity()

        claims = get_jwt()
        if claims.get('role') != 'eleve':
            return {'error': 'Accès réservé aux élèves'}, 403

        # Récupère le JSON envoyé par le frontend (classe_id, creneaux_souhaites)
        donnees = api.payload
        # Ajoute l'ID de l'élève connecté depuis le JWT (non envoyé par le frontend)
        donnees['eleve_id'] = eleve_id

        planning = facade.obtenir_planning_valide(donnees['classe_id'])
        if planning:
            return {'error': 'Planning déjà généré, modification impossible'}, 409

        try:
            soumission_voeux = facade.creer_voeu(donnees)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return soumission_voeux, 201


@api.route('/relancer')
class Relancer(Resource):
    """
    Resource pour relancer les élèves en attente.
    """
    @api.expect(relancer_model)
    @api.response(200, 'Notification envoyée')
    @api.response(400, 'Aucun élève sélectionné')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Relancer les élèves en attente"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees = api.payload
        classe_id = donnees['classe_id']
        eleve_ids = donnees['eleve_ids']

        classe = facade.obtenir_classe(classe_id)
        if not classe:
            return {'error': 'Classe introuvable'}, 404

        if not eleve_ids:
            return {'error': 'Aucun élève sélectionné'}, 400

        try:
            for eleve_id in eleve_ids:
                eleve = facade.obtenir_eleve(eleve_id)
                if not eleve:
                    continue
                # Notification in-app (visible dans la cloche)
                facade.creer_notification({
                    'utilisateur_id': eleve_id,
                    'type': 'collecte_voeux',
                    'titre': 'Rappel vœux',
                    'message': f"N'oubliez pas de soumettre vos vœux pour la classe {classe['nom']} !",
                })
                # Notification push (si l'élève a un token FCM)
                if eleve['token_fcm']:
                    envoyer_notification(
                        eleve['token_fcm'],
                        "Rappel vœux",
                        "N'oubliez pas de soumettre vos vœux !"
                    )
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Notifications envoyées avec succès'}, 200


@api.route('/statut/<classe_id>')
class VoeuStatut(Resource):
    """
    Resource pour consulter le statut des vœux d'une classe.
    """
    @api.response(200, 'Statut affiché')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(404, 'Aucun vœu trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, classe_id):
        """Statut des voeux par élèves"""        
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        classe = facade.obtenir_classe(classe_id)
        if not classe:
            return {'error': 'Classe introuvable'}, 404

        try:
            statut =facade.obtenir_voeu_par_classe(classe_id)          
            if not statut:
                return {'error': 'Aucun vœu trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return statut, 200


@api.route('/<voeu_id>')
class VoeuResource(Resource):
    """
    Resource pour les opérations sur un voeu spécifique.
    """
    @api.response(200, 'Détail du voeu affichée')
    @api.response(404, 'Voeu introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, voeu_id):
        """Récupérer le détail du voeu"""
        try:
            voeu = facade.obtenir_voeu(voeu_id)
            if not voeu:
                return {'error': 'Voeu introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return voeu, 200

    @api.expect(voeu_model)
    @api.response(200, 'Voeu mis à jour')
    @api.response(400, 'Nombre de voeux insuffisant ou jours minimumnon respectés')
    @api.response(404, 'Voeu introuvable')
    @api.response(409, 'Planning déjà généré')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, voeu_id):
        """Modifier un voeu"""
        donnees_voeu = api.payload
        
        voeu = facade.obtenir_voeu(voeu_id)
        if not voeu:
            return {'error': 'Voeu introuvable'}, 404

        planning = facade.obtenir_planning_valide(donnees_voeu['classe_id'])
        if planning:
            return {'error': 'Planning déjà généré, modification impossible'}, 409

        try:
            maj_voeu = facade.mettre_a_jour_voeu(voeu_id, donnees_voeu)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_voeu, 200
