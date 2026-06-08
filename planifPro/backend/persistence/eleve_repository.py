#!/usr/bin/python3
"""
Repository spécifique pour le modèle Eleve.

Ce module définit la classe EleveRepository qui étend
SQLAlchemyRepository avec les opérations CRUD de base pour les Eleves.
"""

from planifPro.backend.classes.eleve import Eleve
from planifPro import db
from planifPro.backend.persistence.repository import SQLAlchemyRepository


class EleveRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Eleve.

    Hérite de SQLAlchemyRepository et fournit les opérations
    CRUD de base pour la gestion des Eleves.
    """
    def __init__(self):
        super().__init__(Eleve)
