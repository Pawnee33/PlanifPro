# PlanifPro

## Description :

PlanifPro est une application web et mobile (PWA : Progressive Web App) de gestion de planning pédagogique.
Le public visé : les professeurs et coachs de toutes catégories (ex : professeur de musique, de sport, etc.) qui travaillent dans différentes structures publiques, privées, ou à leur compte.
L'application permet la gestion des cours et la génération de planning en fonction des différentes classes du formateur.

Le principe : le professeur définit ses disponibilités, les élèves soumettent leurs vœux de créneaux, un algorithme génère **trois propositions de planning**, et le professeur en valide une.

---

## Fonctionnalités :

### Côté professeur / coach
- Création et gestion de classes (conservatoire, cours privé, association) avec code unique de rattachement
- Invitation d'élèves par email (Brevo) ou partage du code de classe
- Définition des disponibilités et lancement de la collecte des vœux
- Génération automatique de **3 propositions de planning** par algorithme, puis sélection et validation de l'une d'elles
- Réajustement du planning validé : ajout / modification / suppression de créneaux avec portée (ce jour / toute la période / plusieurs jours)
- Créneaux personnels ponctuels
- Objectifs pédagogiques datés, par élève
- Événements avec 3 modes de destinataires (toutes les classes / classes ciblées / élèves ciblés)
- Notifications : push (Firebase FCM) + email (Brevo) + in-app
- Export / import Google Calendar (OAuth 2.0)
- Dashboard responsive avec planning global (FullCalendar)

### Côté élève
- Rejoindre une ou plusieurs classes via un code
- Soumission des vœux de créneaux (une soumission par classe)
- Consultation du planning validé
- Réception des objectifs, événements et notifications
- Export / import Google Calendar
- Interface responsive (mobile / desktop), PWA installable

---

## Stack technique :

### Frontend : déployé sur Vercel
| Techno | Usage |
|--------|-------|
| React + Vite | Framework SPA + build |
| Tailwind CSS v4 | Styles (charte via `@theme`) |
| FullCalendar | Affichage des plannings |
| react-router-dom | Routage |
| lucide-react | Icônes |
| vite-plugin-pwa | PWA installable + service worker |

### Backend : déployé sur Render
| Techno | Usage |
|--------|-------|
| Flask + Flask-RESTX | API REST + Swagger |
| SQLAlchemy + Flask-Migrate | ORM + migrations |
| PostgreSQL | Base de données |
| Flask-JWT-Extended | Authentification JWT |
| Flask-Bcrypt | Hachage des mots de passe |
| gunicorn | Serveur WSGI de production |

### Services externes
| Service | Usage |
|---------|-------|
| Firebase Cloud Messaging | Notifications push |
| Brevo | Envoi d'emails |
| Google Calendar API (OAuth 2.0) | Export / import de créneaux |

---

## Captures d'écran :

> Placez vos captures dans `planifPro/documentations/captures/` puis mettez à jour les chemins ci-dessous.

| Écran | Aperçu |
|-------|--------|
| Connexion | `![Connexion](planifPro/documentations/captures/connexion.png)` |
| Dashboard professeur | `![Dashboard prof](planifPro/documentations/captures/dashboard-prof.png)` |
| Dashboard élève | `![Dashboard élève](planifPro/documentations/captures/dashboard-eleve.png)` |

_(Retirez les accents graves une fois les images ajoutées pour que Markdown les affiche.)_

---

## Structure du projet :

```
PlanifPro/
├── .env.example                       # modèle de variables d'environnement (back)
├── .github/
│   └── pull_request_template.md
├── README.md
├── config.py                          # configurations Dev / Prod
├── requirements.txt
├── cle_google/                        # secret Google OAuth (non versionné)
├── cle_firebase/                      # secret Firebase (non versionné)
├── migrations/                        # Flask-Migrate / Alembic
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                      # fichiers de migration
├── tests/                             # scripts de test API (curl)
│   ├── test_auth.sh
│   ├── test_setup.sh
│   ├── test_classes.sh
│   ├── test_voeux.sh
│   ├── test_planning.sh
│   ├── test_creneaux.sh
│   ├── test_evenements.sh
│   ├── test_objectifs.sh
│   └── test_chantecler.sh
└── planifPro/
    ├── __init__.py                    # create_app()
    ├── run.py                         # point d'entrée (app = create_app())
    ├── backend/
    │   ├── classes/                   # modèles SQLAlchemy
    │   │   ├── entitebase.py
    │   │   ├── utilisateur.py
    │   │   ├── professeur.py
    │   │   ├── eleve.py
    │   │   ├── classe.py
    │   │   ├── voeu.py
    │   │   ├── planning.py
    │   │   ├── creneau.py
    │   │   ├── creneau_perso.py
    │   │   ├── objectif.py
    │   │   ├── evenement.py
    │   │   ├── notification.py
    │   │   └── tables_relations.py
    │   ├── persistence/               # repositories (pattern Repository)
    │   │   ├── repository.py
    │   │   ├── utilisateur_repository.py
    │   │   ├── professeur_repository.py
    │   │   ├── eleve_repository.py
    │   │   ├── classe_repository.py
    │   │   ├── voeu_repository.py
    │   │   ├── planning_repository.py
    │   │   ├── creneau_repository.py
    │   │   ├── creneau_perso_repository.py
    │   │   ├── objectif_repository.py
    │   │   ├── evenement_repository.py
    │   │   └── notification_repository.py
    │   ├── routes/                    # endpoints Flask-RESTX
    │   │   ├── authentification.py
    │   │   ├── utilisateurs.py
    │   │   ├── professeurs.py
    │   │   ├── eleves.py
    │   │   ├── classes.py
    │   │   ├── voeux.py
    │   │   ├── plannings.py
    │   │   ├── creneaux.py
    │   │   ├── creneaux_perso.py
    │   │   ├── objectifs.py
    │   │   ├── evenements.py
    │   │   ├── notifications.py
    │   │   └── calendrier.py
    │   └── services/                  # façades + services externes
    │       ├── facade.py              # PlanifProFacade (agrège les 4 façades)
    │       ├── auth_facade.py
    │       ├── classe_voeu_facade.py
    │       ├── planning_creneau_facade.py
    │       ├── objectif_evenement_notification_facade.py
    │       ├── email_service.py       # Brevo
    │       └── fcm_service.py         # Firebase Cloud Messaging
    ├── unittests/                     # tests unitaires (pytest)
    │   ├── api/                       # tests des routes
    │   └── models/                    # tests des modèles
    ├── documentations/
    │   ├── Projet_Portfolio_MVP.pdf
    │   └── Projet-Porfolio_Technical_Documentation.pdf
    └── frontend/                      # application React (Vite + Tailwind v4 + FullCalendar)
        ├── index.html
        ├── package.json
        ├── vite.config.js
        ├── eslint.config.js
        ├── .env.example               # variables front (VITE_*)
        ├── public/                    # favicon + icônes PWA (pwa-192, pwa-512)
        └── src/
            ├── main.jsx               # point d'entrée React
            ├── App.jsx                # routes (react-router-dom)
            ├── index.css              # Tailwind + charte (@theme)
            ├── assets/                # logo, hero
            ├── services/              # couche API
            │   ├── helper.js          # wrapper fetch + JWT (api.get/post/put/delete)
            │   └── google.js          # OAuth + export/import Google Calendar
            ├── utils/
            │   └── creneaux.js        # helpers créneaux FullCalendar
            ├── pages/
            │   ├── Connexion.jsx
            │   ├── Inscription.jsx
            │   ├── GoogleCallback.jsx
            │   ├── DashboardProfesseur.jsx
            │   └── eleve/
            │       └── DashboardEleve.jsx
            └── components/
                ├── EnTete.jsx / PiedDePage.jsx / RouteProtegee.jsx / MenuBurger.jsx
                ├── Calendrier.jsx / CalendrierProposition.jsx
                ├── BarreLaterale.jsx / EspaceClasse.jsx / ClasseEleves.jsx
                ├── CarteStatistique.jsx
                ├── Panneau*.jsx                                        # Voeux, Eleves, Planning, Notifications
                ├── Fiche*.jsx                                          # FicheEleve, FicheEvenement
                ├── Popup*.jsx                                          # popups prof (classe, créneau, événement, objectif, invitation…)
                ├── ui/                                                 # CarteStat, CarteInfo, SectionBarre, SectionHoraires
                └── eleve/                                              # composants spécifiques élève
                    │                                              
                    ├── BarreLateraleEleve.jsx / CalendrierEleve.jsx / FormulaireVoeux.jsx
                    ├── Fiche*.jsx                                      # Objectif, Evenement, Professeur
                    └── Popup*.jsx                                      # RejoindreClasse, ImportGoogle, Objectif
```

---

## Architecture :

Le backend suit une **architecture en couches** :

- **Routes (Flask-RESTX)** : exposent les endpoints REST, valident les entrées, gèrent les codes HTTP et l'authentification JWT.
- **Façade (`PlanifProFacade`)** : point d'entrée unique de la logique métier. Elle agrège quatre façades spécialisées (`AuthFacade`, `ClasseVoeuFacade`, `PlanningCreneauFacade`, `ObjectifEvenementNotificationFacade`). Les routes ne parlent jamais directement aux repositories.
- **Repositories (pattern Repository)** : encapsulent tous les accès SQLAlchemy. Une classe de base `SQLAlchemyRepository` factorise les opérations CRUD communes.
- **Modèles (SQLAlchemy)** : définissent les tables, les validations (`@validates`) et la sérialisation (`to_dict()`).

Ce découpage isole la logique métier de la persistance et des routes, ce qui facilite les tests et les évolutions.

Côté frontend, l'application est une **SPA React** organisée en pages (une par écran) et composants réutilisables, avec une couche services (`helper.js`) qui centralise les appels API et l'injection du token JWT.

---

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
git clone https://github.com/Pawnee33/PlanifPro.git
cd PlanifPro
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
pip install flask flask-restx flask-sqlalchemy flask-migrate flask-jwt-extended flask-bcrypt flask-cors psycopg2-binary sib-api-v3-sdk firebase-admin google-api-python-client google-auth-oauthlib python-dotenv gunicorn pytest pytest-flask
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
BREVO_API_KEY=
BREVO_FROM_EMAIL=
FIREBASE_CREDENTIALS=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:5000/api/v1/calendrier/callback
GOOGLE_CLIENT_SECRETS=
```

> ⚠️ Le `.env` (vraies clés) ne doit **jamais** être versionné. Seul `.env.example`
> (avec des valeurs bidon) est suivi par Git.

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
export FLASK_APP=planifPro.run        # une fois par terminal

flask db init        # une seule fois au tout début (si le dossier migrations/ n'existe pas)
flask db migrate -m "initial migration"
flask db upgrade
```

> Après un simple clone, le dossier `migrations/` existe déjà : un `flask db upgrade` suffit.

---

## 7. Lancer le serveur

### Mode développement (debug, local)

```bash
flask --app planifPro.run run --debug
# ou directement :
python -m planifPro.run
```

Le serveur tourne sur `http://localhost:5000` (base de l'API : `/api/v1`).

### Mode production

```bash
gunicorn "planifPro.run:app"
```

C'est la commande utilisée par Render. Le mode (debug ou non) est piloté par les
classes de `config.py` (`DevelopmentConfig` / `ProductionConfig`), sélectionnées
dans `create_app()`.

---

## 8. Lancer les tests

Tests unitaires :

```bash
pytest -v
```

Tests d'API (curl) : voir la section **Tests** plus bas.

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
| `sib-api-v3-sdk` | Envoi d'emails (Brevo) |
| `firebase-admin` | Notifications push FCM |
| `google-api-python-client` | Google Calendar API |
| `google-auth-oauthlib` | OAuth 2.0 Google |
| `python-dotenv` | Variables d'environnement |
| `gunicorn` | Serveur WSGI de production |
| `pytest` | Tests unitaires |
| `pytest-flask` | Tests Flask |


## Génération de clé JWT

```
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

# Installation : PlanifPro Frontend

## Prérequis
- Node.js 18+ (LTS recommandé)
- npm
- Le backend lancé (voir section précédente)

---

## 1. Aller dans le dossier frontend

```bash
cd planifPro/frontend
```

---

## 2. Installer les dépendances

```bash
npm install
```

---

## 3. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Contenu du `.env` :

```
VITE_API_URL=http://localhost:5000/api/v1
```

> `VITE_API_URL` est l'URL de base de l'API backend. En production, remplace-la par
> l'URL publique de l'API (Render).

---

## 4. Lancer le serveur de développement

```bash
npm run dev
```

Le front tourne sur `http://localhost:5173`.

---

## 5. Build de production

```bash
npm run build       # génère le dossier dist/
npm run preview     # sert le build localement pour vérification
```
---

# Installation avec Docker

Alternative à l'installation manuelle : lancer toute la stack (base PostgreSQL + backend + frontend) en une seule commande, sans installer Python, Node ni PostgreSQL sur la machine.

## Prérequis
- Docker
- Docker Compose (plugin v2 : commande `docker compose`)

---

## 1. Configurer les variables d'environnement

Le `docker-compose.yml` lit ton fichier `.env` (back) pour les clés Brevo, Google et JWT. Assure-toi qu'il existe à la racine (voir section *Configurer les variables d'environnement* plus haut).

> `DATABASE_URL` est **surchargée** automatiquement par le compose pour pointer vers le conteneur PostgreSQL — pas besoin d'y toucher.

Les fichiers de clés (`cle_google/`, `cle_firebase/`) doivent être présents à la racine : ils sont montés dans le conteneur au lancement (jamais copiés dans l'image).

---

## 2. Lancer la stack

```bash
docker compose up --build
```

- `--build` (re)construit les images (nécessaire la première fois).
- Les migrations (`flask db upgrade`) sont appliquées automatiquement au démarrage du backend.

Les services démarrés :

| Service | Description | Accès |
|---------|-------------|-------|
| `db` | Base PostgreSQL 16 | interne (port 5432) |
| `back` | API Flask (gunicorn) | http://localhost:5000 |
| `front` | Front React servi par nginx | http://localhost:8080 |

---

## 3. Utiliser l'application

Ouvre **http://localhost:8080** dans le navigateur.

> La base démarre **vierge**. Crée un compte via l'inscription, ou rejoue les scripts de `tests/` pour peupler des données de démonstration.

---

## 4. Arrêter la stack

```bash
docker compose down       # arrête et supprime les conteneurs (garde la base)
docker compose down -v    # + supprime le volume PostgreSQL (remet la base à zéro)
```

---

## Architecture Docker

| Fichier | Rôle |
|---------|------|
| `Dockerfile` (racine) | Image du backend (Python 3.12 + gunicorn) |
| `planifPro/frontend/Dockerfile` | Image du frontend (build Node 20 multi-stage → nginx) |
| `planifPro/frontend/nginx.conf` | Config nginx : routage SPA (`try_files` vers `index.html`) |
| `docker-compose.yml` | Orchestration des 3 services + réseau + volumes |
| `.dockerignore` | Exclusion des secrets et fichiers inutiles des images |
---

# Convention de nommage : PlanifPro

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

# Rituels de développement : PlanifPro

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
# Migrations Flask-Migrate : PlanifPro

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

## Tests

Les tests d'API sont réalisés avec `curl` (scripts bash dans `tests/`). À lancer avec le **serveur Flask démarré** et sur une **base de données propre**, dans l'ordre ci-dessous.

### Prérequis

```bash
# Rendre les scripts exécutables (une seule fois)
chmod +x tests/*.sh
```

### Ordre d'exécution

```bash
# 1. Authentification : inscription / connexion (indépendant)
./tests/test_auth.sh

# 2. Données de base : 1 professeur + 20 élèves
./tests/test_setup.sh

# 3. Création des classes (Conservatoire, Cours Privé) + rattachement des élèves
./tests/test_classes.sh

# 4. Soumission des vœux + tests des endpoints vœux
./tests/test_voeux.sh

# 5. Flux planning complet : génération, vérification du placement,
#    sélection → modification → validation, et planning global (dashboard)
./tests/test_planning.sh

# 6. Créneaux : ajout / modification / suppression avec portée
./tests/test_creneaux.sh

# 7. Événements
./tests/test_evenements.sh

# 8. Objectifs pédagogiques
./tests/test_objectifs.sh

# Commande pour tout supprimer (reset de la base)
sudo -u postgres psql -d planifpro -c "TRUNCATE utilisateurs CASCADE;"
```

> Les scripts 2 à 5 s'enchaînent et réutilisent les données créées par les précédents.
> Relance la chaîne sur une base propre : les plannings sont générés une seule fois par classe
> (une 2ᵉ génération renvoie une erreur `409`).
>
> `test_chantecler.sh` est un scénario de démonstration complet (données de test dédiées).

---

## Déploiement :

- **Frontend** : déployé sur **Vercel** (build automatique à partir de `planifPro/frontend/`).
- **Backend** : déployé sur **Render** (`gunicorn "planifPro.run:app"`).
- **Base de données** : PostgreSQL managé (Render).

> URLs de production : _à compléter une fois le déploiement effectué._

Variables d'environnement à définir côté hébergeur :
- **Back (Render)** : `DATABASE_URL`, `JWT_SECRET_KEY`, `BREVO_API_KEY`, `BREVO_FROM_EMAIL`, `FIREBASE_CREDENTIALS`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`, `GOOGLE_CLIENT_SECRETS`
- **Front (Vercel)** : `VITE_API_URL` (URL publique de l'API)

---

## Auteur :

Projet portfolio réalisé en solo dans le cadre de la formation **Holberton School Bordeaux**.

- **Pawnee Defize** : [GitHub](https://github.com/Pawnee33)
- [LinkedIn](https://www.linkedin.com/in/pawnee-defize/)
