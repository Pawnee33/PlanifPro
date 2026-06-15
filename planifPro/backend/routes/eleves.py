"""
Endpoints de gestion des élèves de PlanifPro.

Ce module définit les routes REST liées aux élèves,
permettant aux professeurs de consulter leurs élèves
et d'ajouter un élève à une classe via un code unique.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade
from planifPro.backend.services.email_service import envoyer_email

facade = PlanifProFacade()

api = Namespace('eleves', description='Opération Eleve')

eleve_model = api.model('Eleve', {
    'prenom': fields.String(required=True, description='Prénom élève'),
    'nom': fields.String(required=True, description='Nom élève'),
    'email': fields.String(description='Email élève')
})

duree_model = api.model('Duree', {
    'duree_minutes': fields.Integer(required=True, description='Durée du cours en minutes'),
    'classe_id': fields.String(required=True, description='ID de la classe')
})

inviter_model = api.model('InviterEleve', {
    'email': fields.String(required=True, description='Email de l\'élève'),
    'classe_id': fields.String(required=True, description='ID de la classe')
})


@api.route('/')
class ElevesList(Resource):
    """
    Resource pour la gestion des élèves.

    Fournit l'endpoint pour lister les élèves d'un professeur.
    """
    @api.response(200, 'Liste des élèves affichée')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Aucun élève trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Lister les élèves du professeur connecté"""
        professeur_id = get_jwt_identity()
        
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        try:
            tout_eleves = facade.obtenir_eleves_par_professeur(professeur_id)
            if not tout_eleves:
                return {'error': 'Aucun élève trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return tout_eleves, 200

@api.route('/inviter')
class Inviter(Resource):
    """
    Resource pour inviter un élève par email.
    """
    @api.expect(inviter_model)
    @api.response(200, 'Invitation envoyée')
    @api.response(400, 'Format email invalide')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur Brevo')
    @jwt_required()
    def post(self):
        """Inviter un élève par email"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees = api.payload
        email = donnees.get('email')
        classe_id = donnees.get('classe_id')

        classe = facade.obtenir_classe(classe_id)
        if not classe:
            return {'error': 'Classe introuvable'}, 404

        if not email or '@' not in email:
            return {'error': 'Format email invalide'}, 400

        try:
            envoyer_email(
                destinataire_email=email,
                destinataire_nom='Nouvel élève',
                sujet='Invitation PlanifPro',
                contenu=f'''
                    <h2>Vous avez été invité à rejoindre une classe sur PlanifPro</h2>
                    <p>Votre professeur vous invite à rejoindre sa classe.</p>
                    <p>Votre code d'accès : <strong>{classe['code_classe']}</strong></p>
                    <p>Téléchargez l'application PlanifPro et utilisez ce code 
                    pour rejoindre la classe.</p>
                '''
            )
        except Exception as e:
            return {'error': 'Erreur envoi email'}, 500
        return {'message': 'Invitation envoyée'}, 200


@api.route('/<eleve_id>')
class EleveResource(Resource):
    """
    Resource pour les opérations sur un eleve spécifique.
    """
    @api.response(200, 'Fiche élève affichée')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Élève introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, eleve_id):
        """Récupérer la fiche d'un élève"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        try:
            eleve = facade.obtenir_eleve(eleve_id)
            if not eleve:
                return {'error': 'Élève introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return eleve, 200

    @api.expect(duree_model)
    @api.response(200, 'Durée mise à jour')
    @api.response(400, 'Durée invalide')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Élève introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, eleve_id):
        """Modifier la durée de cours d'un élève"""
        donnees_eleve = api.payload

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        eleve = facade.obtenir_eleve(eleve_id)
        if not eleve:
            return {'error': 'Élève introuvable'}, 404

        if 'duree_minutes' not in donnees_eleve or donnees_eleve['duree_minutes'] <= 0:
            return {'error': 'Durée invalide'}, 400
        try:
            maj_eleve = facade.mettre_a_jour_duree_eleve_classe(
                eleve_id, donnees_eleve['classe_id'], donnees_eleve['duree_minutes']
            )
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_eleve, 200

    @api.response(200, 'Élève retiré avec succès')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Élève introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, eleve_id):
        """Retirer un élève d'une classe"""
        claims = get_jwt()
        professeur_id = get_jwt_identity()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        try:
            eleve = facade.obtenir_eleve(eleve_id)
            if not eleve:
                return {'error': 'Élève introuvable'}, 404
            facade.retirer_eleve_classes_professeur(professeur_id, eleve_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Élève retiré avec succès'}, 200
