#!/usr/bin/python3
"""
Tests unitaires du modèle Evenement.

Vérifie les règles @validates : titre (non vide, max 50 caractères),
description (chaîne), date_heure (objet datetime) et destinataires
(dictionnaire non vide).
"""
import unittest
from datetime import datetime

from planifPro import create_app
from planifPro.backend.classes.evenement import Evenement


class TestEvenementModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def evenement_valide(self, **kwargs):
        donnees = {
            "titre": "Audition de fin d'année",
            "description": "Audition au conservatoire",
            "date_heure": datetime(2026, 6, 28, 18, 0),
            "destinataires": {"type": "toutes_classes"},
        }
        donnees.update(kwargs)
        return Evenement(**donnees)

    def test_creation_valide(self):
        evenement = self.evenement_valide()
        self.assertEqual(evenement.titre, "Audition de fin d'année")

    def test_titre_vide(self):
        with self.assertRaises(ValueError):
            self.evenement_valide(titre="")

    def test_titre_trop_long(self):
        with self.assertRaises(ValueError):
            self.evenement_valide(titre="A" * 51)

    def test_description_non_string(self):
        with self.assertRaises(ValueError):
            self.evenement_valide(description=123)

    def test_date_heure_non_datetime(self):
        with self.assertRaises(ValueError):
            self.evenement_valide(date_heure="2026-06-28T18:00:00")

    def test_destinataires_vide(self):
        with self.assertRaises(ValueError):
            self.evenement_valide(destinataires={})

    def test_destinataires_non_dict(self):
        with self.assertRaises(ValueError):
            self.evenement_valide(destinataires="tous")


if __name__ == "__main__":
    unittest.main()
