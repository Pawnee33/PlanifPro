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
from planifPro.backend.persistence.classe_repository import ClasseRepository
from planifPro.backend.persistence.eleve_repository import EleveRepository
from planifPro.backend.classes.objectif import Objectif
from planifPro.backend.classes.evenement import Evenement
from planifPro.backend.classes.notification import Notification
from planifPro.backend.classes.eleve import Eleve
from planifPro.backend.classes.classe import Classe


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
        self.classe_repo = ClasseRepository()
        self.eleve_repo = EleveRepository()

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

        # Résolution des destinataires
        type_destinataires = donnees['destinataires']['type']
        eleves = []

        if type_destinataires == 'toutes_classes':
            # Récupère tous les élèves de toutes les classes du professeur
            classes = self.classe_repo.obtenir_classes_par_professeur(donnees['professeur_id'])
            for classe in classes:
                eleves.extend(classe.eleves)

        elif type_destinataires == 'classes':
            # Récupère les élèves des classes sélectionnées
            for classe_id in donnees['destinataires']['ids']:
                classe = self.classe_repo.obtenir(classe_id)
                if classe:
                    eleves.extend(classe.eleves)

        elif type_destinataires == 'eleves':
            # Récupère directement les élèves sélectionnés
            for eleve_id in donnees['destinataires']['ids']:
                eleve = self.eleve_repo.obtenir(eleve_id)
                if eleve:
                    eleves.append(eleve)

        elif type_destinataires == 'mixte':
            # Récupère les élèves des classes + les élèves spécifiques
            for classe_id in donnees['destinataires']['classes_ids']:
                classe = self.classe_repo.obtenir(classe_id)
                if classe:
                    eleves.extend(classe.eleves)
            for eleve_id in donnees['destinataires']['eleves_ids']:
                eleve = self.eleve_repo.obtenir(eleve_id)
                if eleve:
                    eleves.append(eleve)

        # Peuplement de la table eleve_evenement
        evenement.eleves = list(set(eleves))
        return evenement.to_dict()

    def obtenir_evenement(self, evenement_id):
        """obtenir_evenement permet de récupérer un evenement"""
        evenement = self.evenement_repo.obtenir(evenement_id)
        if not evenement:
            return None
        return evenement.to_dict()

    def obtenir_evenements_par_eleve(self, eleve_id):
        """
        Récupère tous les événements d'un élève.

        Arguments :
            eleve_id (str) : Identifiant unique de l'élève.

        Retourne :
            list : Liste des événements de l'élève ou None si aucun trouvé.
        """
        eleve = self.eleve_repo.obtenir(eleve_id)
        if not eleve:
            return None
        return [evenement.to_dict() for evenement in eleve.evenements]

    def obtenir_evenements_par_professeur(self, professeur_id):
        """
        obtenir_evenement_par_professeur permet de récupérer
        les événements à partir de ID du professeur.
        """
        evenements = self.evenement_repo.obtenir_evenements_par_professeur(professeur_id)
        if not evenements:
            return None
        return [evenement.to_dict() for evenement in evenements]

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

    # Notification
    def creer_notification(self, donnees):
        """
        Crée une nouvelle notification dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            de la notification (utilisateur_id, type, titre
            et message).

        Retourne :
            dict : Dictionnaire contenant les informations
            de la notification créée.
        """
        notification = Notification(
            utilisateur_id=donnees['utilisateur_id'],
            type=donnees['type'],
            titre=donnees['titre'],
            message=donnees['message'],
            lu=False
        )
        self.notification_repo.ajouter(notification)
        return notification.to_dict()

    def obtenir_notification(self, notification_id):
        """obtenir_notification permet de récupère une notification"""
        notification = self.notification_repo.obtenir(notification_id)
        if not notification:
            return None
        return notification.to_dict()

    def obtenir_notifications_par_utilisateur(self, utilisateur_id):
        """
        obtenir_notifications_par_utilisateur permet de récupérer
        les notifications à partir de ID de l'utilisateur'.
        """
        notifications = self.notification_repo.obtenir_notifications_par_utilisateur(utilisateur_id)
        if not notifications:
            return None
        return [notification.to_dict() for notification in notifications]

    def obtenir_notifications_non_lues(self, utilisateur_id):
        """
        obtenir_notifications_non_lues permet de récupérer
        les notifications à partir de ID de l'utilisateur'.
        """
        notifications = self.notification_repo.obtenir_notifications_non_lues(utilisateur_id)
        if not notifications:
            return None
        return [notification.to_dict() for notification in notifications]

    def marquer_notification_lue(self, notification_id):
        """
        Marque une notification comme lue.

        Arguments :
            notification_id (str) : Identifiant unique de la notification.

        Retourne :
            dict : Dictionnaire contenant les informations
            de la notification mise à jour.
        """
        notification = self.notification_repo.obtenir(notification_id)
        if not notification:
            return None
        self.notification_repo.mis_a_jour(notification_id, {'lu': True})
        return self.notification_repo.obtenir(notification_id).to_dict()

    def marquer_toutes_notifications_lue(self, utilisateur_id):
        """
        Marque toutes les notifications d'un utilisateur comme lues.

        Arguments :
            utilisateur_id (str) : Identifiant unique de l'utilisateur.

        Retourne :
            list : Liste des notifications mises à jour.
        """
        notifications = self.notification_repo.obtenir_notifications_par_utilisateur(utilisateur_id)
        if not notifications:
            return None
        for notification in notifications:
            self.notification_repo.mis_a_jour(notification.id, {'lu': True})
        return [notification.to_dict() for notification in notifications]

    def supprimer_notification(self, notification_id):
        """Supprimer une notification existant et toutes les données associées (cascade)."""
        self.notification_repo.supprime(notification_id)
