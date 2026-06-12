#!/usr/bin/python3
"""
Tests unitaires du modèle Professeur.

Professeur hérite d'Utilisateur : on vérifie qu'il reprend bien les
validations héritées (email) et que to_dict expose utilisateur_id.
"""
import unittest

from planifPro import create_app
from planifPro.backend.classes.professeur import Professeur


class TestProfesseurModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def professeur_valide(self, **kwargs):
        donnees = {
            "prenom": "Marie",
            "nom": "Curie",
            "email": "marie@planifpro.com",
            "role": "professeur",
        }
        donnees.update(kwargs)
        return Professeur(**donnees)

    def test_creation_valide(self):
        professeur = self.professeur_valide()
        self.assertEqual(professeur.prenom, "Marie")
        self.assertEqual(professeur.role, "professeur")

    def test_email_invalide_herite(self):
        with self.assertRaises(ValueError):
            self.professeur_valide(email="email-invalide")

    def test_to_dict_contient_utilisateur_id(self):
        professeur = self.professeur_valide()
        self.assertIn("utilisateur_id", professeur.to_dict())


if __name__ == "__main__":
    unittest.main()
