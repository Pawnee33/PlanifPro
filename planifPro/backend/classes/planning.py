#!/usr/bin/python3
"""
Modèle Planning.

Ce module définit l'entité Planning, qui représente les propositions
générées par l'algorithme de génération de planning en fonction des voeux
des élèves.
"""


from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from datetime import datetime, timezone
from sqlalchemy.orm import validates


class Planning(EntiteBase):
    """
    Le modèle Planning.

    Représente les propositions de planning générées par l'algorithme.
    Contient les plannings générés, le statut du planning choisi,
    ainsi que la date de validation.
    """
    __tablename__ = 'plannings'

    classe_id = db.Column(
        db.String(36),
        db.ForeignKey('classes.id'),
        nullable=False
    )

    numero_proposition = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.String(50), nullable=False)
    valide_le =db.Column(db.DateTime, nullable=True)

    creneaux = db.relationship(
        'Creneau', backref='planning',
        lazy=True, cascade='all, delete-orphan'
    )


    @validates('statut')
    def validate_statut(self, key, value):
        """
        Vérifie si le statut est valide et si il appartient aux valeurs autorisées: 
        généré, sélectionné, modifié et validé.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le statut doit être une chaîne de caractères")
        if value not in [
            'genere',
            'selectionne',
            'modifie',
            'valide']:
            raise ValueError("Statut invalide")
        return value

    @validates('numero_proposition')
    def validate_numero_proposition(self, key, value):
        """
        Vérifie si le numéro de proposition est un entier et
        supérieur à zéro.
        """
        if not isinstance(value, int):
            raise ValueError("Le numéro de proposition doit être un entier")
        if value <= 0:            
            raise ValueError("Le numéro de proposition doit être supérieur à 0")
        return value
