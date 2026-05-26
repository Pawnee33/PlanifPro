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
pip install flask flask-sqlalchemy flask-migrate flask-jwt-extended flask-bcrypt flask-cors psycopg2-binary sendgrid firebase-admin google-api-python-client google-auth-oauthlib python-dotenv pytest pytest-flask
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