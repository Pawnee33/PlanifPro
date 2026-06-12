#!/usr/bin/python3
"""
Tests unitaires du modèle Planning.

Vérifie les règles @validates : statut (valeurs autorisées) et
numero_proposition (entier strictement positif).
"""
import unittest

from planifPro import create_app
from planifPro.backend.classes.planning import Planning


class TestPlanningModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def planning_valide(self, **kwargs):
        donnees = {
            "numero_proposition": 1,
            "statut": "genere",
        }
        donnees.update(kwargs)
        return Planning(**donnees)

    def test_creation_valide(self):
        planning = self.planning_valide()
        self.assertEqual(planning.numero_proposition, 1)
        self.assertEqual(planning.statut, "genere")

    def test_statut_invalide(self):
        with self.assertRaises(ValueError):
            self.planning_valide(statut="autre")

    def test_statuts_valides(self):
        for statut in ["genere", "selectionne", "modifie", "valide"]:
            self.assertEqual(self.planning_valide(statut=statut).statut, statut)

    def test_numero_proposition_non_positif(self):
        with self.assertRaises(ValueError):
            self.planning_valide(numero_proposition=0)

    def test_numero_proposition_non_entier(self):
        with self.assertRaises(ValueError):
            self.planning_valide(numero_proposition="1")


if __name__ == "__main__":
    unittest.main()
