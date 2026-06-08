#!/usr/bin/python3
"""
Repository spécifique pour le modèle CreneauPerso.

Ce module définit la classe CreneauPersoRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des créneaux personnels.
"""

from planifPro.backend.classes.creneau_perso import CreneauPerso
from planifPro import db
from planifPro.backend.persistence.repository import SQLAlchemyRepository


class CreneauPersoRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle CreneauPerso.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des créneaux personnels.
    """
    def __init__(self):
        super().__init__(CreneauPerso)

    def obtenir_creneaux_perso_par_utilisateur(self, utilisateur_id):
        """
        Récupère tous les créneaux personnels d'un utilisateur.

        Arguments :
            utilisateur_id (str) : Identifiant unique de l'utilisateur.

        Retourne :
            list : Liste des créneaux personnels ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(utilisateur_id=utilisateur_id).all()
