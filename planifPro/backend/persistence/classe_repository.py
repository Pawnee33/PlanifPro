#!/usr/bin/python3
"""
Repository spécifique pour le modèle Classe.

Ce module définit la classe ClasseRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques à la
gestion des classes, telles que la recherche par code unique
et la récupération des classes d'un professeur.
"""

from planifPro.backend.classes.classe import Classe
from planifPro import db
from planifPro.backend.persistence import SQLAlchemyRepository


class ClasseRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Classe.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des classes comme la recherche
    par code unique et par professeur.
    """
    def __init__(self):
        super().__init__(Classe)

    def obtenir_classe_code(self, code_classe):
        """
        Récupère une classe par son code unique.

        Arguments :
            code_classe (str) : Code unique de la classe.

        Retourne :
            Classe : Instance de la classe ou None si non trouvée.
        """
        return self.model.query.filter_by(code_classe=code_classe).first()

    def obtenir_classes_par_professeur(self, professeur_id):
        """
        Récupère toutes les classes d'un professeur.

        Arguments :
            professeur_id (str) : Identifiant unique du professeur.

        Retourne :
            list : Liste des classes du professeur ou une liste vide si aucune trouvée.
        """
        return self.model.query.filter_by(professeur_id=professeur_id).all()
