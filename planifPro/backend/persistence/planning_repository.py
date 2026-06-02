#!/usr/bin/python3
"""
Repository spécifique pour le modèle Planning.

Ce module définit la classe PlanningRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des plannings, telles que la récupération des
propositions par classe et du planning validé.
"""

from planifPro.backend.classes.planning import Planning
from planifPro import db
from planifPro.backend.persistence import SQLAlchemyRepository


class PlanningRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Planning.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des plannings comme la recherche
    par classe et par statut.
    """
    def __init__(self):
        super().__init__(Planning)

    def obtenir_plannings_par_classe(self, classe_id):
        """
        Récupère toutes les propositions de planning d'une classe.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            list : Liste des propositions de planning ou une liste vide si aucune trouvée.
        """
        return self.model.query.filter_by(classe_id=classe_id).all()

    def obtenir_planning_valide(self, classe_id):
        """
        Récupère le planning validé d'une classe.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            Planning : Instance du planning validé ou None si non trouvé.
        """
        return self.model.query.filter_by(classe_id=classe_id, statut='valide').first()
