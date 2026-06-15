#!/usr/bin/python3
"""
Tests unitaires du modèle Notification.

Vérifie les règles @validates : type (valeurs autorisées), titre (non vide,
max 50 caractères), message (chaîne) et lu (booléen).
"""
import unittest

from planifPro import create_app
from planifPro.backend.classes.notification import Notification


class TestNotificationModele(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()

    def tearDown(self):
        self.contexte.pop()

    def notification_valide(self, **kwargs):
        donnees = {
            "type": "voeux_soumis",
            "titre": "Nouveau vœu",
            "message": "Un élève a soumis ses vœux",
            "lu": False,
        }
        donnees.update(kwargs)
        return Notification(**donnees)

    def test_creation_valide(self):
        notification = self.notification_valide()
        self.assertEqual(notification.titre, "Nouveau vœu")
        self.assertFalse(notification.lu)

    def test_type_invalide(self):
        with self.assertRaises(ValueError):
            self.notification_valide(type="autre")

    def test_titre_vide(self):
        with self.assertRaises(ValueError):
            self.notification_valide(titre="")

    def test_titre_trop_long(self):
        with self.assertRaises(ValueError):
            self.notification_valide(titre="A" * 51)

    def test_message_non_string(self):
        with self.assertRaises(ValueError):
            self.notification_valide(message=123)

    def test_lu_non_booleen(self):
        with self.assertRaises(ValueError):
            self.notification_valide(lu="oui")


if __name__ == "__main__":
    unittest.main()
