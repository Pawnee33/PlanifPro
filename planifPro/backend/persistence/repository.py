"""
Module de persistance.

Ce module définit les classes Repository et SQLAlchemyRepository
qui gèrent l'accès à la base de données pour tous les modèles.
"""

from abc import ABC, abstractmethod
from planifPro import db


class Repository(ABC):
    """
    Classe abstraite définissant le contrat pour tous les repositories.
    Toute classe héritant de Repository doit implémenter ces méthodes.
    """
    @abstractmethod
    def ajouter(self, obj):
        pass

    @abstractmethod
    def obtenir(self, obj_id):
        pass

    @abstractmethod
    def tout_obtenir(self):
        pass

    @abstractmethod
    def mis_a_jour(self, obj_id, data):
        pass

    @abstractmethod
    def supprime(self, obj_id):
        pass

    @abstractmethod
    def obtenir_par_attribut(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    """
    Implémentation du repository avec SQLAlchemy.
    Fournit les opérations CRUD de base pour tous les modèles.
    """
    def __init__(self, model):
        self.model = model

    def ajouter(self, obj):
        """Ajoute un objet en base de données."""
        db.session.add(obj)
        db.session.commit()

    def obtenir(self, obj_id):
        """Récupère un objet par son identifiant."""
        return db.session.get(self.model, obj_id)

    def tout_obtenir(self):
        """Récupère tous les objets du modèle."""
        return self.model.query.all()

    def mis_a_jour(self, obj_id, data):
        """Met à jour les attributs d'un objet par son identifiant."""
        obj = self.obtenir(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def supprime(self, obj_id):
        """Supprime un objet par son identifiant."""
        obj = self.obtenir(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def obtenir_par_attribut(self, attr_name, attr_value):
        """Récupère un objet par la valeur d'un de ses attributs."""
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
            ).first()
