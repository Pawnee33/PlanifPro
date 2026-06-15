#!/usr/bin/python3
"""
Tests unitaires du modèle Eleve.

Eleve hérite d'Utilisateur : on vérifie qu'il reprend bien les
validations héritées (email) et que to_dict expose utilisateur_id.
"""
import unittest

from planifPro import create_app
from planifPro.backend.classes.eleve import Eleve


class TestEleveModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def eleve_valide(self, **kwargs):
        donnees = {
            "prenom": "Lucas",
            "nom": "Bernard",
            "email": "lucas@planifpro.com",
            "role": "eleve",
        }
        donnees.update(kwargs)
        return Eleve(**donnees)

    def test_creation_valide(self):
        eleve = self.eleve_valide()
        self.assertEqual(eleve.prenom, "Lucas")
        self.assertEqual(eleve.role, "eleve")

    def test_email_invalide_herite(self):
        with self.assertRaises(ValueError):
            self.eleve_valide(email="email-invalide")

    def test_to_dict_contient_utilisateur_id(self):
        eleve = self.eleve_valide()
        self.assertIn("utilisateur_id", eleve.to_dict())


if __name__ == "__main__":
    unittest.main()
