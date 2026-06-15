#!/usr/bin/python3
"""
Tests d'intégration des endpoints d'authentification.

Couvre l'inscription (201 / 400 / 409), la connexion (200 / 401)
et l'accès à une route protégée par JWT (200 / 401).
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestAuthentificationAPI(BaseTestCase):

    # ----- Inscription -----
    def test_inscription_professeur_valide(self):
        reponse, _ = self.inscrire(role="professeur")
        self.assertEqual(reponse.status_code, 201)
        self.assertIn("id", reponse.get_json())

    def test_inscription_eleve_valide(self):
        reponse, _ = self.inscrire(role="eleve")
        self.assertEqual(reponse.status_code, 201)

    def test_inscription_champ_manquant(self):
        payload = self.payload_inscription()
        payload.pop("email")
        reponse = self.client.post(
            "/api/v1/authentification/inscription", json=payload
        )
        self.assertEqual(reponse.status_code, 400)

    def test_inscription_email_invalide(self):
        reponse, _ = self.inscrire(email="email-invalide")
        self.assertEqual(reponse.status_code, 400)

    def test_inscription_email_deja_utilise(self):
        self.inscrire(email="doublon@planifpro.com")
        reponse = self.client.post(
            "/api/v1/authentification/inscription",
            json=self.payload_inscription(email="doublon@planifpro.com"),
        )
        self.assertEqual(reponse.status_code, 409)

    # ----- Connexion -----
    def test_connexion_valide(self):
        _, payload = self.inscrire()
        reponse = self.client.post(
            "/api/v1/authentification/connexion",
            json={"email": payload["email"],
                  "mot_de_passe": payload["mot_de_passe"]},
        )
        self.assertEqual(reponse.status_code, 200)
        self.assertIn("access_token", reponse.get_json())

    def test_connexion_mauvais_mot_de_passe(self):
        _, payload = self.inscrire()
        reponse = self.client.post(
            "/api/v1/authentification/connexion",
            json={"email": payload["email"], "mot_de_passe": "mauvais"},
        )
        self.assertEqual(reponse.status_code, 401)

    def test_connexion_email_inconnu(self):
        reponse = self.client.post(
            "/api/v1/authentification/connexion",
            json={"email": "inconnu@planifpro.com",
                  "mot_de_passe": "motdepasse123"},
        )
        self.assertEqual(reponse.status_code, 401)

    # ----- Route protégée -----
    def test_protected_sans_token(self):
        reponse = self.client.get("/api/v1/authentification/protected")
        self.assertEqual(reponse.status_code, 401)

    def test_protected_avec_token(self):
        token, _ = self.creer_et_connecter(role="professeur")
        reponse = self.client.get(
            "/api/v1/authentification/protected",
            headers=self.entetes_auth(token),
        )
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.get_json()["role"], "professeur")


if __name__ == "__main__":
    unittest.main()
