#!/usr/bin/python3
"""
Modèle Evenement.

Ce module définit l'entité Evenement, qui représente les événements
que le Professeur peut créer et inviter ses élèves.
"""


from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from datetime import date, time, datetime, timezone
from sqlalchemy.orm import validates


class Evenement(EntiteBase):
    """
    Le modèle Evenement.

    Représente un événement créé par un professeur dans le système.
    Contient le titre, la description, la date et l'heure ainsi
    que les destinataires concernés (classes ou élèves).
    """
    __tablename__ = 'evenements'

    professeur_id = db.Column(
        db.String(36),
        db.ForeignKey('professeurs.utilisateur_id'),
        nullable=False
    )

    titre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_heure =db.Column(db.DateTime, nullable=False)
    destinataires = db.Column(db.JSON, nullable=False)

    @validates('titre')
    def validate_titre(self, key, value):
        """
        Vérifie si le titre est une string et ne dépasse pas les 50 caractères.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le titre est obligatoire et doit être une string")
        if len(value) > 50:
            raise ValueError("Le titre ne doit pas dépasser 50 caractères")
        return value

    @validates('description')
    def validate_description(self, key, value):
        """
        Vérifie si la description est une chaîne de caractères et non vide.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("La description dois être une chaîne de caractères")
        return value

    @validates('date_heure')
    def validate_date_heure(self, key, value):
        """Vérifie si la date et l'heure est une date et une heure valide."""
        if not isinstance(value, datetime):
            raise ValueError("La date et l'heure doivent être une date et une heure valide")
        return value

    @validates('destinataires')
    def validate_destinataires(self, key, value):
        """
        Vérifie si les destinataires sont un dictionnaire non vide.
        """
        if not isinstance(value, dict):
            raise ValueError("Les destinataires doivent être un dictionnaire")
        if not value:
            raise ValueError("Les destinataires doivent être remplit")
        return value
