#!/usr/bin/python3
"""
Repository spécifique pour le modèle Utilisateur.

Ce module définit la classe UtilisateurRepository qui étend
SQLAlchemyRepository avec des méthodes spécifiques aux utilisateurs.
"""

from planifPro.backend.classes.utilisateur import Utilisateur
from planifPro import db
from planifPro.backend.persistence import SQLAlchemyRepository


class UtilisateurRepository(SQLAlchemyRepository):
    """
    Repository pour le modèle Utilisateur.

    Hérite de SQLAlchemyRepository et ajoute des méthodes
    spécifiques à la gestion des utilisateurs.
    """
    def __init__(self):
        super().__init__(Utilisateur)

    def obtenir_par_email(self, email):
        """
        Récupère un utilisateur par son adresse email.

        Arguments :
            email (str) : Adresse email de l'utilisateur.

        Retourne :
            Utilisateur : Instance de l'utilisateur ou None si non trouvé.
        """
        return self.model.query.filter_by(email=email).first()
