#!/usr/bin/python3
"""
Tests d'intégration des endpoints professeurs (vue élève).

Couvre la liste des professeurs d'un élève (200 / 403), le détail,
l'inscription via code (rejoindre) et la désinscription.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestProfesseursAPI(BaseTestCase):

    def _prof_classe_et_eleve(self):
        """Prof + classe + élève rattaché. Renvoie (prof_id, token_prof, classe, token_eleve)."""
        rep_prof, p_prof = self.inscrire(role="professeur")
        prof_id = rep_prof.get_json()["id"]
        token_prof = self.connexion(p_prof["email"])
        classe = self.creer_classe(token_prof)
        _, p_eleve = self.inscrire(role="eleve")
        token_eleve = self.connexion(p_eleve["email"])
        self.rejoindre_classe(token_eleve, classe["code_classe"])
        return prof_id, token_prof, classe, token_eleve

    def test_lister_professeurs_de_eleve(self):
        _, _, _, token_eleve = self._prof_classe_et_eleve()
        reponse = self.client.get(
            "/api/v1/professeurs/", headers=self.entetes_auth(token_eleve)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_lister_professeurs_prof_refuse(self):
        _, token_prof, _, _ = self._prof_classe_et_eleve()
        reponse = self.client.get(
            "/api/v1/professeurs/", headers=self.entetes_auth(token_prof)
        )
        self.assertEqual(reponse.status_code, 403)

    def test_detail_professeur(self):
        prof_id, _, _, token_eleve = self._prof_classe_et_eleve()
        reponse = self.client.get(
            f"/api/v1/professeurs/{prof_id}",
            headers=self.entetes_auth(token_eleve),
        )
        self.assertEqual(reponse.status_code, 200)

    def test_rejoindre_via_professeurs(self):
        _, p_prof = self.inscrire(role="professeur")
        token_prof = self.connexion(p_prof["email"])
        classe = self.creer_classe(token_prof)
        _, p_eleve = self.inscrire(role="eleve")
        token_eleve = self.connexion(p_eleve["email"])
        reponse = self.client.post(
            "/api/v1/professeurs/rejoindre",
            headers=self.entetes_auth(token_eleve),
            json={"code_unique": classe["code_classe"]},
        )
        self.assertEqual(reponse.status_code, 201)

    def test_rejoindre_code_inconnu(self):
        _, p_eleve = self.inscrire(role="eleve")
        token_eleve = self.connexion(p_eleve["email"])
        reponse = self.client.post(
            "/api/v1/professeurs/rejoindre",
            headers=self.entetes_auth(token_eleve),
            json={"code_unique": "INCONNU0"},
        )
        self.assertEqual(reponse.status_code, 404)

    def test_desinscription_professeur(self):
        prof_id, _, _, token_eleve = self._prof_classe_et_eleve()
        reponse = self.client.delete(
            f"/api/v1/professeurs/{prof_id}",
            headers=self.entetes_auth(token_eleve),
        )
        self.assertEqual(reponse.status_code, 200)


if __name__ == "__main__":
    unittest.main()
