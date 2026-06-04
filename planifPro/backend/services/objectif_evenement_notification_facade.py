"""
Facade de gestion des objectifs, événements et notifications de PlanifPro.

Ce module définit la classe ObjectifEvenementNotificationFacade qui gère
la logique métier liée aux objectifs pédagogiques, aux événements
et aux notifications.
"""
from planifPro.backend.persistence import SQLAlchemyRepository
from planifPro.backend.persistence.objectif_repository import ObjectifRepository
from planifPro.backend.persistence.evenement_repository import EvenementRepository
from planifPro.backend.persistence.notification_repository import NotificationRepository
from planifPro.backend.classes.objectif import Objectif
from planifPro.backend.classes.evenement import Evenement
from planifPro.backend.classes.notification import Notification


class ObjectifEvenementNotificationFacade:
    """
    Facade pour la gestion des objectifs, événements et notifications.

    Centralise la logique métier liée aux objectifs pédagogiques,
    à la création d'événements et à la gestion des notifications.
    Fait le lien entre les routes API et les repositories correspondants.
    """
    def __init__(self):
        self.objectif_repo = ObjectifRepository()
        self.evenement_repo = EvenementRepository()
        self.notification_repo = NotificationRepository()

    # Objectif
    def creer_objectif(self, donnees):
        """
        Crée un nouvel objectif dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            de l'objectif (professeur_id, eleve_id, creneau_id, contenu,
            et conseils).

        Retourne :
            dict : Dictionnaire contenant les informations
            de l'objectif créé.
        """
        objectif = Objectif(
            professeur_id=donnees['professeur_id'],
            eleve_id=donnees['eleve_id'],
            creneau_id=donnees['creneau_id'],
            contenu=donnees['contenu'],
            conseils=donnees.get('conseils')
        )
        self.objectif_repo.ajouter(objectif)
        return objectif.to_dict()

    def obtenir_objectif(self, objectif_id):
        """obtenir_objectif permet de récupère un objectif"""
        objectif = self.objectif_repo.obtenir(objectif_id)
        if not objectif:
            return None
        return objectif.to_dict()

    def mettre_a_jour_objectif(self, objectif_id, donnees_objectif):
        """Mettre à jour un objectif existant"""
        objectif = self.objectif_repo.obtenir(objectif_id)
        if not objectif:
            return None
        self.objectif_repo.mis_a_jour(objectif_id, donnees_objectif)
        return self.objectif_repo.obtenir(objectif_id).to_dict()

    def obtenir_objectifs_par_eleve(self, eleve_id):
        """
        obtenir_objectifs_par_eleve permet de récupérer
        les objectifs à partir de ID de la eleve.
        """
        objectifs = self.objectif_repo.obtenir_objectifs_par_eleve(eleve_id)
        if not objectifs:
            return None
        return [objectif.to_dict() for objectif in objectifs]

    def obtenir_objectifs_par_creneau(self, creneau_id):
        """
        obtenir_objectifs_par_creneau permet de récupérer
        les objectifs à partir de ID du créneau.
        """
        objectifs = self.objectif_repo.obtenir_objectifs_par_creneau(creneau_id)
        if not objectifs:
            return None
        return [objectif.to_dict() for objectif in objectifs]

    def supprimer_objectif(self, objectif_id):
        """Supprimer un objectif existant et toutes les données associées (cascade)."""
        self.objectif_repo.supprime(objectif_id)

    # Événement
    def creer_evenement(self, donnees):
        """
        Crée un nouvel événement dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            de l'événement (professeur_id, titre, description,
            date_heure et destinataires).

        Retourne :
            dict : Dictionnaire contenant les informations
            de l'événement créé.
        """
        evenement = Evenement(
            professeur_id=donnees['professeur_id'],
            titre=donnees['titre'],
            description=donnees['description'],
            date_heure=donnees['date_heure'],
            destinataires=donnees['destinataires']
        )
        self.evenement_repo.ajouter(evenement)
        return evenement.to_dict()

    def obtenir_evenement(self, evenement_id):
        """obtenir_evenement permet de récupérer un evenement"""
        evenement = self.evenement_repo.obtenir(evenement_id)
        if not evenement:
            return None
        return evenement.to_dict()

    def obtenir_tout_evenements(self):
        """obtenir_tout_evenements permet de récupérer tout les evenements"""
        tout_evenements = self.evenement_repo.tout_obtenir()
        if not tout_evenements:
            return None
        return [evenement.to_dict() for evenement in tout_evenements]

    def mettre_a_jour_evenement(self, evenement_id, donnees_evenement):
        """Mettre à jour un evenement existant"""
        evenement = self.evenement_repo.obtenir(evenement_id)
        if not evenement:
            return None
        self.evenement_repo.mis_a_jour(evenement_id, donnees_evenement)
        return self.evenement_repo.obtenir(evenement_id).to_dict()

    def supprimer_evenement(self, evenement_id):
        """Supprimer un evenement existant et toutes les données associées (cascade)."""
        self.evenement_repo.supprime(evenement_id)
