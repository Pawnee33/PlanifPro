#!/usr/bin/python3
"""
Repository spécifique pour le modèle Evenement.

Ce module définit la classe EvenementRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des événements, telles que la récupération des
événements par professeur.
"""

from planifPro.backend.classes.evenement import Evenement
from planifPro import db
from planifPro.backend.persistence import SQLAlchemyRepository


class EvenementRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Evenement.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des événements comme la recherche
    par professeur.
    """
    def __init__(self):
        super().__init__(Evenement)

    def obtenir_evenements_par_professeur(self, professeur_id):
        """
        Récupère tous les événements d'un professeur.

        Arguments :
            professeur_id (str) : Identifiant unique du professeur.

        Retourne :
            list : Liste des événements du professeur ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(professeur_id=professeur_id).all()

    def obtenir_evenements_par_eleve(self, eleve_id):
        """
        Récupère tous les événements d'un élève.

        Arguments :
            eleve_id (str) : Identifiant unique de l'élève.

        Retourne :
            list : Liste des événements de l'élève ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(eleve_id=eleve_id).all()
