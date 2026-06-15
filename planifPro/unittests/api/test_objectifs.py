#!/usr/bin/python3
"""
Tests d'intégration des endpoints d'objectifs.

Gardes de rôle (403), existence (404) et liste vide. La création réelle
dépend d'un créneau validé (fragile) et n'est pas couverte ici ; on teste
le chemin créneau introuvable.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestObjectifsAPI(BaseTestCase):

    URL = "/api/v1/objectifs/"

    def _payload(self):
        return {
            "eleve_id": self.FAKE_UUID,
            "creneau_id": self.FAKE_UUID,
            "contenu": "Travailler les gammes",
            "conseils": "30 minutes par jour",
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
            self.URL, headers=self.entetes_auth(token), json=self._payload()
        )
        self.assertEqual(reponse.status_code, 403)

    def test_creer_creneau_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            self.URL, headers=self.entetes_auth(token), json=self._payload()
        )
        self.assertEqual(reponse.status_code, 404)

    def test_objectifs_creneau_prof_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.get(
            f"{self.URL}creneau/{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 403)

    def test_objectifs_creneau_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(
            f"{self.URL}creneau/{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_objectifs_eleve_prof_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.get(
            f"{self.URL}eleve/{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 403)

    def test_objectifs_eleve_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(
            f"{self.URL}eleve/{self.FAKE_UUID}", headers=self.entetes_auth(token)
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
            json=self._payload(),
        )
        self.assertEqual(reponse.status_code, 403)

    def test_modifier_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.put(
            f"{self.URL}{self.FAKE_UUID}",
            headers=self.entetes_auth(token),
            json=self._payload(),
        )
        self.assertEqual(reponse.status_code, 404)

    def test_supprimer_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.delete(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 403)

    def test_supprimer_introuvable(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.delete(
            f"{self.URL}{self.FAKE_UUID}", headers=self.entetes_auth(token)
        )
        self.assertEqual(reponse.status_code, 404)


if __name__ == "__main__":
    unittest.main()
