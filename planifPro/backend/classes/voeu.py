#!/usr/bin/python3
"""
Modèle Voeu.

Ce module définit l'entité Voeu, qui représente les vœux
d'horaires soumis par un élève pour une classe donnée.
"""


from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from datetime import datetime, timezone
from sqlalchemy.orm import validates


class Voeu(EntiteBase):
    """
    Le modèle Voeu.

    Représente les vœux d'horaires d'un élève pour une classe.
    Contient les créneaux souhaités, le statut de soumission
    ainsi que la date de soumission.
    """
    __tablename__ = 'voeux'

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
    
    creneaux_souhaites = db.Column(db.JSON, nullable=False)
    statut = db.Column(db.String(50), nullable=False)
    soumis_le =db.Column(db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


    @validates('statut')
    def validate_statut(self, key, value):
        """
        Vérifie si le statut est valide et si il appartient aux valeurs autorisées: 
        en attente, soumis et validé.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le statut doit être une chaîne de caractères")
        if value not in [
            'en_attente',
            'soumis',
            'valide']:
            raise ValueError("Statut invalide")
        return value

    @validates('creneaux_souhaites')
    def validate_creneaux_souhaites(self, key, value):
        """
        Vérifie si les créneaux souhaités sont un dictionnaire non vide.
        """
        if not isinstance(value, dict):
            raise ValueError("Les créneaux souhaitée doivent être un dictionnaire")
        if not value:
            raise ValueError("Les créneaux souhaités doivent être remplit")
        return value
