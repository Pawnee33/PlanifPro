#!/usr/bin/python3
"""
Tests d'intégration des endpoints de notifications.

Couvre le cas vide (404 quand l'utilisateur n'a aucune notification),
l'écriture effective en BDD via les flux câblés (collecte des vœux →
notif élève, soumission de vœux → notif prof), l'enregistrement du
token FCM (200 / 400) et les chemins introuvables.
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

    # ----- Écriture effective en BDD via les flux câblés -----
    def test_collecte_cree_notification_eleve(self):
        # Lancer la collecte doit déposer une notif 'collecte_voeux' à l'élève
        _, _, _, token_eleve = self.preparer_classe_pour_voeux()
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token_eleve))
        self.assertEqual(reponse.status_code, 200)
        notifs = reponse.get_json()
        self.assertTrue(any(n["type"] == "collecte_voeux" for n in notifs))

    def test_soumission_voeux_cree_notification_prof(self):
        # Soumettre des vœux doit déposer une notif 'voeux_soumis' au prof
        token_prof, classe, _, token_eleve = self.preparer_classe_pour_voeux()
        self.soumettre_voeux(token_eleve, classe["id"])
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token_prof))
        self.assertEqual(reponse.status_code, 200)
        notifs = reponse.get_json()
        self.assertTrue(any(n["type"] == "voeux_soumis" for n in notifs))


if __name__ == "__main__":
    unittest.main()
