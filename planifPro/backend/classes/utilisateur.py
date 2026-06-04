#!/usr/bin/python3
"""
Modèle Utilisateur.

Ce module définit l'entité Utilisateur, qui hérite d'EntiteBase et
représente les paramètres utilisateur de l'application avec des règles
de validation pour les champs principaux.
"""


from planifPro import bcrypt
from planifPro.backend.classes.entitebase import EntiteBase
from planifPro import db
from sqlalchemy.orm import validates
import re


class Utilisateur(EntiteBase):
    """
    Le modèle Utilisateur.

    Représente les paramètres d'un utilisateur dans le système avec des
    informations d'identité de base et, éventuellement, des privilèges
    d'administration. Une validation est effectuée lors de l'initialisation
    afin de garantir l'intégrité des données.
    """
    __tablename__ = 'utilisateurs'

    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    mot_de_passe_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    token_fcm = db.Column(db.String(255), nullable=True)

    @validates('prenom')
    def validate_prenom(self, key, value):
        """
        Vérifie si le prénom est une string et ne dépasse pas les 50 caractères.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le prénom est obligatoire")
        if len(value) > 50:
            raise ValueError("Le prénom ne doit pas dépasser 50 caractères")
        return value

    @validates('nom')
    def validate_nom(self, key, value):
        """
        Vérifie si le nom est une string et ne dépasse pas les 50 caractères.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le nom est obligatoire")
        if len(value) > 50:
            raise ValueError("Le nom ne doit pas dépasser 50 caractères")
        return value

    @validates('email')
    def validate_email(self, key, value):
        """
        Vérifie si l'adresse email est une string et a le bon format.
        """
        if not isinstance(value, str):
            raise ValueError("L'adresse email est obligatoire")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, value):
            raise ValueError("Format d'email invalide")
        return value

    def hash_password(self, password):
        """Hache le mot de passe avant de l'enregistrer."""
        self.mot_de_passe_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe fourni correspond au mot_de_passe haché."""
        return bcrypt.check_password_hash(self.mot_de_passe_hash, password)

    @validates('role')
    def validate_role(self, key, value):
        """
        Vérifie si le rôle est valide.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le rôle est obligatoire")
        if value not in ['professeur', 'eleve']:
            raise ValueError("Le rôle doit être 'professeur' ou 'eleve'")
        return value

    @validates('token_fcm')
    def validate_token_fcm(self, key, value):
        """
        Vérifie si le token_fcm est valide.
        """
        if value is None:
            return value
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le token FCM doit être une chaîne de caractères valide")
        return value

    def to_dict(self):
        """
        Convertit l'instance Utilisateur en dictionnaire.

        Retourne :
            dict : Dictionnaire contenant les informations
            de l'utilisateur (id, prenom, nom, email, role, token_fcm).
        """
        donnees = super().to_dict()
        donnees.update({
            'prenom': self.prenom,
            'nom': self.nom,
            'email': self.email,
            'role': self.role,
            'token_fcm': self.token_fcm
        })
        return donnees
