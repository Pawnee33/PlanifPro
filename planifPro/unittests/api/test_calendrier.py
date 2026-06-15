#!/usr/bin/python3
"""
Tests d'intégration des endpoints de calendrier Google.

Le flux OAuth complet n'est pas testable sans un vrai compte Google ;
on couvre les gardes fiables : protection JWT et validations d'entrée
de l'export.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestCalendrierAPI(BaseTestCase):

    def test_auth_sans_token(self):
        reponse = self.client.get("/api/v1/calendrier/auth")
        self.assertEqual(reponse.status_code, 401)

    def test_export_sans_creneaux(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            "/api/v1/calendrier/export",
            headers=self.entetes_auth(token),
            json={"creneau_ids": []},
        )
        self.assertEqual(reponse.status_code, 400)

    def test_export_sans_token_google(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            "/api/v1/calendrier/export",
            headers=self.entetes_auth(token),
            json={"creneau_ids": [self.FAKE_UUID]},
        )
        self.assertEqual(reponse.status_code, 401)


if __name__ == "__main__":
    unittest.main()
