#!/usr/bin/python3
"""
Classe de base pour les tests d'API de PlanifPro.

Fournit la configuration commune (application de test, base de données
SQLite en mémoire, client HTTP) ainsi que des helpers d'authentification
et de fixtures (classe, rattachement, vœux, génération/validation de
planning) réutilisables par toutes les suites de tests d'endpoints.
"""
import unittest
import uuid

from planifPro import create_app, db


class BaseTestCase(unittest.TestCase):
    """Socle commun : app de test, BDD en mémoire, helpers JWT et fixtures."""

    FAKE_UUID = "00000000-0000-0000-0000-000000000000"

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.contexte = self.app.app_context()
        self.contexte.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.contexte.pop()

    # ----- Authentification -----
    def payload_inscription(self, role="professeur", prenom="Jean",
                            nom="Dupont", email=None,
                            mot_de_passe="motdepasse123"):
        """Construit un payload d'inscription valide (email unique par défaut)."""
        if email is None:
            email = f"user{uuid.uuid4().hex[:8]}@planifpro.com"
        return {
            "role": role,
            "prenom": prenom,
            "nom": nom,
            "email": email,
            "mot_de_passe": mot_de_passe,
        }

    def inscrire(self, **kwargs):
        """Inscrit un utilisateur. Renvoie (reponse, payload)."""
        payload = self.payload_inscription(**kwargs)
        reponse = self.client.post(
            "/api/v1/authentification/inscription", json=payload
        )
        return reponse, payload

    def connexion(self, email, mot_de_passe="motdepasse123"):
        """Connecte un utilisateur. Renvoie le token JWT, ou None si échec."""
        reponse = self.client.post(
            "/api/v1/authentification/connexion",
            json={"email": email, "mot_de_passe": mot_de_passe},
        )
        if reponse.status_code != 200:
            return None
        return reponse.get_json().get("access_token")

    def creer_et_connecter(self, role="professeur"):
        """Inscrit puis connecte un utilisateur. Renvoie (token, payload)."""
        _, payload = self.inscrire(role=role)
        token = self.connexion(payload["email"], payload["mot_de_passe"])
        return token, payload

    def entetes_auth(self, token):
        """Construit les headers Authorization à partir d'un token JWT."""
        return {"Authorization": f"Bearer {token}"}

    # ----- Fixtures classe -----
    def payload_classe(self, **kwargs):
        """Construit un payload de création de classe valide."""
        donnees = {
            "nom": "Conservatoire",
            "date_debut": "2026-09-01",
            "date_fin": "2027-06-30",
            "jours_horaires": {
                "lundi": {"debut": "09:00", "fin": "17:00"},
                "mardi": {"debut": "09:00", "fin": "12:00"},
            },
            "nombre_propositions": 3,
            "nombre_voeux_requis": 3,
            "nombre_jours_min": 2,
        }
        donnees.update(kwargs)
        return donnees

    def creer_classe(self, token, **kwargs):
        """Crée une classe (en tant que professeur) et renvoie son JSON."""
        reponse = self.client.post(
            "/api/v1/classes/",
            headers=self.entetes_auth(token),
            json=self.payload_classe(**kwargs),
        )
        return reponse.get_json()

    def rejoindre_classe(self, token_eleve, code_classe):
        """Rattache l'élève connecté à une classe via son code. Renvoie la réponse."""
        return self.client.post(
            "/api/v1/classes/rejoindre",
            headers=self.entetes_auth(token_eleve),
            json={"code_unique": code_classe},
        )

    # ----- Fixtures chaîne vœux / planning -----
    def payload_voeux(self):
        """Créneaux souhaités valides : 3 entrées réparties sur 2 jours."""
        return {
            "1": {"jour": "lundi", "heure": "09:00"},
            "2": {"jour": "lundi", "heure": "10:00"},
            "3": {"jour": "mardi", "heure": "09:00"},
        }

    def preparer_classe_pour_voeux(self):
        """
        Prof + classe (collecte lancée), un élève rattaché avec une durée.
        Les vœux ne sont PAS encore soumis.
        Renvoie (token_prof, classe, eleve_id, token_eleve).
        """
        _, p_prof = self.inscrire(role="professeur")
        token_prof = self.connexion(p_prof["email"])
        classe = self.creer_classe(token_prof)
        rep_eleve, p_eleve = self.inscrire(role="eleve")
        eleve_id = rep_eleve.get_json()["id"]
        token_eleve = self.connexion(p_eleve["email"])
        self.rejoindre_classe(token_eleve, classe["code_classe"])
        self.client.post(
            f"/api/v1/classes/{classe['id']}/collecte",
            headers=self.entetes_auth(token_prof),
        )
        self.client.put(
            f"/api/v1/eleves/{eleve_id}",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": classe["id"], "duree_minutes": 60},
        )
        return token_prof, classe, eleve_id, token_eleve

    def soumettre_voeux(self, token_eleve, classe_id, creneaux=None):
        """Soumet les vœux d'un élève. Renvoie la réponse."""
        return self.client.post(
            "/api/v1/voeux/",
            headers=self.entetes_auth(token_eleve),
            json={
                "classe_id": classe_id,
                "creneaux_souhaites": creneaux or self.payload_voeux(),
            },
        )

    def preparer_classe_avec_voeux(self):
        """Comme preparer_classe_pour_voeux, mais avec les vœux déjà soumis."""
        token_prof, classe, eleve_id, token_eleve = self.preparer_classe_pour_voeux()
        self.soumettre_voeux(token_eleve, classe["id"])
        return token_prof, classe, eleve_id, token_eleve

    def generer_plannings(self, token_prof, classe_id):
        """Génère les propositions de planning. Renvoie la réponse."""
        return self.client.post(
            "/api/v1/plannings/generer",
            headers=self.entetes_auth(token_prof),
            json={"classe_id": classe_id},
        )

    def generer_et_valider(self, token_prof, classe_id):
        """Génère puis valide la première proposition. Renvoie la liste des plannings."""
        plannings = self.generer_plannings(token_prof, classe_id).get_json()
        if isinstance(plannings, list) and plannings:
            self.client.put(
                "/api/v1/plannings/valider",
                headers=self.entetes_auth(token_prof),
                json={"planning_id": plannings[0]["id"]},
            )
        return plannings
