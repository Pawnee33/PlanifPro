#!/usr/bin/python3
"""
Modèle Élève.

Ce module définit l'entité Élève, qui hérite d'Utilisateur et
représente un élève dans l'application avec ses relations
vers les classes, voeux, créneaux,événements et objectifs.
"""


from planifPro import db
from planifPro.backend.classes.utilisateur import Utilisateur
from planifPro.backend.classes.tables_relations import eleve_classe, eleve_evenement


class Eleve(Utilisateur):
    """
    Le modèle Élève.

    Représente un élève dans le système. Hérite de tous les
    attributs d'Utilisateur et définit les relations avec les
    classes auxquelles il appartient, les vœux qu'il soumet,
    les créneaux qui lui sont attribués, les objectifs
    pédagogiques qu'il reçoit et les événements auxquels
    il participe.
    """
    __tablename__ = 'eleves'

    utilisateur_id = db.Column(
        db.String(36),
        db.ForeignKey('utilisateurs.id'),
        primary_key=True
    )
    
    classes = db.relationship(
        'Classe', secondary=eleve_classe,
        lazy=True
    )

    evenements = db.relationship(
        'Evenement', secondary=eleve_evenement,
        backref='eleves',
        lazy=True
    )

    voeux = db.relationship(
        'Voeu', backref='eleve',
        lazy=True, cascade='all, delete-orphan'
    )

    creneaux = db.relationship(
        'Creneau', backref='eleve',
        lazy=True, cascade='all, delete-orphan'
    )

    objectifs = db.relationship(
        'Objectif', backref='eleve_objectifs',
        lazy=True, cascade='all, delete-orphan'
    )

    def to_dict(self):
        """
        Convertit l'instance Eleve en dictionnaire.

        Retourne :
            dict : Dictionnaire contenant les informations
            de l'élève (héritées de Utilisateur + utilisateur_id).
        """
        donnees = super().to_dict()
        donnees.update({
            'utilisateur_id': self.utilisateur_id
        })
        return donnees
