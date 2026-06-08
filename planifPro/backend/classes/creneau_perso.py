#!/usr/bin/python3
"""
Modèle CreneauPerso.

Ce module définit l'entité CreneauPerso, qui représente un créneau
personnel ajouté par un utilisateur dans son calendrier.
"""

from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from datetime import time
from sqlalchemy.orm import validates


class CreneauPerso(EntiteBase):
    """
    Le modèle CreneauPerso.

    Représente un créneau personnel dans le système. Contient
    les informations temporelles (jour, heure début, heure fin)
    ainsi qu'un titre et une description optionnelle.
    """
    __tablename__ = 'creneaux_perso'

    utilisateur_id = db.Column(
        db.String(36),
        db.ForeignKey('utilisateurs.id'),
        nullable=False
    )

    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    jour = db.Column(db.String(50), nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)

    @validates('titre')
    def validate_titre(self, key, value):
        """Vérifie si le titre est une chaîne de caractères non vide."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le titre doit être une chaîne de caractères non vide")
        if len(value) > 100:
            raise ValueError("Le titre ne doit pas dépasser 100 caractères")
        return value

    @validates('heure_debut')
    def validate_heure_debut(self, key, value):
        """Vérifie si l'heure de début est une heure valide."""
        if not isinstance(value, time):
            raise ValueError("L'heure de début doit être une heure valide")
        return value

    @validates('heure_fin')
    def validate_heure_fin(self, key, value):
        """Vérifie si l'heure de fin est valide et après l'heure de début."""
        if not isinstance(value, time):
            raise ValueError("L'heure de fin doit être une heure valide")
        if self.heure_debut and value <= self.heure_debut:
            raise ValueError("L'heure de fin doit être après l'heure de début")
        return value

    def to_dict(self):
        """Convertit l'instance CreneauPerso en dictionnaire."""
        donnees = super().to_dict()
        donnees.update({
            'utilisateur_id': self.utilisateur_id,
            'titre': self.titre,
            'description': self.description,
            'jour': self.jour,
            'heure_debut': self.heure_debut.isoformat() if self.heure_debut else None,
            'heure_fin': self.heure_fin.isoformat() if self.heure_fin else None,
        })
        return donnees
