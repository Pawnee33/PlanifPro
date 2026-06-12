#!/usr/bin/python3
"""
Tests unitaires du modèle Objectif.

Vérifie les règles @validates : contenu et conseils doivent être des
chaînes de caractères.
"""
import unittest

from planifPro import create_app
from planifPro.backend.classes.objectif import Objectif


class TestObjectifModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def objectif_valide(self, **kwargs):
        donnees = {
            "contenu": "Travailler la gamme de Do majeur",
            "conseils": "Lentement au métronome",
        }
        donnees.update(kwargs)
        return Objectif(**donnees)

    def test_creation_valide(self):
        objectif = self.objectif_valide()
        self.assertEqual(objectif.contenu, "Travailler la gamme de Do majeur")

    def test_contenu_non_string(self):
        with self.assertRaises(ValueError):
            self.objectif_valide(contenu=123)

    def test_conseils_non_string(self):
        with self.assertRaises(ValueError):
            self.objectif_valide(conseils=123)


if __name__ == "__main__":
    unittest.main()
