#!/usr/bin/python3
"""
Tests unitaires du modèle Utilisateur.

Vérifie les règles de validation déclarées par les décorateurs @validates
(prénom, nom, email, rôle, token FCM) ainsi que la non-exposition du mot de
passe dans to_dict. Ces tests ne dépendent pas de la base de données.
"""
import unittest

from planifPro import create_app
from planifPro.backend.classes.utilisateur import Utilisateur


class TestUtilisateurModele(unittest.TestCase):

    def setUp(self):
        # Contexte applicatif pour lier db/bcrypt (aucune table nécessaire)
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def utilisateur_valide(self, **kwargs):
        """Instancie un Utilisateur valide, surchargeable champ par champ."""
        donnees = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@planifpro.com",
            "role": "professeur",
        }
        donnees.update(kwargs)
        return Utilisateur(**donnees)

    # ----- Cas nominal -----
    def test_creation_valide(self):
        utilisateur = self.utilisateur_valide()
        self.assertEqual(utilisateur.prenom, "Jean")
        self.assertEqual(utilisateur.nom, "Dupont")
        self.assertEqual(utilisateur.role, "professeur")

    # ----- Prénom -----
    def test_prenom_obligatoire(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(prenom="")

    def test_prenom_espaces_seulement(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(prenom="   ")

    def test_prenom_trop_long(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(prenom="A" * 51)

    def test_prenom_borne_valide(self):
        utilisateur = self.utilisateur_valide(prenom="A" * 50)
        self.assertEqual(len(utilisateur.prenom), 50)

    # ----- Nom -----
    def test_nom_obligatoire(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(nom="")

    def test_nom_trop_long(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(nom="B" * 51)

    def test_nom_borne_valide(self):
        utilisateur = self.utilisateur_valide(nom="B" * 50)
        self.assertEqual(len(utilisateur.nom), 50)

    # ----- Email -----
    def test_email_format_invalide(self):
        for email in ["invalide", "a@b", "@planifpro.com",
                      "jean@", "jean planifpro.com"]:
            with self.assertRaises(ValueError):
                self.utilisateur_valide(email=email)

    def test_email_formats_valides(self):
        for email in ["a@b.com", "jean.dupont@test.co",
                      "user-1@mail-domain.org"]:
            utilisateur = self.utilisateur_valide(email=email)
            self.assertEqual(utilisateur.email, email)

    # ----- Rôle -----
    def test_role_obligatoire(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(role="")

    def test_role_invalide(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(role="admin")

    def test_roles_valides(self):
        for role in ["professeur", "eleve"]:
            utilisateur = self.utilisateur_valide(role=role)
            self.assertEqual(utilisateur.role, role)

    # ----- Token FCM -----
    def test_token_fcm_none_accepte(self):
        utilisateur = self.utilisateur_valide(token_fcm=None)
        self.assertIsNone(utilisateur.token_fcm)

    def test_token_fcm_vide_refuse(self):
        with self.assertRaises(ValueError):
            self.utilisateur_valide(token_fcm="   ")

    # ----- to_dict -----
    def test_to_dict_n_expose_pas_le_mot_de_passe(self):
        utilisateur = self.utilisateur_valide()
        utilisateur.hash_password("motdepasse123")
        donnees = utilisateur.to_dict()
        self.assertNotIn("mot_de_passe_hash", donnees)
        self.assertIn("email", donnees)
        self.assertIn("role", donnees)


if __name__ == "__main__":
    unittest.main()
