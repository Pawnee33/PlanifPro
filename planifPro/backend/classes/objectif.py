#!/usr/bin/python3
"""
Modèle Objectif.

Ce module définit l'entité Objectif, qui représente les objectifs
et conseils des cours attribué à un élève.
"""


from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from datetime import date, time, datetime, timezone
from sqlalchemy.orm import validates


class Objectif(EntiteBase):
    """
    Le modèle Objectif.

    Représente les objectifs et conseils des cours dans le système.
    Contient les informations du contenu des objectifs et les conseils des cours.
    """
    __tablename__ = 'objectifs'

    professeur_id = db.Column(
        db.String(36),
        db.ForeignKey('professeurs.utilisateur_id'),
        nullable=False
    )

    eleve_id = db.Column(
        db.String(36),
        db.ForeignKey('eleves.utilisateur_id'),
        nullable=False
    )

    creneau_id = db.Column(
        db.String(36),
        db.ForeignKey('creneaux.id'),
        nullable=False
    )
    
    contenu = db.Column(db.Text, nullable=False)
    conseils = db.Column(db.Text, nullable=True)


    @validates('contenu')
    def validate_contenu(self, key, value):
        """
        Vérifie si le contenu est une chaîne de caractères et non vide.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le contenu dois être une chaîne de caractères")
        return value

    @validates('conseils')
    def validate_conseils(self, key, value):
        """
        Vérifie si les conseils est une chaîne de caractères et non vide.
        """
        if value is None:
            return value
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Les conseils dois être une chaîne de caractères")
        return value

    def to_dict(self):
        """
        Convertit l'instance Objectif en dictionnaire.

        Retourne :
            dict : Dictionnaire contenant les informations
            des objectifs (id, professeur_id, eleve_id, creneau_id, contenu,
            et conseils).
        """
        donnees = super().to_dict()
        donnees.update({
            'professeur_id': self.professeur_id,
            'eleve_id': self.eleve_id,
            'creneau_id': self.creneau_id,
            'contenu': self.contenu,
            'conseils': self.conseils
        })
        return donnees
