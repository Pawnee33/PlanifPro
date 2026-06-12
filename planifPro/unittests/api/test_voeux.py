#!/usr/bin/python3
"""
Tests d'intégration des endpoints de vœux.

Couvre la soumission (201 / 400 / 403 / 409), la liste, le statut par classe
(200 / 403) et la relance des élèves (200 / 404).
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestVoeuxAPI(BaseTestCase):

    def test_soumettre_voeux(self):
        _, classe, _, token_eleve = self.preparer_classe_pour_voeux()
        reponse = self.soumettre_voeux(token_eleve, classe["id"])
        self.assertEqual(reponse.status_code, 201)

    def test_soumettre_voeux_insuffisants(self):
        _, classe, _, token_eleve = self.preparer_classe_pour_voeux()
        # Une seule entrée sur un seul jour : sous les seuils (3 vœux / 2 jours)
        reponse = self.soumettre_voeux(
            token_eleve, classe["id"],
            creneaux={"1": {"jour": "lundi", "heure": "09:00"}},
        )
        self.assertEqual(reponse.status_code, 400)

    def test_soumettre_voeux_prof_refuse(self):
        token_prof, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            "/api/v1/voeux/",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": self.FAKE_UUID, "creneaux_souhaites": self.payload_voeux()},
        )
        self.assertEqual(reponse.status_code, 403)

    def test_soumettre_voeux_planning_deja_valide(self):
        token_prof, classe, _, token_eleve = self.preparer_classe_avec_voeux()
        self.generer_et_valider(token_prof, classe["id"])
        reponse = self.soumettre_voeux(token_eleve, classe["id"])
        self.assertEqual(reponse.status_code, 409)

    def test_lister_voeux_eleve(self):
        _, classe, _, token_eleve = self.preparer_classe_avec_voeux()
        reponse = self.client.get(
            "/api/v1/voeux/", headers=self.entetes_auth(token_eleve)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_statut_voeux(self):
        token_prof, classe, _, _ = self.preparer_classe_avec_voeux()
        reponse = self.client.get(
            f"/api/v1/voeux/statut/{classe['id']}",
            headers=self.entetes_auth(token_prof),
        )
        self.assertEqual(reponse.status_code, 200)

    def test_statut_voeux_eleve_refuse(self):
        token_eleve, _ = self.creer_et_connecter("eleve")
        reponse = self.client.get(
            f"/api/v1/voeux/statut/{self.FAKE_UUID}",
            headers=self.entetes_auth(token_eleve),
        )
        self.assertEqual(reponse.status_code, 403)

    def test_relancer(self):
        token_prof, classe, eleve_id, _ = self.preparer_classe_pour_voeux()
        reponse = self.client.post(
            "/api/v1/voeux/relancer",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": classe["id"], "eleve_ids": [eleve_id]},
        )
        self.assertEqual(reponse.status_code, 200)

    def test_relancer_classe_introuvable(self):
        token_prof, _, eleve_id, _ = self.preparer_classe_pour_voeux()
        reponse = self.client.post(
            "/api/v1/voeux/relancer",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": self.FAKE_UUID, "eleve_ids": [eleve_id]},
        )
        self.assertEqual(reponse.status_code, 404)


if __name__ == "__main__":
    unittest.main()
