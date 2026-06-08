#!/usr/bin/python3
"""
Repository spécifique pour le modèle Voeu.

Ce module définit la classe VoeuRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des vœux, telles que la récupération des vœux
par classe et par élève.
"""

from planifPro.backend.classes.voeu import Voeu
from planifPro import db
from planifPro.backend.persistence.repository import SQLAlchemyRepository


class VoeuRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Voeu.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des vœux comme la recherche
    par classe et par élève.
    """
    def __init__(self):
        super().__init__(Voeu)

    def obtenir_voeux_par_classe(self, classe_id):
        """
        Récupère tous les vœux d'une classe.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            list : Liste des vœux de la classe ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(classe_id=classe_id).all()

    def obtenir_voeux_par_eleve(self, eleve_id):
        """
        Récupère tous les vœux d'un élève.

        Arguments :
            eleve_id (str) : Identifiant unique de l'élève.

        Retourne :
            list : Liste des vœux de l'élève ou une liste vide si aucun trouvé.
        """
        return self.model.query.filter_by(eleve_id=eleve_id).all()
