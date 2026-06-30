#!/usr/bin/python3
"""
Modèle Créneau.

Ce module définit l'entité Créneau, qui représente un créneau
de cours attribué à un élève dans le cadre d'une classe.
"""

from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from datetime import date, time, datetime, timezone
from sqlalchemy.orm import validates


class Creneau(EntiteBase):
    """
    Le modèle Créneau.

    Représente un créneau de cours dans le système. Contient
    les informations temporelles (jour, date début, date fin,
    heure début, heure fin, durée), le type de cours, le statut
    ainsi que les liens vers le planning, l'élève et la classe associés.
    """
    __tablename__ = 'creneaux'

    planning_id = db.Column(
        db.String(36),
        db.ForeignKey('plannings.id'),
        nullable=False
    )

    eleve_id = db.Column(
        db.String(36),
        db.ForeignKey('eleves.utilisateur_id'),
        nullable=False
    )

    classe_id = db.Column(
        db.String(36),
        db.ForeignKey('classes.id'),
        nullable=False
    )

    type = db.Column(db.String(50), nullable=False)
    jour = db.Column(db.String(50), nullable=False)
    semaine_alternance = db.Column(db.String(10), nullable=True)
    date_debut = db.Column(db.Date, nullable=True)
    date_fin = db.Column(db.Date, nullable=True)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)
    duree_minutes = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.String(50), nullable=False)

    objectifs = db.relationship(
        'Objectif', backref='creneau',
        lazy=True, cascade='all, delete-orphan'
    )

    @validates('statut')
    def validate_statut(self, key, value):
        """
        Vérifie si le statut est valide et si il appartient aux valeurs autorisées:
        en attente, confirmé, validé et annulé.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le statut doit être une chaîne de caractères")
        if value not in ['en_attente', 'confirme', 'valide', 'annule']:
            raise ValueError("Statut invalide")
        return value

    @validates('type')
    def validate_type(self, key, value):
        """
        Vérifie si le type est une chaîne de caractères non vide.
        """
        if not isinstance(value, str):
            raise ValueError("Le type doit être une chaîne de caractères")
        if not value.strip():
            raise ValueError("Le type ne peut pas être vide")
        return value

    @validates('jour')
    def validate_jour(self, key, value):
        """
        Vérifie si le jour est une chaîne de caractères non vide.
        """
        if not isinstance(value, str):
            raise ValueError("Le jour doit être une chaîne de caractères")
        if not value.strip():
            raise ValueError("Le jour ne peut pas être vide")
        return value

    @validates('date_debut')
    def validate_date_debut(self, key, value):
        """
        Vérifie si la date de début est une date valide ou None.
        """
        if value is None:
            return value
        if not isinstance(value, date):
            raise ValueError("La date de début doit être une date valide")
        return value

    @validates('date_fin')
    def validate_date_fin(self, key, value):
        """
        Vérifie si la date de fin est une date valide et
        arrive après la date de début.
        """
        if value is None:
            return value
        if not isinstance(value, date):
            raise ValueError("La date de fin doit être une date valide")
        if self.date_debut and value < self.date_debut:
            raise ValueError("La date de fin doit être après la date de début")
        return value

    @validates('heure_debut')
    def validate_heure_debut(self, key, value):
        """
        Vérifie si l'heure de début est une heure valide.
        """
        if not isinstance(value, time):
            raise ValueError("L'heure de début doit être une heure valide")
        return value

    @validates('heure_fin')
    def validate_heure_fin(self, key, value):
        """
        Vérifie si l'heure de fin est une heure valide et
        arrive après l'heure de début.
        """
        if not isinstance(value, time):
            raise ValueError("L'heure de fin doit être une heure valide")
        if self.heure_debut and value <= self.heure_debut:
            raise ValueError("L'heure de fin doit être après l'heure de début")
        return value

    @validates('duree_minutes')
    def validate_duree_minutes(self, key, value):
        """Vérifie si la durée des minutes est un entier supérieur à 0."""
        if not isinstance(value, int):
            raise ValueError("La durée des minutes doit être un nombre entier")
        if value <= 0:
            raise ValueError("La durée des minutes doit être supérieur à 0")
        return value

    def to_dict(self):
        """
        Convertit l'instance Creneau en dictionnaire.

        Retourne :
            dict : Dictionnaire contenant les informations
            des creneaux (id, planning_id, eleve_id, classe_id, type,
            jour, date_debut, date_fin, heure_debut, heure_fin,
            duree_minutes et statut).
        """
        donnees = super().to_dict()
        donnees.update({
            'planning_id': self.planning_id,
            'eleve_id': self.eleve_id,
            'classe_id': self.classe_id,
            'type': self.type,
            'jour': self.jour,
            'semaine_alternance': self.semaine_alternance,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'heure_debut': self.heure_debut.isoformat() if self.heure_debut else None,
            'heure_fin': self.heure_fin.isoformat() if self.heure_fin else None,
            'duree_minutes': self.duree_minutes,
            'statut': self.statut
        })
        return donnees
