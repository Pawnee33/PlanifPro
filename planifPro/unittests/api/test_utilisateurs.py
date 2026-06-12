#!/usr/bin/python3
"""
Tests d'intégration des endpoints de profil utilisateur.

Couvre /utilisateurs/profil (GET / PUT / DELETE), /utilisateurs/parametres
(GET / PUT) et /utilisateurs/aide (GET).
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestUtilisateursAPI(BaseTestCase):

    # ----- Profil -----
    def test_profil_get(self):
        token, payload = self.creer_et_connecter()
        reponse = self.client.get(
            "/api/v1/utilisateurs/profil", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.get_json()["email"], payload["email"])

    def test_profil_get_sans_token(self):
        reponse = self.client.get("/api/v1/utilisateurs/profil")
        self.assertEqual(reponse.status_code, 401)

    def test_profil_put(self):
        token, _ = self.creer_et_connecter()
        reponse = self.client.put(
            "/api/v1/utilisateurs/profil",
            headers=self.entetes_auth(token),
            json={"prenom": "Modifié", "nom": "Nouveau"},
        )
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.get_json()["prenom"], "Modifié")

    def test_profil_put_email_deja_utilise(self):
        _, autre = self.inscrire()
        token, _ = self.creer_et_connecter()
        reponse = self.client.put(
            "/api/v1/utilisateurs/profil",
            headers=self.entetes_auth(token),
            json={"prenom": "X", "nom": "Y", "email": autre["email"]},
        )
        self.assertEqual(reponse.status_code, 409)

    def test_profil_delete(self):
        token, _ = self.creer_et_connecter()
        reponse = self.client.delete(
            "/api/v1/utilisateurs/profil", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)
        # Le compte n'existe plus
        suite = self.client.get(
            "/api/v1/utilisateurs/profil", headers=self.entetes_auth(token)
        )
        self.assertEqual(suite.status_code, 404)

    # ----- Paramètres -----
    def test_parametres_get(self):
        token, _ = self.creer_et_connecter()
        reponse = self.client.get(
            "/api/v1/utilisateurs/parametres", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_parametres_put(self):
        token, _ = self.creer_et_connecter()
        reponse = self.client.put(
            "/api/v1/utilisateurs/parametres",
            headers=self.entetes_auth(token),
            json={"langue": "fr", "theme": "sombre", "notifications": True},
        )
        self.assertEqual(reponse.status_code, 200)

    # ----- Aide -----
    def test_aide_get(self):
        token, _ = self.creer_et_connecter()
        reponse = self.client.get(
            "/api/v1/utilisateurs/aide", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)


if __name__ == "__main__":
    unittest.main()
