#!/usr/bin/python3
"""
Repository spécifique pour le modèle Creneau.

Ce module définit la classe CreneauRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des créneaux, telles que la récupération des
créneaux par classe, par élève et par planning.
"""

from planifPro.backend.classes.creneau import Creneau
from planifPro import db
from planifPro.backend.persistence import SQLAlchemyRepository


class CreneauRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Creneau.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des créneaux comme la recherche
    par classe, par élève et par planning.
    """
    def __init__(self):
        super().__init__(Creneau)

    def obtenir_creneaux_par_classe(self, classe_id):
        """
        Récupère tous les créneaux d'une classe.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            list : Liste des créneaux de la classe ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(classe_id=classe_id).all()

    def obtenir_creneaux_par_eleve(self, eleve_id):
        """
        Récupère tous les créneaux d'un élève.

        Arguments :
            eleve_id (str) : Identifiant unique de l'élève.

        Retourne :
            list : Liste des créneaux de l'élève ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(eleve_id=eleve_id).all()

    def obtenir_creneaux_par_planning(self, planning_id):
        """
        Récupère tous les créneaux d'un planning.

        Arguments :
            planning_id (str) : Identifiant unique du planning.

        Retourne :
            list : Liste des créneaux du planning ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(planning_id=planning_id).all()
