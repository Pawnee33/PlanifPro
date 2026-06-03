#!/usr/bin/python3
"""
Modèle Notification.

Ce module définit l'entité Notification, qui représente les
notifications envoyées aux utilisateurs de l'application.
"""


from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from datetime import date, time, datetime, timezone
from sqlalchemy.orm import validates


class Notification(EntiteBase):
    """
    Le modèle Notification.

    Représente une notification dans le système. Contient le type,
    le type, le message ainsi que le statut de lecture de la
    notification envoyée à un utilisateur.
    """
    __tablename__ = 'notifications'

    utilisateur_id = db.Column(
        db.String(36),
        db.ForeignKey('utilisateurs.id'),
        nullable=False
    )

    type = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    lu =db.Column(db.Boolean, nullable=False, default=False)

    @validates('type')
    def validate_type(self, key, value):
        """
        Vérifie si le type est valide et si il appartient aux valeurs autorisées: 
        voeux soumis, créneau confirmé, événement accepté, code de la classe,
        collecte des voeux, créneau attribué, objectif et événement.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le type doit être une chaîne de caractères")
        if value not in [
            'voeux_soumis',
            'creneau_confirme',
            'evenement_accepte',
            'code_classe',
            'collecte_voeux',
            'creneau_attribue',
            'objectif',
            'evenement']:
            raise ValueError("Type invalide")
        return value

    @validates('type')
    def validate_type(self, key, value):
        """
        Vérifie si le type est une string et ne dépasse pas les 50 caractères.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le type est obligatoire et doit être une string")
        if len(value) > 50:
            raise ValueError("Le type ne doit pas dépasser 50 caractères")
        return value

    @validates('message')
    def validate_message(self, key, value):
        """
        Vérifie si le message est une chaîne de caractères et non vide.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le message dois être une chaîne de caractères")
        return value

    @validates('lu')
    def validate_lu(self, key, value):
        """
        Vérifie si lu est un booléen.
        """
        if not isinstance(value, bool):
            raise ValueError("Le statut de lecture doit être un booléen")
        return value

    def to_dict(self):
        """
        Convertit l'instance Notification en dictionnaire.

        Retourne :
            dict : Dictionnaire contenant les informations
            des notifications (id, utilisateur_id, type, titre,
            message et lu).
        """
        donnees = super().to_dict()
        donnees.update({
            'utilisateur_id': self.utilisateur_id,
            'type': self.type,
            'titre': self.titre,
            'message': self.message,
            'lu': self.lu
        })
        return donnees
