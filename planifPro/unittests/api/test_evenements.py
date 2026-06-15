#!/usr/bin/python3
"""
Tests d'intégration des endpoints d'événements.

Création réelle (un cas, destinataires « toutes_classes »), refus de rôle,
date invalide, liste vide et chemins introuvables.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestEvenementsAPI(BaseTestCase):

    URL = "/api/v1/evenements/"

    def _payload(self, **kwargs):
        donnees = {
            "titre": "Audition",
            "description": "Audition de fin d'année",
            "date_heure": "2026-06-30T18:00:00",
            "destinataires": {"type": "toutes_classes"},
        }
        donnees.update(kwargs)
        return donnees

    def test_creer(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            self.URL, headers=self.entetes_auth(token), json=self._payload()
        )
        self.assertEqual(reponse.status_code, 201)

    def test_creer_eleve_refuse(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.post(
            self.URL, headers=self.entetes_auth(token), json=self._payload()
        )
        self.assertEqual(reponse.status_code, 403)

    def test_creer_date_invalide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.post(
            self.URL,
            headers=self.entetes_auth(token),
            json=self._payload(date_heure="pas-une-date"),
        )
        self.assertEqual(reponse.status_code, 400)

    def test_lister_prof_vide(self):
        token, _ = self.creer_et_connecter("professeur")
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
        self.assertEqual(reponse.status_code, 404)

    def test_lister_eleve_vide(self):
        token, _ = self.creer_et_connecter("eleve")
        reponse = self.client.get(self.URL, headers=self.entetes_auth(token))
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
