"""
Endpoints de gestion des classes de PlanifPro.

Ce module définit les routes REST liées aux classes,
permettant aux professeurs de consulter leurs classes
et d'ajouter un élève à une classe via un code unique.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from planifPro.backend.services.facade import PlanifProFacade
from planifPro.backend.services.email_service import envoyer_email

facade = PlanifProFacade()

api = Namespace('classes', description='Opération de Classe')

classe_model = api.model('Classe', {
    'nom': fields.String(required=True, description='Nom de la classe'),
    'date_debut': fields.String(required=True, description='Date de début'),
    'date_fin': fields.String(required=True, description='Date de fin'),
    'jours_horaires': fields.Raw(description='Jours et horaires'),
    'nombre_propositions': fields.Integer(required=True),
    'nombre_voeux_requis': fields.Integer(required=True),
    'nombre_jours_min': fields.Integer(required=True)
})

rejoindre_model = api.model('RejoindreClasse', {
    'code_unique': fields.String(required=True, description='Code unique de la classe')
})

inviter_model = api.model('InviterEleve', {
    'email': fields.String(required=True, description='Email de l\'élève à inviter')
})

ajouter_eleve_model = api.model('AjouterEleve', {
    'eleve_id': fields.String(required=True, description='ID de l\'élève')
})


@api.route('/')
class ClassesList(Resource):
    """
    Resource pour la gestion des classes.

    Fournit l'endpoint pour lister les classes d'un professeur.
    """
    @api.response(200, 'Liste des classes affichée')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Aucune classes trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self):
        """Lister les classes du professeur connecté"""
        professeur_id = get_jwt_identity()
        
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        try:
            tout_classes = facade.obtenir_classes_par_professeur(professeur_id)
            if not tout_classes:
                return {'error': 'Aucune classes trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return tout_classes, 200

    @api.expect(classe_model)
    @api.response(201, 'Classe créée')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Créer une classe du professeur connecté"""
        professeur_id = get_jwt_identity()

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees = api.payload
        donnees['professeur_id'] = professeur_id

        try:
            nouvelle_classe = facade.creer_classe(donnees)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return nouvelle_classe, 201


@api.route('/rejoindre')
class Rejoindre(Resource):
    """
    Resource pour rejoindre une classe via un code unique.
    """
    @api.expect(rejoindre_model)
    @api.response(201, 'Élève rattaché à la classe')
    @api.response(400, 'Code invalide')
    @api.response(403, 'Accès réservé aux élèves')
    @api.response(404, 'Classe introuvable')
    @api.response(409, 'Déjà inscrit dans cette classe')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self):
        """Rejoindre une classe via un code unique"""
        claims = get_jwt()
        if claims.get('role') != 'eleve':
            return {'error': 'Accès réservé aux élèves'}, 403

        eleve_id = get_jwt_identity()
        code_unique = api.payload['code_unique']

        classe = facade.obtenir_classe_par_code(code_unique)
        if not classe:
            return {'error': 'Classe introuvable'}, 404

        # Vérifier si l'élève est déjà dans la classe
        eleves_classe = facade.obtenir_eleves_par_classe(classe['id'])
        if eleves_classe and any(eleve['id'] == eleve_id for eleve in eleves_classe):
            return {'error': 'Déjà inscrit dans cette classe'}, 409

        try:
            facade.ajouter_eleve_classe(classe['id'], eleve_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return classe, 201


@api.route('/<classe_id>')
class ClasseResource(Resource):
    """
    Resource pour les opérations sur une classe spécifique.
    """
    @api.response(200, 'Détail de la classe affichée')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, classe_id):
        """Récupérer le détail de la classe"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        try:
            classe = facade.obtenir_classe(classe_id)
            if not classe:
                return {'error': 'Classe introuvable'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return classe, 200

    @api.expect(classe_model)
    @api.response(200, 'Classe mise à jour')
    @api.response(400, 'Données invalide')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def put(self, classe_id):
        """Modifier la classe"""
        donnees_classe = api.payload

        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        classe = facade.obtenir_classe(classe_id)
        if not classe:
            return {'error': 'Classe introuvable'}, 404

        try:
            maj_classe = facade.mettre_a_jour_classe(classe_id, donnees_classe)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return maj_classe, 200

    @api.response(200, 'Classe supprimée avec succès')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def delete(self, classe_id):
        """Supprimer une classe"""
        claims = get_jwt()

        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        try:
            classe = facade.obtenir_classe(classe_id)
            if not classe:
                return {'error': 'Classe introuvable'}, 404
            facade.supprimer_classe(classe_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Classe supprimée avec succès'}, 200


@api.route('/<classe_id>/eleves')
class ClasseEleves(Resource):
    """
    Resource pour la gestion des élèves d'une classe spécifique.

    Fournit les endpoints pour lister et ajouter des élèves dans une classe.
    """
    @api.response(200, 'Liste des élèves affichée')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Aucun élève trouvé')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def get(self, classe_id):
        """Lister les élèves d'une classe spécifique"""
        
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403
        
        try:
            tout_eleves = facade.obtenir_eleves_par_classe(classe_id)
            if not tout_eleves:
                return {'error': 'Aucun élève trouvé'}, 404
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return tout_eleves, 200

    @api.expect(ajouter_eleve_model)
    @api.response(201, 'Élève ajouté')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Élève introuvable')
    @api.response(409, 'Élève déjà dans la classe')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self, classe_id):
        """Ajouter un élève à une classe"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        donnees = api.payload
        eleve_id = donnees['eleve_id']

        eleve = facade.obtenir_eleve(eleve_id)
        if not eleve:
            return {'error': 'Élève introuvable'}, 404

        classe = facade.obtenir_classe(classe_id)
        if not classe:
            return {'error': 'Classe introuvable'}, 404

        # Vérifier si l'élève est déjà dans la classe
        eleves_classe = facade.obtenir_eleves_par_classe(classe_id)
        if eleves_classe and any(eleve['id'] == eleve_id for eleve in eleves_classe):
            return {'error': 'Élève déjà dans la classe'}, 409

        try:
            facade.ajouter_eleve_classe(classe_id, eleve_id)
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return {'message': 'Élève ajouté avec succès'}, 201


@api.route('/<classe_id>/collecte')
class ClasseCollecte(Resource):
    """
    Resource pour lancer la collecte des vœux d'une classe.
    """
    @api.response(200, 'Collecte lancée')
    @api.response(400, 'Classe non active')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur interne du serveur')
    @jwt_required()
    def post(self, classe_id):
        """Lancer la collecte des vœux pour une classe"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        try:
            classe = facade.lancer_collecte(classe_id)
            if not classe:
                return {'error': 'Classe introuvable'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
        return classe, 200


@api.route('/<classe_id>/inviter')
class Inviter(Resource):
    """
    Resource pour inviter un élève par email dans une classe.
    """
    @api.expect(inviter_model)
    @api.response(200, 'Invitation envoyée')
    @api.response(400, 'Format email invalide')
    @api.response(403, 'Accès réservé aux professeurs')
    @api.response(404, 'Classe introuvable')
    @api.response(500, 'Erreur Brevo')
    @jwt_required()
    def post(self, classe_id):
        """Inviter un élève par email dans une classe"""
        claims = get_jwt()
        if claims.get('role') != 'professeur':
            return {'error': 'Accès réservé aux professeurs'}, 403

        classe = facade.obtenir_classe(classe_id)
        if not classe:
            return {'error': 'Classe introuvable'}, 404

        donnees = api.payload
        email = donnees.get('email')

        if not email or '@' not in email:
            return {'error': 'Format email invalide'}, 400

        try:
            envoyer_email(
                destinataire_email=email,
                destinataire_nom='Nouvel élève',
                sujet='Invitation à rejoindre une classe PlanifPro',
                contenu=f'''
                    <h2>Vous avez été invité à rejoindre une classe sur PlanifPro</h2>
                    <p>Votre professeur vous invite à rejoindre la classe 
                    <strong>{classe['nom']}</strong>.</p>
                    <p>Votre code d'accès : <strong>{classe['code_classe']}</strong></p>
                    <p>Téléchargez l'application PlanifPro et utilisez ce code 
                    pour rejoindre la classe.</p>
                '''
            )
        except Exception as e:
            return {'error': 'Erreur envoi email'}, 500
        return {'message': 'Invitation envoyée'}, 200
