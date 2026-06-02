#!/usr/bin/python3
"""
Repository spécifique pour le modèle Objectif.

Ce module définit la classe ObjectifRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des objectifs, telles que la récupération des
objectifs par élève et par créneau.
"""

from planifPro.backend.classes.objectif import Objectif
from planifPro import db
from planifPro.backend.persistence import SQLAlchemyRepository


class ObjectifRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Objectif.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des objectifs comme la recherche
    par élève et par créneau.
    """
    def __init__(self):
        super().__init__(Objectif)

    def obtenir_objectifs_par_eleve(self, eleve_id):
        """
        Récupère tous les objectifs d'un élève.

        Arguments :
            eleve_id (str) : Identifiant unique de l'élève.

        Retourne :
            list : Liste des objectifs de l'élève ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(eleve_id=eleve_id).all()

    def obtenir_objectifs_par_creneau(self, creneau_id):
        """
        Récupère tous les objectifs d'un créneau.

        Arguments :
            creneau_id (str) : Identifiant unique du créneau.

        Retourne :
            list : Liste des objectifs du créneau ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(creneau_id=creneau_id).all()
