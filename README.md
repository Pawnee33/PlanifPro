# PlanifPro

## Description:

PlanifPro est une application web et mobile (PWA : Application web progressive) de gestion de planning pédagogique.
Le publique visé sont les professeurs et coachs de toute catégories (ex : professeur de musique, sport etc) qui travail dans diférentes structures publiques, privés ou à leurs compte.
L'application permettra la gestion des cours et la génération de planning en fonction des différentes classes du formateur.

## Structure du projet : 

```
PlanifPro/
├── backend/
│   ├── classes/
│   ├── persistance/
│   ├── routes/
│   └── services/
│ 
├── documentations/
│   ├── Projet_Portfolio_MVP.pdf
│   └── Projet-Porfolio_Technical_Documentation.pdf
│ 
├── frontend/
│   ├── images/
│   └── pages/
│ 
├── unittests/
│ 
└── README.md
```

# Installation : PlanifPro Backend

## Prérequis
- Python 3.x
- PostgreSQL
- Git

---

## 0. Installer PostgreSQL

```bash
sudo apt-get update
sudo apt install postgresql postgresql-contrib
```

Démarrer le service PostgreSQL :

```bash
sudo service postgresql start
```

Vérifier l'installation :

```bash
psql --version
```

---

## 1. Cloner le projet

```bash
git clone https://github.com/ton-repo/planifpro.git
cd planifpro
```

---

## 2. Créer et activer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

> ⚠️ À chaque nouveau terminal, réactive le venv avec `source venv/bin/activate`
> Tu verras `(venv)` apparaître au début de ta ligne de commande.

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement :

```bash
pip install flask flask-restx flask-sqlalchemy flask-migrate flask-jwt-extended flask-bcrypt flask-cors psycopg2-binary sendgrid firebase-admin google-api-python-client google-auth-oauthlib python-dotenv pytest pytest-flask
```

---

## 4. Configurer les variables d'environnement

Copie le fichier `.env.example` et remplis les valeurs :

```bash
cp .env.example .env
```

Contenu du `.env` :

```
DATABASE_URL=postgresql://user:motdepasse@localhost/planifpro
JWT_SECRET_KEY=
SENDGRID_API_KEY=
FIREBASE_CREDENTIALS=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

---

## 5. Créer la base de données

```bash
psql -U postgres
CREATE DATABASE planifpro;
\q
```

---

## 6. Appliquer les migrations

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

---

## 7. Lancer le serveur

```bash
flask run
```

Le serveur tourne sur `http://localhost:5000`

---

## 8. Lancer les tests

```bash
pytest -v
```

---

## Dépendances principales

| Package | Usage |
|---------|-------|
| `flask` | Framework web |
| `flask-restx` | API REST + Swagger |
| `flask-sqlalchemy` | ORM base de données |
| `flask-migrate` | Migrations BDD |
| `flask-jwt-extended` | Authentification JWT |
| `flask-bcrypt` | Hachage des mots de passe |
| `flask-cors` | Gestion des CORS |
| `psycopg2-binary` | Connecteur PostgreSQL |
| `sendgrid` | Envoi d'emails |
| `firebase-admin` | Notifications push FCM |
| `google-api-python-client` | Google Calendar API |
| `google-auth-oauthlib` | OAuth 2.0 Google |
| `python-dotenv` | Variables d'environnement |
| `pytest` | Tests unitaires |
| `pytest-flask` | Tests Flask |


## Génération de clé JWT 

```
python3 -c "import secrets; print(secrets.token_hex(32))"
```

# Convention de nommage — PlanifPro

## Branches

| Format | Usage |
|--------|-------|
| `feature/nom-de-la-feature` | Nouvelle fonctionnalité |
| `fix/nom-du-bug` | Correction de bug |
| `hotfix/nom-du-fix` | Correction urgente en production |

**Exemples :**
```
feature/setup-flask-postgres
feature/authentification
feature/classes
fix/correction-jwt-token
hotfix/erreur-base-de-donnees
```

---

## Commits

| Préfixe | Usage |
|---------|-------|
| `feat:` | Nouvelle fonctionnalité |
| `fix:` | Correction de bug |
| `chore:` | Tâche technique (config, dépendances) |
| `test:` | Ajout de tests |
| `docs:` | Documentation |
| `scm:` | Tâche Git / SCM |

**Exemples :**
```
feat: ajout endpoint POST /classes
fix: correction erreur JWT expired
chore: mise à jour requirements.txt
test: tests unitaires modèle User
docs: mise à jour README
scm: ajout template Pull Request
```

---

## Workflow Git

```
main        → production uniquement (merge via PR depuis develop)
develop     → branche de développement principale
feature/*   → fonctionnalités (merge via PR vers develop)
fix/*       → corrections (merge via PR vers develop)
hotfix/*    → corrections urgentes (merge via PR vers main)
```

**Étapes pour chaque feature :**
```bash
# 1. Partir de develop
git checkout develop
git pull origin develop

# 2. Créer la branche
git checkout -b feature/nom-de-la-feature

# 3. Coder + commiter
git add .
git commit -m "feat: description du changement"

# 4. Pusher
git push origin feature/nom-de-la-feature

# 5. Créer une Pull Request vers develop sur GitHub
# 6. Merger après validation
# 7. Fermer l'issue liée (Closes #N)
```

# Rituels de développement — PlanifPro

## À chaque fonctionnalité terminée

1. `git add` fichiers concernés
2. `git commit -m "feat/fix/chore: description"`
3. `git push origin feature/ma-branche`
4. Créer une PR vers `develop` sur GitHub
5. Remplir le template de PR (description, issue liée, checklist)
6. Merger la PR
7. Fermer l'issue liée (`Closes #N`)

---

## À chaque fin de sprint

1. Vérifier que toutes les issues du sprint sont fermées
2. Faire une sprint review (démonstration des fonctionnalités)
3. Faire une rétrospective (ce qui a bien marché / blocages)
4. Planifier le sprint suivant

---

## À chaque fin de journée

1. Pusher ton travail en cours même si pas terminé
2. Mettre à jour le statut des issues sur GitHub
3. Noter les blocages ou questions pour le lendemain

---

## Bonnes pratiques Git

1. Toujours partir de `develop` avant de créer une branche
2. Ne jamais pusher directement sur `main` ou `develop`
3. Un commit = une tâche précise
4. `requirements.txt` à jour si nouveau package installé

---
# Migrations Flask-Migrate — PlanifPro

## Prérequis

- PostgreSQL installé et démarré
- Environnement virtuel activé
- Variables d'environnement configurées dans `.env`

---

## 1. Démarrer PostgreSQL

```bash
sudo service postgresql start
```

---

## 2. Créer la base de données

```bash
sudo -u postgres psql
```

Dans le shell PostgreSQL :

```sql
CREATE DATABASE planifpro;
\q
```

---

## 3. Initialiser Flask-Migrate

À faire **une seule fois** au début du projet :

```bash
flask --app planifPro.run db init
```

Crée le dossier `migrations/` avec la configuration d'Alembic.

---

## 4. Générer la migration

À faire à chaque fois que tu **ajoutes ou modifies un modèle** :

```bash
flask --app planifPro.run db migrate -m "description des changements"
```

Génère un fichier dans `migrations/versions/` qui décrit les changements à appliquer en base.

---

## 5. Appliquer la migration

```bash
flask --app planifPro.run db upgrade
```

Applique les changements en base de données.

---

## 6. Vérifier les tables créées

```bash
sudo -u postgres psql -d planifpro
\dt
\q
```

---

## Workflow à chaque modification de modèle

```
Modifier un modèle → flask db migrate -m "description" → flask db upgrade
```

---

## Commandes utiles

| Commande | Description |
|----------|-------------|
| `flask db init` | Initialiser Flask-Migrate (une seule fois) |
| `flask db migrate -m "message"` | Générer un fichier de migration |
| `flask db upgrade` | Appliquer les migrations |
| `flask db downgrade` | Annuler la dernière migration |
| `flask db history` | Voir l'historique des migrations |
| `flask db current` | Voir la migration actuelle |
