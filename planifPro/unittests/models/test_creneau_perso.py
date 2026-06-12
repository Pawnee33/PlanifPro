#!/usr/bin/python3
"""
Tests unitaires du modèle CreneauPerso.

Vérifie les règles @validates : titre (non vide, max 100 caractères)
et heures (objet time, fin après début).
"""
import unittest
from datetime import time

from planifPro import create_app
from planifPro.backend.classes.creneau_perso import CreneauPerso


class TestCreneauPersoModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def creneau_perso_valide(self, **kwargs):
        donnees = {
            "titre": "Rendez-vous médecin",
            "jour": "mardi",
            "heure_debut": time(14, 0),
            "heure_fin": time(15, 0),
        }
        donnees.update(kwargs)
        return CreneauPerso(**donnees)

    def test_creation_valide(self):
        creneau = self.creneau_perso_valide()
        self.assertEqual(creneau.titre, "Rendez-vous médecin")

    def test_titre_vide(self):
        with self.assertRaises(ValueError):
            self.creneau_perso_valide(titre="")

    def test_titre_trop_long(self):
        with self.assertRaises(ValueError):
            self.creneau_perso_valide(titre="A" * 101)

    def test_titre_borne_valide(self):
        creneau = self.creneau_perso_valide(titre="A" * 100)
        self.assertEqual(len(creneau.titre), 100)

    def test_heure_debut_non_time(self):
        with self.assertRaises(ValueError):
            self.creneau_perso_valide(heure_debut="14:00")

    def test_heure_fin_avant_debut(self):
        with self.assertRaises(ValueError):
            self.creneau_perso_valide(heure_fin=time(13, 0))


if __name__ == "__main__":
    unittest.main()
