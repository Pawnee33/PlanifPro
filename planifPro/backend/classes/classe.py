#!/usr/bin/python3
"""
Modèle Classe.

Ce module définit l'entité Classe, qui représente une classe
créée par un professeur dans l'application. Chaque classe est
liée à un professeur et contient les informations de planification
telles que la période, les jours et horaires, ainsi que les
contraintes de vœux.
"""


from planifPro import db
from planifPro.backend.classes.entitebase import EntiteBase
from sqlalchemy.orm import validates


class Classe(EntiteBase):
    """
    Le modèle Classe.

    Représente une classe créée par un professeur dans le système.
    Contient les informations de planification telles que la période,
    les jours et horaires disponibles, les contraintes de vœux ainsi
    que le statut de la collecte et du planning.
    """
    __tablename__ = 'classes'

    professeur_id = db.Column(
        db.String(36),
        db.ForeignKey('professeurs.utilisateur_id'),
        nullable=False
    )
    
    nom = db.Column(db.String(50), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    jours_horaires = db.Column(db.JSON, nullable=False)
    nombre_voeux_requis = db.Column(db.Integer, nullable=False)
    nombre_jours_min = db.Column(db.Integer, nullable=False)
    code_classe = db.Column(db.String(8), nullable=False, unique=True)
    statut = db.Column(db.String(50), nullable=False)

    voeux = db.relationship(
        'Voeu', backref='classe',
        lazy=True, cascade='all, delete-orphan'
    )

    planning = db.relationship(
        'Planning', backref='classe',
        lazy=True, cascade='all, delete-orphan'
    )

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

    @validates('statut')
    def validate_statut(self, key, value):
        """
        Vérifie si le statut est valide et si il appartient aux valeurs autorisées: 
        classe activé, collecte activé, planning généré et planning terminé
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le statut doit être une chîne de caractères")
        if value not in [
            'classe_active',
            'collecte_active',
            'planning_genere',
            'planning_termine']:
            raise ValueError("Statut invalide")
        return value

    @validates('nombre_voeux_requis')
    def validate_nombre_voeux_requis(self, key, value):
        """Vérifie si le nombre de vœux requis est un entier supérieur à 0."""
        if not isinstance(value, int):
            raise ValueError(
                "Le nombre de voeux requis doit être un nombre entier")
        if value <= 0:
            raise ValueError("Le nombre de voeux doit être supérieur à 0")
        return value

    @validates('nombre_jours_min')
    def validate_nombre_jours_min(self, key, value):
        """Vérifie si le nombre de jours minimum est un entier supérieur à 0."""
        if not isinstance(value, int):
            raise ValueError(
                "Le nombre de jours minimum doit être un nombre entier")
        if value <= 0:
            raise ValueError("Le nombre de jours minimum doit être supérieur à 0")
        return value

    @validates('code_classe')
    def validate_code_classe(self, key, value):
        """Vérifie si le code de la classe est une chaîne de caractères
        d'exactement 8 caractères."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                "Le code de la classe doit être une chaîne de caractères")
        if len(value) != 8:
            raise ValueError("Le code de la classe doit avoir exactement 8 caractères")
        return value
