"""
Endpoints de gestion des créneaux de PlanifPro.

Ce module définit les routes REST liées aux créneaux,
permettant aux professeurs d'échanger, déplacer et confirmer des
créneaux d'élèves de consulter les créneaux global.
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade

facade = PlanifProFacade()

api = Namespace('creneaux', description='Opération de Creneau')

creneau_model = api.model('Creneau', {
    'planning_id': fields.String(required=True, description='ID du planning'),
    'eleve_id': fields.String(required=True, description='ID de l\'élève'),
    'classe_id': fields.String(required=True, description='ID de la classe'),
    'type': fields.String(required=True, description='Type de créneau'),
    'jour': fields.String(required=True, description='Jour du créneau'),
    'semaine_alternance': fields.String(description='Semaine alternance (paire/impaire)'),
    'heure_debut': fields.String(required=True, description='Heure de début du créneau'),
    'heure_fin': fields.String(required=True, description='Heure de fin du créneau'),
    'duree_minutes': fields.Integer(required=True, description='Durée du créneau'),
    'date_debut': fields.String(required=False, description='Début de période (AAAA-MM-JJ)'),
    'date_fin': fields.String(required=False, description='Fin de période (AAAA-MM-JJ)')
})

echanger_model = api.model('EchangerCreneaux', {
    'creneau_id_1': fields.String(required=True, description='ID du premier créneau'),
    'creneau_id_2': fields.String(required=True, description='ID du deuxième créneau')
})

deplacer_model = api.model('DeplacerCreneau', {
    'jour': fields.String(required=True, description='Nouveau jour'),
    'heure_debut': fields.String(required=True, description='Nouvelle heure de début'),
    'heure_fin': fields.String(required=True, description='Nouvelle heure de fin')
})


@api.route('/')
class CreneauList(Resource):
    """
    Resource pour la gestion des Créneaux.

    Fournit l'endpoint pour lister les créneaux.
    """
    @api.response(200, 'Créneaux affichés')
    @api.response(404, 'Aucun créneau trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Récupérer les créneaux de l'utilisateur connecté"""
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

    @api.expect(creneau_model)
    @api.response(201, 'Créneau créé')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Planning ou élève introuvable')
    @api.response(409, 'Chevauchement avec un créneau existant')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Créer un créneau manuellement"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees = api.payload

        planning = facade.obtenir_planning(donnees['planning_id'])
        if not planning:
            return {'error': 'Planning introuvable'}, 404

        eleve = facade.obtenir_eleve(donnees['eleve_id'])
        if not eleve:
            return {'error': 'Élève introuvable'}, 404

        try:
            donnees['statut'] = planning['statut']
            creneau = facade.creer_creneau(donnees)
        except ValueError as e:
            if 'chevauchement' in str(e).lower():
                return {'error': str(e)}, 409
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return creneau, 201


@api.route('/echanger')
class CreneauxEchanger(Resource):
    """
    Resource pour échanger deux créneaux entre élèves.
    """
    @api.expect(echanger_model)
    @api.response(200, 'Créneaux échangés')
    @api.response(400, 'Les deux créneaux appartiennent au même élève')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Un des deux créneaux introuvable')
    @api.response(409, 'Chevauchement après échange')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self):
        """Échanger deux créneaux entre élèves"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees = api.payload
        creneau_id_1 = donnees['creneau_id_1']
        creneau_id_2 = donnees['creneau_id_2']

        creneau_1 = facade.obtenir_creneau(creneau_id_1)
        if not creneau_1:
            return {'error': 'Un des deux créneaux introuvable'}, 404
        creneau_2 = facade.obtenir_creneau(creneau_id_2)
        if not creneau_2:
            return {'error': 'Un des deux créneaux introuvable'}, 404

        try:
            echanger = facade.echanger_creneaux(creneau_id_1, creneau_id_2)
        except ValueError as e:
            if 'chevauchement' in str(e).lower():
                return {'error': str(e)}, 409
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return echanger, 200


@api.route('/<creneau_id>')
class CreneauResource(Resource):
    """
    Resource pour les opérations sur un créneau spécifique.
    """
    @api.response(200, 'Détail du créneau affiché')
    @api.response(404, 'Créneau introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, creneau_id):
        """Récupérer le détail d'un créneau"""
        try:
            creneau = facade.obtenir_creneau(creneau_id)
            if not creneau:
                return {'error': 'Créneau introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return creneau, 200

    @api.expect(creneau_model)
    @api.response(200, 'Créneau modifié')
    @api.response(400, 'Données invalides')
    @api.response(400, 'Scope invalide')
    @api.response(400, 'Dates cibles requises pour ce scope')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Créneau introuvable')
    @api.response(409, 'Chevauchement avec un créneau existant')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, creneau_id):
        """Modifier un créneau"""
        donnees_creneau = api.payload

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        creneau = facade.obtenir_creneau(creneau_id)
        if not creneau:
            return {'error': 'Créneau introuvable'}, 404

        # Extraire le scope et les dates du payload avant d'envoyer à la façade
        scope = donnees_creneau.pop('scope', 'toute_la_periode')
        debut_jour = donnees_creneau.pop('debut_jour', None)
        fin_jour = donnees_creneau.pop('fin_jour', None)

        # Si scope = ce_jour, fin_jour = debut_jour
        if scope == 'ce_jour' and debut_jour and not fin_jour:
            fin_jour = debut_jour

        # Valider le scope
        if scope not in ('toute_la_periode', 'ce_jour', 'plusieurs_jours'):
            return {'error': 'Scope invalide'}, 400

        # Vérifier que les dates sont fournies si scope != toute_la_periode
        if scope != 'toute_la_periode' and (not debut_jour or not fin_jour):
            return {'error': 'Dates cibles requises pour ce scope'}, 400

        try:
            modifie_creneau = facade.mettre_a_jour_creneau(
                creneau_id, donnees_creneau, scope, debut_jour, fin_jour)
        except ValueError as e:
            if 'chevauchement' in str(e).lower():
                return {'error': str(e)}, 409
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return modifie_creneau, 200

    @api.response(200, 'Créneau supprimé avec succès')
    @api.response(400, 'Scope invalide')
    @api.response(400, 'Dates cibles requises pour ce scope')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Créneau introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, creneau_id):
        """Supprimer un créneau"""
        claims = get_jwt()

        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        # Scope et dates en query params ex: ?scope=ce_jour&debut_jour=2026-10-05
        scope = request.args.get('scope', 'toute_la_periode')
        debut_jour = request.args.get('debut_jour')
        fin_jour = request.args.get('fin_jour')

        if scope == 'ce_jour' and debut_jour and not fin_jour:
            fin_jour = debut_jour

        if scope not in ('toute_la_periode', 'ce_jour', 'plusieurs_jours'):
            return {'error': 'Scope invalide'}, 400

        if scope != 'toute_la_periode' and (not debut_jour or not fin_jour):
            return {'error': 'Dates cibles requises pour ce scope'}, 400

        try:
            creneau = facade.obtenir_creneau(creneau_id)
            if not creneau:
                return {'error': 'Créneau introuvable'}, 404
            facade.supprimer_creneau(creneau_id, scope, debut_jour, fin_jour)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Créneau supprimé avec succès'}, 200


@api.route('/<creneau_id>/confirmer')
class CreneauConfirmation(Resource):
    """
    Resource pour la confirmation d'un créneau.
    """
    @api.response(200, 'Créneau confirmé')
    @api.response(403, 'Accès réservé aux élèves')
    @api.response(404, 'Créneau introuvable')
    @api.response(409, 'Créneau déjà confirmé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, creneau_id):
        """confirmation d'un créneau"""
        claims = get_jwt()
        if claims.get('role') != 'eleve':
            return {'error': 'Accès réservé aux élèves'}, 403

        creneau = facade.obtenir_creneau(creneau_id)
        if not creneau:
            return {'error': 'Créneau introuvable'}, 404

        if creneau['statut'] == 'confirme':
            return {'error': 'Créneau déjà confirmé'}, 409
        try:
            maj_creneau = facade.mettre_a_jour_creneau(
                creneau_id,
                {'statut': 'confirme'}
            )
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        # Notifie le professeur que l'élève a confirmé son créneau
        classe = facade.obtenir_classe(creneau['classe_id'])
        if classe:
            facade.creer_notification({
                'utilisateur_id': classe['professeur_id'],
                'type': 'creneau_confirme',
                'titre': 'Créneau confirmé',
                'message': f"Un élève a confirmé son créneau ({creneau['jour']})",
            })
        return maj_creneau, 200


@api.route('/<creneau_id>/deplacer')
class DeplacerCreneau(Resource):
    """
    Resource pour déplacer un créneau.
    """
    @api.expect(deplacer_model)
    @api.response(200, 'Créneau déplacé')
    @api.response(400, 'Nouveau créneau invalide')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Créneau introuvable')
    @api.response(409, 'Chevauchement avec un créneau existant')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, creneau_id):
        """Déplacer un créneau"""
        claims = get_jwt()

        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        creneau = facade.obtenir_creneau(creneau_id)
        if not creneau:
            return {'error': 'Créneau introuvable'}, 404

        donnees = api.payload
        try:
            deplacer = facade.mettre_a_jour_creneau(creneau_id, donnees)
        except ValueError as e:
            if 'chevauchement' in str(e).lower():
                return {'error': str(e)}, 409
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return deplacer, 200
