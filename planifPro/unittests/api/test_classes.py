#!/usr/bin/python3
"""
Tests d'intégration des endpoints de classes.

Couvre la création (201 / 403), la lecture (200 / 403), la modification,
la suppression, la collecte, l'inscription d'un élève via code (rejoindre),
la liste des élèves et les chemins d'erreur de l'invitation.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestClassesAPI(BaseTestCase):

    # ----- Création -----
    def test_creer_classe(self):
        token, _ = self.creer_et_connecter(role="professeur")
        reponse = self.client.post(
            "/api/v1/classes/",
            headers=self.entetes_auth(token),
            json=self.payload_classe(),
        )
        self.assertEqual(reponse.status_code, 201)
        self.assertIn("code_classe", reponse.get_json())

    def test_creer_classe_eleve_refuse(self):
        token, _ = self.creer_et_connecter(role="eleve")
        reponse = self.client.post(
            "/api/v1/classes/",
            headers=self.entetes_auth(token),
            json=self.payload_classe(),
        )
        self.assertEqual(reponse.status_code, 403)

    # ----- Lecture -----
    def test_lister_classes(self):
        token, _ = self.creer_et_connecter(role="professeur")
        self.creer_classe(token)
        reponse = self.client.get(
            "/api/v1/classes/", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_detail_classe(self):
        token, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token)
        reponse = self.client.get(
            f"/api/v1/classes/{classe['id']}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_detail_classe_eleve_refuse(self):
        token_prof, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token_prof)
        token_eleve, _ = self.creer_et_connecter(role="eleve")
        reponse = self.client.get(
            f"/api/v1/classes/{classe['id']}",
            headers=self.entetes_auth(token_eleve),
        )
        self.assertEqual(reponse.status_code, 403)

    # ----- Modification / suppression -----
    def test_modifier_classe(self):
        token, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token)
        reponse = self.client.put(
            f"/api/v1/classes/{classe['id']}",
            headers=self.entetes_auth(token),
            json={"nom": "Cours Privé"},
        )
        self.assertEqual(reponse.status_code, 200)

    def test_supprimer_classe(self):
        token, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token)
        reponse = self.client.delete(
            f"/api/v1/classes/{classe['id']}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 200)

    # ----- Collecte -----
    def test_lancer_collecte(self):
        token, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token)
        reponse = self.client.post(
            f"/api/v1/classes/{classe['id']}/collecte",
            headers=self.entetes_auth(token),
        )
        self.assertEqual(reponse.status_code, 200)

    # ----- Rejoindre (élève) -----
    def test_rejoindre_classe(self):
        token_prof, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token_prof)
        token_eleve, _ = self.creer_et_connecter(role="eleve")
        reponse = self.rejoindre_classe(token_eleve, classe["code_classe"])
        self.assertEqual(reponse.status_code, 201)

    def test_rejoindre_classe_deja_inscrit(self):
        token_prof, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token_prof)
        token_eleve, _ = self.creer_et_connecter(role="eleve")
        self.rejoindre_classe(token_eleve, classe["code_classe"])
        reponse = self.rejoindre_classe(token_eleve, classe["code_classe"])
        self.assertEqual(reponse.status_code, 409)

    def test_rejoindre_code_inconnu(self):
        token_eleve, _ = self.creer_et_connecter(role="eleve")
        reponse = self.rejoindre_classe(token_eleve, "INCONNU0")
        self.assertEqual(reponse.status_code, 404)

    # ----- Élèves d'une classe -----
    def test_eleves_classe_vide(self):
        token, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token)
        reponse = self.client.get(
            f"/api/v1/classes/{classe['id']}/eleves",
            headers=self.entetes_auth(token),
        )
        self.assertEqual(reponse.status_code, 404)

    def test_eleves_classe_apres_rejoindre(self):
        token_prof, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token_prof)
        token_eleve, _ = self.creer_et_connecter(role="eleve")
        self.rejoindre_classe(token_eleve, classe["code_classe"])
        reponse = self.client.get(
            f"/api/v1/classes/{classe['id']}/eleves",
            headers=self.entetes_auth(token_prof),
        )
        self.assertEqual(reponse.status_code, 200)

    # ----- Invitation (chemins d'erreur, sans envoi réel) -----
    def test_inviter_email_invalide(self):
        token, _ = self.creer_et_connecter(role="professeur")
        classe = self.creer_classe(token)
        reponse = self.client.post(
            f"/api/v1/classes/{classe['id']}/inviter",
            headers=self.entetes_auth(token),
            json={"email": "pasunemail"},
        )
        self.assertEqual(reponse.status_code, 400)

    def test_inviter_classe_introuvable(self):
        token, _ = self.creer_et_connecter(role="professeur")
        reponse = self.client.post(
            f"/api/v1/classes/{self.FAKE_UUID}/inviter",
            headers=self.entetes_auth(token),
            json={"email": "x@y.com"},
        )
        self.assertEqual(reponse.status_code, 404)


if __name__ == "__main__":
    unittest.main()
