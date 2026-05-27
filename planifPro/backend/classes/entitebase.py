#!/usr/bin/python3
"""
Entité base.

Ce module définit la classe EntiteBase, qui fournit des attributs
et des comportements communs à tous les modèles de domaine, tels que
l'identification unique et la gestion des horodatages.
"""

from planifPro import db
import uuid
from datetime import datetime, timezone


class EntiteBase(db.Model):
    """
    Classe de base pour tous les modèles.

    Fournit un identifiant unique ainsi que des horodatages pour la
    création et la dernière mise à jour. Comprend également des méthodes
    d'aide pour mettre à jour et enregistrer les modifications d'état
    """
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
        )
    cree_le = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
        )
    modifie_le = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
        )

    def sauvegarder(self):
        """
        Mettre à jour l'horodatage de la dernière modification.

        Cette méthode doit être appelée chaque fois que l'état de l'objet
        change, afin de refléter l'heure de la dernière mise à jour.
        """
        self.modifie_le = datetime.now(timezone.utc)

    def mise_a_jour(self, data):
        """
        Mise à jour des attributs d'un modèle à partir d'un dictionnaire.

        Parcourt les paires clé-valeur fournies et met à jour
        uniquement les attributs existants, puis actualise l'horodatage
        de la mise à jour.

        Arguments :
            data (dict) : Dictionnaire contenant les attributs à mettre à jour.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.sauvegarder()
