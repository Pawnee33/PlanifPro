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
from datetime import date, datetime, timezone
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
    couleur = db.Column(db.String(7), nullable=True)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    jours_horaires = db.Column(db.JSON, nullable=False)
    nombre_propositions = db.Column(db.Integer, nullable=False)
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

    @validates('date_debut')
    def validate_date_debut(self, key, value):
        """Vérifie si la date de début est une date valide."""
        if not isinstance(value, date):
            raise ValueError("La date de début doit être une date valide")
        return value
        
    @validates('date_fin')
    def validate_date_fin(self, key, value):
        """Vérifie si la date de fin est une date valide et
        si elle est postérieure à la date de début."""
        if not isinstance(value, date):
            raise ValueError("La date de fin doit être une date valide")
        if self.date_debut and value <= self.date_debut:
            raise ValueError("La date de fin doit être après la date de début")
        return value

    @validates('jours_horaires')
    def validate_jours_horaires(self, key, value):
        """
        Vérifie si les jours horaires sont un dictionnaire non vide.
        """
        if not isinstance(value, dict):
            raise ValueError("Les jours horaires doivent être un dictionnaire")
        if not value:
            raise ValueError("Les jours horaires doivent être remplit")
        return value

    @validates('statut')
    def validate_statut(self, key, value):
        """
        Vérifie si le statut est valide et si il appartient aux valeurs autorisées: 
        classe activé, collecte activé, planning généré et planning terminé
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le statut doit être une chaîne de caractères")
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

    @validates('nombre_propositions')
    def validate_nombre_propositions(self, key, value):
        """
        Vérifie si le nombre de propositions est un entier et
        supérieur à zéro.
        """
        if not isinstance(value, int):
            raise ValueError("Le nombre de propositions doit être un entier")
        if value <= 0:            
            raise ValueError("Le nombre de propositions doit être supérieur à 0")
        return value

    def to_dict(self):
        """
        Convertit l'instance Classe en dictionnaire.

        Retourne :
            dict : Dictionnaire contenant les informations
            de la classe (id, professeur_id, nom, dates, jours_horaires,
            contraintes de vœux, code_classe et statut).
        """
        donnees = super().to_dict()
        donnees.update({
            'professeur_id': self.professeur_id,
            'nom': self.nom,
            'couleur': self.couleur,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'jours_horaires': self.jours_horaires,
            'nombre_propositions': self.nombre_propositions,
            'nombre_voeux_requis': self.nombre_voeux_requis,
            'nombre_jours_min': self.nombre_jours_min,
            'code_classe': self.code_classe,
            'statut': self.statut
        })
        return donnees
