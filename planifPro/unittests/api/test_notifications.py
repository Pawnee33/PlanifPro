#!/usr/bin/python3
"""
Tests d'intégration des endpoints de notifications.

Aucune notification n'étant écrite en BDD dans les flux actuels, les GET
renvoient 404. On teste aussi l'enregistrement du token FCM (200 / 400)
et les chemins introuvables.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestNotificationsAPI(BaseTestCase):

    URL = "/api/v1/notifications/"

    def test_lister_vide_prof(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
        self.assertEqual(reponse.status_code, 404)

    def test_lister_vide_eleve(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
        self.assertEqual(reponse.status_code, 404)

    def test_lire_aucune(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}lire", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_token_professeur(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            f"{self.URL}token",
            headers=self.entetes_auth(token),
            json={"token_fcm": "jeton-fcm-de-test"},
        )
        self.assertEqual(reponse.status_code, 200)

    def test_token_eleve(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.post(
            f"{self.URL}token",
            headers=self.entetes_auth(token),
            json={"token_fcm": "jeton-fcm-de-test"},
        )
        self.assertEqual(reponse.status_code, 200)

    def test_token_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            f"{self.URL}token",
            headers=self.entetes_auth(token),
            json={"token_fcm": ""},
        )
        self.assertEqual(reponse.status_code, 400)

    def test_marquer_lue_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_supprimer_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.delete(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)


if __name__ == "__main__":
    unittest.main()
