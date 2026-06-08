#!/usr/bin/python3
"""
Repository spécifique pour le modèle Professeur.

Ce module définit la classe ProfesseurRepository qui étend
SQLAlchemyRepository avec les opérations CRUD de base pour les professeurs.
"""

from planifPro.backend.classes.professeur import Professeur
from planifPro import db
from planifPro.backend.persistence.repository import SQLAlchemyRepository


class ProfesseurRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Professeur.

    Hérite de SQLAlchemyRepository et fournit les opérations
    CRUD de base pour la gestion des professeurs.
    """
    def __init__(self):
        super().__init__(Professeur)
