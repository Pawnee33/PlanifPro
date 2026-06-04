"""
Facade d'authentification de PlanifPro.

Ce module définit la classe AuthFacade qui gère la logique
métier liée aux utilisateurs, professeurs et élèves.
"""
from planifPro.backend.persistence import SQLAlchemyRepository
from planifPro.backend.persistence.utilisateur_repository import UtilisateurRepository
from planifPro.backend.persistence.professeur_repository import ProfesseurRepository
from planifPro.backend.persistence.eleve_repository import EleveRepository
from planifPro.backend.classes.utilisateur import Utilisateur
from planifPro.backend.classes.professeur import Professeur
from planifPro.backend.classes.eleve import Eleve


class AuthFacade:
    """
    Facade pour la gestion des utilisateurs, professeurs et élèves.

    Centralise la logique métier liée à l'authentification et
    à la gestion des comptes utilisateurs. Fait le lien entre
    les routes API et les repositories correspondants.
    """
    def __init__(self):
        self.utilisateur_repo = UtilisateurRepository()
        self.professeur_repo = ProfesseurRepository()
        self.eleve_repo = EleveRepository()

    # Utilisateur
    def creer_utilisateur(self, donnees):
        """
        Crée un nouvel utilisateur dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            de l'utilisateur (prenom, nom, email, role, mot_de_passe).

        Retourne :
            dict : Dictionnaire contenant les informations
            de l'utilisateur créé.
        """
        utilisateur = Utilisateur(
            prenom=donnees['prenom'],
            nom=donnees['nom'],
            email=donnees['email'],
            role=donnees['role'],
            mot_de_passe_hash='temp'
        )
        utilisateur.hash_password(donnees['mot_de_passe'])
        self.utilisateur_repo.ajouter(utilisateur)
        return utilisateur.to_dict()

    def obtenir_utilisateur(self, utilisateur_id):
        """obtenir_utilisateur permet de récupère un utilisateur"""
        utilisateur = self.utilisateur_repo.obtenir(utilisateur_id)
        if not utilisateur:
            return None
        return utilisateur.to_dict()

    def obtenir_tout_utilisateurs(self):
        """obtenir_tout_utilisateurs permet de récupérer tout les utilisateurs"""
        tout_utilisateurs = self.utilisateur_repo.tout_obtenir()
        if not tout_utilisateurs:
            return None
        return [utilisateur.to_dict() for utilisateur in tout_utilisateurs]

    def mettre_a_jour_utilisateur(self, utilisateur_id, donnees_utilisateur):
        """Mettre à jour d'un utilisateur existant"""
        utilisateur = self.utilisateur_repo.obtenir(utilisateur_id)
        if not utilisateur:
            return None
        self.utilisateur_repo.mis_a_jour(utilisateur_id, donnees_utilisateur)
        return self.utilisateur_repo.obtenir(utilisateur_id).to_dict()

    def obtenir_utilisateur_par_email(self, email):
        """
        obtenir_utilisateur_par_email  permet de récupérer
        un utilisateur à partir d'une adresse e-mail
        """
        utilisateur = self.utilisateur_repo.obtenir_par_attribut('email', email)
        if not utilisateur:
            return None
        return utilisateur.to_dict()

    def supprimer_utilisateur(self, utilisateur_id):
        """Supprimer un utilisateur existant et toutes les données associées (cascade)."""
        self.utilisateur_repo.supprime(utilisateur_id)

    # Professeur
    def creer_professeur(self, donnees):
        """
        Crée un nouveau professeur dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            du professeur (prenom, nom, email, role, mot_de_passe).

        Retourne :
            dict : Dictionnaire contenant les informations
            du professeur créé.
        """
        professeur = Professeur(
            prenom=donnees['prenom'],
            nom=donnees['nom'],
            email=donnees['email'],
            role=donnees['role'],
            mot_de_passe_hash='temp'
        )
        professeur.hash_password(donnees['mot_de_passe'])
        self.professeur_repo.ajouter(professeur)
        return professeur.to_dict()

    def obtenir_professeur(self, professeur_id):
        """obtenir_professeur permet de récupérer un professeur"""
        professeur = self.professeur_repo.obtenir(professeur_id)
        if not professeur:
            return None
        return professeur.to_dict()

    def obtenir_tout_professeurs(self):
        """obtenir_tout_professeurs permet de récupérer tout les professeurs"""
        tout_professeurs = self.professeur_repo.tout_obtenir()
        if not tout_professeurs:
            return None
        return [professeur.to_dict() for professeur in tout_professeurs]

    def mettre_a_jour_professeur(self, professeur_id, donnees_professeur):
        """Mettre à jour d'un professeur existant"""
        professeur = self.professeur_repo.obtenir(professeur_id)
        if not professeur:
            return None
        self.professeur_repo.mis_a_jour(professeur_id, donnees_professeur)
        return self.professeur_repo.obtenir(professeur_id).to_dict()

    def obtenir_professeur_par_email(self, email):
        """
        obtenir_professeur_par_email  permet de récupérer
        un professeur à partir d'une adresse e-mail
        """
        professeur = self.professeur_repo.obtenir_par_attribut('email', email)
        if not professeur:
            return None
        return professeur.to_dict()

    def supprimer_professeur(self, professeur_id):
        """Supprimer un professeur existant et toutes les données associées (cascade)."""
        self.professeur_repo.supprime(professeur_id)

    # Élève
    def creer_eleve(self, donnees):
        """
        Crée un nouvel élève dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            de l'élève (prenom, nom, email, role, mot_de_passe).

        Retourne :
            dict : Dictionnaire contenant les informations
            de l'élève créé.
        """
        eleve = Eleve(
            prenom=donnees['prenom'],
            nom=donnees['nom'],
            email=donnees['email'],
            role=donnees['role'],
            mot_de_passe_hash='temp'
        )
        eleve.hash_password(donnees['mot_de_passe'])
        self.eleve_repo.ajouter(eleve)
        return eleve.to_dict()

    def obtenir_eleve(self, eleve_id):
        """obtenir_eleve permet de récupérer un élève"""
        eleve = self.eleve_repo.obtenir(eleve_id)
        if not eleve:
            return None
        return eleve.to_dict()

    def obtenir_tout_eleves(self):
        """obtenir_tout_eleves permet de récupérer tous les élèves"""
        tout_eleves = self.eleve_repo.tout_obtenir()
        if not tout_eleves:
            return None
        return [eleve.to_dict() for eleve in tout_eleves]

    def mettre_a_jour_eleve(self, eleve_id, donnees_eleve):
        """Mettre à jour un élève existant"""
        eleve = self.eleve_repo.obtenir(eleve_id)
        if not eleve:
            return None
        self.eleve_repo.mis_a_jour(eleve_id, donnees_eleve)
        return self.eleve_repo.obtenir(eleve_id).to_dict()

    def obtenir_eleve_par_email(self, email):
        """
        obtenir_eleve_par_email permet de récupérer
        un élève à partir d'une adresse e-mail
        """
        eleve = self.eleve_repo.obtenir_par_attribut('email', email)
        if not eleve:
            return None
        return eleve.to_dict()

    def supprimer_eleve(self, eleve_id):
        """Supprimer un élève existant et toutes les données associées (cascade)."""
        self.eleve_repo.supprime(eleve_id)
