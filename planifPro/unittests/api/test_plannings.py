#!/usr/bin/python3
"""
Tests d'intégration des endpoints de planning.

Couvre la génération des propositions (200 / 403 / 404) et la validation
d'une proposition (200 / 404 / 409). On n'asserte pas le placement réel
des créneaux (dépendant de l'algorithme), seulement les codes de retour.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestPlanningsAPI(BaseTestCase):

    def test_generer(self):
        token_prof, classe, _, _ = self.preparer_classe_avec_voeux()
        reponse = self.generer_plannings(token_prof, classe["id"])
        self.assertEqual(reponse.status_code, 200)

    def test_generer_eleve_refuse(self):
        token_eleve, _ = self.creer_et_connecter("eleve")
        reponse = self.client.post(
            "/api/v1/plannings/generer",
            headers=self.entetes_auth(token_eleve),
            json={"classe_id": self.FAKE_UUID},
        )
        self.assertEqual(reponse.status_code, 403)

    def test_generer_classe_introuvable(self):
        token_prof, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            "/api/v1/plannings/generer",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": self.FAKE_UUID},
        )
        self.assertEqual(reponse.status_code, 404)

    def test_valider(self):
        token_prof, classe, _, _ = self.preparer_classe_avec_voeux()
        plannings = self.generer_plannings(token_prof, classe["id"]).get_json()
        reponse = self.client.put(
            "/api/v1/plannings/valider",
            headers=self.entetes_auth(token_prof),
            json={"planning_id": plannings[0]["id"]},
        )
        self.assertEqual(reponse.status_code, 200)

    def test_valider_planning_introuvable(self):
        token_prof, _, _, _ = self.preparer_classe_avec_voeux()
        reponse = self.client.put(
            "/api/v1/plannings/valider",
            headers=self.entetes_auth(token_prof),
            json={"planning_id": self.FAKE_UUID},
        )
        self.assertEqual(reponse.status_code, 404)

    def test_valider_deja_valide(self):
        token_prof, classe, _, _ = self.preparer_classe_avec_voeux()
        plannings = self.generer_plannings(token_prof, classe["id"]).get_json()
        # Première validation
        self.client.put(
            "/api/v1/plannings/valider",
            headers=self.entetes_auth(token_prof),
            json={"planning_id": plannings[0]["id"]},
        )
        # Revalider le même planning (déjà validé pour cette classe) -> 409
        reponse = self.client.put(
            "/api/v1/plannings/valider",
            headers=self.entetes_auth(token_prof),
            json={"planning_id": plannings[0]["id"]},
        )
        self.assertEqual(reponse.status_code, 409)

    def test_generer_deja_genere(self):
        token_prof, classe, _, _ = self.preparer_classe_avec_voeux()
        self.generer_plannings(token_prof, classe["id"])
        reponse = self.generer_plannings(token_prof, classe["id"])
        self.assertEqual(reponse.status_code, 409)

    # ----- Consultation -----
    def test_global_prof_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(
            "/api/v1/plannings/global", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_global_eleve_vide(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.get(
            "/api/v1/plannings/global", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_detail_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(
            f"/api/v1/plannings/{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_creneaux_planning_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(
            f"/api/v1/plannings/{self.FAKE_UUID}/creneaux",
            headers=self.entetes_auth(token),
        )
        self.assertEqual(reponse.status_code, 404)

    def test_confirmation_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.put(
            f"/api/v1/plannings/{self.FAKE_UUID}/confirmation",
            headers=self.entetes_auth(token),
            json={"confirmation": True},
        )
        self.assertEqual(reponse.status_code, 403)

    def test_confirmation_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"/api/v1/plannings/{self.FAKE_UUID}/confirmation",
            headers=self.entetes_auth(token),
            json={"confirmation": True},
        )
        self.assertEqual(reponse.status_code, 404)


if __name__ == "__main__":
    unittest.main()
