#!/usr/bin/python3
"""
Tests d'intégration des endpoints de créneaux.

On teste les gardes fiables (rôle 403, introuvable 404, scope invalide 400)
en fixtures minimales. La création/modification réelle d'un créneau dépend
d'un planning validé avec créneaux placés (fragile) et n'est pas couverte ici.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestCreneauxAPI(BaseTestCase):

    URL = "/api/v1/creneaux/"

    def _payload_creneau(self):
        return {
            "planning_id": self.FAKE_UUID,
            "eleve_id": self.FAKE_UUID,
            "classe_id": self.FAKE_UUID,
            "type": "Piano",
            "jour": "lundi",
            "heure_debut": "09:00",
            "heure_fin": "10:00",
            "duree_minutes": 60,
        }

    def test_lister_prof_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
        self.assertEqual(reponse.status_code, 404)

    def test_lister_eleve_vide(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
        self.assertEqual(reponse.status_code, 404)

    def test_creer_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.post(
            self.URL, headers=self.entetes_auth(token), json=self._payload_creneau()
        )
        self.assertEqual(reponse.status_code, 403)

    def test_creer_planning_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            self.URL, headers=self.entetes_auth(token), json=self._payload_creneau()
        )
        self.assertEqual(reponse.status_code, 404)

    def test_echanger_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.put(
            f"{self.URL}echanger",
            headers=self.entetes_auth(token),
            json={"creneau_id_1": self.FAKE_UUID, "creneau_id_2": self.FAKE_UUID},
        )
        self.assertEqual(reponse.status_code, 403)

    def test_echanger_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}echanger",
            headers=self.entetes_auth(token),
            json={"creneau_id_1": self.FAKE_UUID, "creneau_id_2": self.FAKE_UUID},
        )
        self.assertEqual(reponse.status_code, 404)

    def test_detail_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_modifier_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}",
            headers=self.entetes_auth(token),
            json={"jour": "mardi"},
        )
        self.assertEqual(reponse.status_code, 403)

    def test_modifier_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}",
            headers=self.entetes_auth(token),
            json={"jour": "mardi"},
        )
        self.assertEqual(reponse.status_code, 404)

    def test_supprimer_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.delete(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 403)

    def test_supprimer_scope_invalide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.delete(
            f"{self.URL}{self.FAKE_UUID}?scope=bidon",
            headers=self.entetes_auth(token),
        )
        self.assertEqual(reponse.status_code, 400)

    def test_supprimer_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.delete(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_confirmer_prof_refuse(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}/confirmer", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 403)

    def test_confirmer_introuvable(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}/confirmer", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_deplacer_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}/deplacer",
            headers=self.entetes_auth(token),
            json={"jour": "mardi", "heure_debut": "09:00", "heure_fin": "10:00"},
        )
        self.assertEqual(reponse.status_code, 403)

    def test_deplacer_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}/deplacer",
            headers=self.entetes_auth(token),
            json={"jour": "mardi", "heure_debut": "09:00", "heure_fin": "10:00"},
        )
        self.assertEqual(reponse.status_code, 404)


if __name__ == "__main__":
    unittest.main()
