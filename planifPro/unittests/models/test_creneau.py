#!/usr/bin/python3
"""
Tests unitaires du modèle Creneau.

Vérifie les règles @validates : type et jour non vides, heures (objet time,
fin après début), dates optionnelles (objet date, fin après début),
duree_minutes (entier positif) et statut (valeurs autorisées).
"""
import unittest
from datetime import date, time

from planifPro import create_app
from planifPro.backend.classes.creneau import Creneau


class TestCreneauModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def creneau_valide(self, **kwargs):
        donnees = {
            "type": "conservatoire",
            "jour": "lundi",
            "heure_debut": time(9, 0),
            "heure_fin": time(10, 0),
            "duree_minutes": 60,
            "statut": "en_attente",
        }
        donnees.update(kwargs)
        return Creneau(**donnees)

    def test_creation_valide(self):
        creneau = self.creneau_valide()
        self.assertEqual(creneau.jour, "lundi")
        self.assertEqual(creneau.statut, "en_attente")

    def test_type_vide(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(type="")

    def test_jour_vide(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(jour="")

    def test_heure_debut_non_time(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(heure_debut="09:00")

    def test_heure_fin_avant_debut(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(heure_fin=time(8, 0))

    def test_duree_minutes_non_positif(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(duree_minutes=0)

    def test_duree_minutes_non_entier(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(duree_minutes="60")

    def test_statut_invalide(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(statut="autre")

    def test_statuts_valides(self):
        for statut in ["en_attente", "confirme", "valide", "annule"]:
            self.assertEqual(self.creneau_valide(statut=statut).statut, statut)

    def test_date_debut_none_acceptee(self):
        creneau = self.creneau_valide(date_debut=None)
        self.assertIsNone(creneau.date_debut)

    def test_date_fin_avant_debut(self):
        with self.assertRaises(ValueError):
            self.creneau_valide(date_debut=date(2026, 9, 1),
                                date_fin=date(2026, 8, 1))


if __name__ == "__main__":
    unittest.main()
