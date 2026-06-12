#!/usr/bin/python3
"""
Tests unitaires du modèle Voeu.

Vérifie les règles @validates : statut (valeurs autorisées) et
creneaux_souhaites (dictionnaire non vide).
"""
import unittest

from planifPro import create_app
from planifPro.backend.classes.voeu import Voeu


class TestVoeuModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def voeu_valide(self, **kwargs):
        donnees = {
            "statut": "en_attente",
            "creneaux_souhaites": {"lundi": ["09:00"]},
        }
        donnees.update(kwargs)
        return Voeu(**donnees)

    def test_creation_valide(self):
        voeu = self.voeu_valide()
        self.assertEqual(voeu.statut, "en_attente")

    def test_statut_invalide(self):
        with self.assertRaises(ValueError):
            self.voeu_valide(statut="autre")

    def test_statuts_valides(self):
        for statut in ["en_attente", "soumis", "valide"]:
            self.assertEqual(self.voeu_valide(statut=statut).statut, statut)

    def test_creneaux_souhaites_vide(self):
        with self.assertRaises(ValueError):
            self.voeu_valide(creneaux_souhaites={})

    def test_creneaux_souhaites_non_dict(self):
        with self.assertRaises(ValueError):
            self.voeu_valide(creneaux_souhaites="lundi")


if __name__ == "__main__":
    unittest.main()
