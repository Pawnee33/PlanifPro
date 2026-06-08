#!/usr/bin/python3
"""
Modèle Professeur.

Ce module définit l'entité Professeur, qui hérite d'Utilisateur et
représente un professeur dans l'application avec ses relations
vers les classes, événements et objectifs.
"""


from planifPro.backend.classes.utilisateur import Utilisateur
from planifPro import db


class Professeur(Utilisateur):
    """
    Le modèle Professeur.

    Représente un professeur dans le système. Hérite de tous les
    attributs d'Utilisateur et définit les relations avec les classes
    qu'il gère, les événements qu'il crée et les objectifs
    pédagogiques qu'il rédige.
    """
    __tablename__ = 'professeurs'

    utilisateur_id = db.Column(
        db.String(36),
        db.ForeignKey('utilisateurs.id'),
        primary_key=True
    )
    
    classes = db.relationship(
        'Classe', backref='professeur',
        lazy=True,
        cascade='all, delete-orphan'
    )

    evenements = db.relationship(
        'Evenement', backref='professeur',
        lazy=True,
        cascade='all, delete-orphan'
    )

    objectifs = db.relationship(
        'Objectif', backref='professeur',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        """
        Convertit l'instance Professeur en dictionnaire.

        Retourne :
            dict : Dictionnaire contenant les informations
            du professeur (héritées de Utilisateur + utilisateur_id).
        """
        donnees = super().to_dict()
        donnees.update({
            'utilisateur_id': self.utilisateur_id
        })
        return donnees
