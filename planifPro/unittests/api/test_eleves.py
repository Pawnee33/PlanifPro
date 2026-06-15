#!/usr/bin/python3
"""
Tests d'intégration des endpoints élèves (vue professeur).

Couvre la liste des élèves d'un prof (200 / 404 / 403), le détail,
la modification de la durée de cours, le retrait et les chemins
d'erreur de l'invitation.
"""
import unittest

from planifPro.unittests.models.tests_base import BaseTestCase


class TestElevesAPI(BaseTestCase):

    def _prof_classe_et_eleve(self):
        """Prof + classe + élève rattaché. Renvoie (token_prof, classe, eleve_id, token_eleve)."""
        _, p_prof = self.inscrire(role="professeur")
        token_prof = self.connexion(p_prof["email"])
        classe = self.creer_classe(token_prof)
        rep_eleve, p_eleve = self.inscrire(role="eleve")
        eleve_id = rep_eleve.get_json()["id"]
        token_eleve = self.connexion(p_eleve["email"])
        self.rejoindre_classe(token_eleve, classe["code_classe"])
        return token_prof, classe, eleve_id, token_eleve

    def test_lister_eleves_du_prof(self):
        token_prof, _, _, _ = self._prof_classe_et_eleve()
        reponse = self.client.get(
            "/api/v1/eleves/", headers=self.entetes_auth(token_prof)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_lister_eleves_sans_eleve(self):
        _, p_prof = self.inscrire(role="professeur")
        token_prof = self.connexion(p_prof["email"])
        reponse = self.client.get(
            "/api/v1/eleves/", headers=self.entetes_auth(token_prof)
        )
        self.assertEqual(reponse.status_code, 404)

    def test_lister_eleves_eleve_refuse(self):
        _, p_eleve = self.inscrire(role="eleve")
        token_eleve = self.connexion(p_eleve["email"])
        reponse = self.client.get(
            "/api/v1/eleves/", headers=self.entetes_auth(token_eleve)
        )
        self.assertEqual(reponse.status_code, 403)

    def test_detail_eleve(self):
        token_prof, _, eleve_id, _ = self._prof_classe_et_eleve()
        reponse = self.client.get(
            f"/api/v1/eleves/{eleve_id}", headers=self.entetes_auth(token_prof)
        )
        self.assertEqual(reponse.status_code, 200)

    def test_modifier_duree_eleve(self):
        token_prof, classe, eleve_id, _ = self._prof_classe_et_eleve()
        reponse = self.client.put(
            f"/api/v1/eleves/{eleve_id}",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": classe["id"], "duree_minutes": 45},
        )
        self.assertEqual(reponse.status_code, 200)

    def test_modifier_duree_invalide(self):
        token_prof, classe, eleve_id, _ = self._prof_classe_et_eleve()
        reponse = self.client.put(
            f"/api/v1/eleves/{eleve_id}",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": classe["id"], "duree_minutes": 0},
        )
        self.assertEqual(reponse.status_code, 400)

    def test_retirer_eleve(self):
        token_prof, _, eleve_id, _ = self._prof_classe_et_eleve()
        reponse = self.client.delete(
            f"/api/v1/eleves/{eleve_id}", headers=self.entetes_auth(token_prof)
        )
        self.assertEqual(reponse.status_code, 200)

    # ----- Invitation (chemins d'erreur, sans envoi réel) -----
    def test_inviter_email_invalide(self):
        token_prof, classe, _, _ = self._prof_classe_et_eleve()
        reponse = self.client.post(
            "/api/v1/eleves/inviter",
            headers=self.entetes_auth(token_prof),
            json={"email": "pasunemail", "classe_id": classe["id"]},
        )
        self.assertEqual(reponse.status_code, 400)

    def test_inviter_classe_introuvable(self):
        _, p_prof = self.inscrire(role="professeur")
        token_prof = self.connexion(p_prof["email"])
        reponse = self.client.post(
            "/api/v1/eleves/inviter",
            headers=self.entetes_auth(token_prof),
            json={"email": "x@y.com", "classe_id": self.FAKE_UUID},
        )
        self.assertEqual(reponse.status_code, 404)

    def test_inviter_eleve_refuse(self):
        _, p_eleve = self.inscrire(role="eleve")
        token_eleve = self.connexion(p_eleve["email"])
        reponse = self.client.post(
            "/api/v1/eleves/inviter",
            headers=self.entetes_auth(token_eleve),
            json={"email": "x@y.com", "classe_id": self.FAKE_UUID},
        )
        self.assertEqual(reponse.status_code, 403)


if __name__ == "__main__":
    unittest.main()
