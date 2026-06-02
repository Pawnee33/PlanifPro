#!/usr/bin/python3
"""
Repository spécifique pour le modèle Notification.

Ce module définit la classe NotificationRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des notifications, telles que la récupération des
notifications par utilisateur et des notifications non lues.
"""

from planifPro.backend.classes.notification import Notification
from planifPro import db
from planifPro.backend.persistence import SQLAlchemyRepository


class NotificationRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Notification.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des notifications comme la recherche
    par utilisateur et par statut de lecture.
    """
    def __init__(self):
        super().__init__(Notification)

    def obtenir_notifications_par_utilisateur(self, utilisateur_id):
        """
        Récupère toutes les notifications d'un utilisateur.

        Arguments :
            utilisateur_id (str) : Identifiant unique de l'utilisateur.

        Retourne :
            list : Liste des notifications de l'utilisateur ou une liste vide si aucune trouvée.
        """
        return self.model.query.filter_by(utilisateur_id=utilisateur_id).all()

    def obtenir_notifications_non_lues(self, utilisateur_id):
        """
        Récupère toutes les notifications non lues d'un utilisateur.

        Arguments :
            utilisateur_id (str) : Identifiant unique de l'utilisateur.

        Retourne :
            list : Liste des notifications non lues ou une liste vide si aucune trouvée.
        """
        return self.model.query.filter_by(utilisateur_id=utilisateur_id, lu=False).all()
