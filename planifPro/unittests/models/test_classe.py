#!/usr/bin/python3
"""
Tests unitaires du modèle Classe.

Vérifie les règles @validates : nom, dates (objet date, fin après début),
jours_horaires (dict non vide), statut (valeurs autorisées), code_classe
(8 caractères) et les compteurs entiers strictement positifs.
"""
import unittest
from datetime import date

from planifPro import create_app
from planifPro.backend.classes.classe import Classe


class TestClasseModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def classe_valide(self, **kwargs):
        donnees = {
            "nom": "Conservatoire",
            "date_debut": date(2026, 9, 1),
            "date_fin": date(2027, 6, 30),
            "jours_horaires": {"lundi": ["09:00-12:00"]},
            "statut": "classe_active",
            "nombre_voeux_requis": 3,
            "nombre_jours_min": 2,
            "code_classe": "ABCD1234",
            "nombre_propositions": 3,
        }
        donnees.update(kwargs)
        return Classe(**donnees)

    def test_creation_valide(self):
        classe = self.classe_valide()
        self.assertEqual(classe.nom, "Conservatoire")
        self.assertEqual(classe.statut, "classe_active")

    def test_nom_obligatoire(self):
        with self.assertRaises(ValueError):
            self.classe_valide(nom="")

    def test_nom_trop_long(self):
        with self.assertRaises(ValueError):
            self.classe_valide(nom="A" * 51)

    def test_date_debut_non_date(self):
        with self.assertRaises(ValueError):
            self.classe_valide(date_debut="2026-09-01")

    def test_date_fin_avant_debut(self):
        with self.assertRaises(ValueError):
            self.classe_valide(date_fin=date(2026, 8, 1))

    def test_jours_horaires_vide(self):
        with self.assertRaises(ValueError):
            self.classe_valide(jours_horaires={})

    def test_jours_horaires_non_dict(self):
        with self.assertRaises(ValueError):
            self.classe_valide(jours_horaires="lundi")

    def test_statut_invalide(self):
        with self.assertRaises(ValueError):
            self.classe_valide(statut="autre")

    def test_statuts_valides(self):
        for statut in ["classe_active", "collecte_active",
                       "planning_genere", "planning_termine"]:
            self.assertEqual(self.classe_valide(statut=statut).statut, statut)

    def test_nombre_voeux_requis_non_positif(self):
        with self.assertRaises(ValueError):
            self.classe_valide(nombre_voeux_requis=0)

    def test_nombre_jours_min_non_positif(self):
        with self.assertRaises(ValueError):
            self.classe_valide(nombre_jours_min=0)

    def test_nombre_propositions_non_positif(self):
        with self.assertRaises(ValueError):
            self.classe_valide(nombre_propositions=0)

    def test_code_classe_mauvaise_longueur(self):
        with self.assertRaises(ValueError):
            self.classe_valide(code_classe="ABC")


if __name__ == "__main__":
    unittest.main()
