#!/usr/bin/python3
"""
Tests d'intégration des endpoints de créneaux personnels.

Couvre la création (201 / 400), la liste (200 / 404), le détail, la
modification, le déplacement, la suppression (200 / 404) et l'import
Google sans token (400).
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestCreneauxPersoAPI(BaseTestCase):

    URL = "/api/v1/creneaux/perso/"

    def _creer(self, token, **kwargs):
        """Crée un créneau personnel. Renvoie la réponse."""
        donnees = {
            "titre": "Cours perso",
            "jour": "lundi",
            "heure_debut": "09:00",
            "heure_fin": "10:00",
        }
        donnees.update(kwargs)
        return self.client.post(
            self.URL, headers=self.entetes_auth(token), json=donnees
        )

    def test_creer(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self._creer(token)
        self.assertEqual(reponse.status_code, 201)

    def test_creer_titre_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self._creer(token, titre="")
        self.assertEqual(reponse.status_code, 400)

    def test_lister(self):
        token, _ = self.creer_et_connecter("professeur")
        self._creer(token)
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
        self.assertEqual(reponse.status_code, 200)

    def test_lister_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
        self.assertEqual(reponse.status_code, 404)

    def test_detail(self):
        token, _ = self.creer_et_connecter("professeur")
        creneau = self._creer(token).get_json()
        reponse = self.client.get(
            f"{self.URL}{creneau['id']}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_detail_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_modifier(self):
        token, _ = self.creer_et_connecter("professeur")
        creneau = self._creer(token).get_json()
        reponse = self.client.put(
            f"{self.URL}{creneau['id']}",
            headers=self.entetes_auth(token),
            json={
                "titre": "Cours modifié",
                "jour": "mardi",
                "heure_debut": "14:00",
                "heure_fin": "15:00",
            },
        )
        self.assertEqual(reponse.status_code, 200)

    def test_modifier_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}",
            headers=self.entetes_auth(token),
            json={
                "titre": "X",
                "jour": "mardi",
                "heure_debut": "14:00",
                "heure_fin": "15:00",
            },
        )
        self.assertEqual(reponse.status_code, 404)

    def test_deplacer(self):
        token, _ = self.creer_et_connecter("professeur")
        creneau = self._creer(token).get_json()
        reponse = self.client.put(
            f"{self.URL}{creneau['id']}/deplacer",
            headers=self.entetes_auth(token),
            json={"jour": "mercredi", "heure_debut": "11:00", "heure_fin": "12:00"},
        )
        self.assertEqual(reponse.status_code, 200)

    def test_deplacer_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}/deplacer",
            headers=self.entetes_auth(token),
            json={"jour": "mercredi", "heure_debut": "11:00", "heure_fin": "12:00"},
        )
        self.assertEqual(reponse.status_code, 404)

    def test_supprimer(self):
        token, _ = self.creer_et_connecter("professeur")
        creneau = self._creer(token).get_json()
        reponse = self.client.delete(
            f"{self.URL}{creneau['id']}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_supprimer_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.delete(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_import_sans_token_google(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            f"{self.URL}import", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 400)


if __name__ == "__main__":
    unittest.main()
