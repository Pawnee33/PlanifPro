# PlanifPro

## Description :

PlanifPro est une application web et mobile (PWA : Progressive Web App) de gestion de planning pédagogique.
Le public visé : les professeurs et coachs de toutes catégories (ex : professeur de musique, de sport, etc.) qui travaillent dans différentes structures publiques, privées, ou à leur compte.
L'application permet la gestion des cours et la génération de planning en fonction des différentes classes du formateur.

## Structure du projet :

```
PlanifPro/
├── .env.example                       # modèle de variables d'environnement
├── README.md
├── config.py                          # configurations Dev / Prod
├── requirements.txt
├── migrations/                        # Flask-Migrate / Alembic
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                      # fichiers de migration
├── planifPro/
│   ├── __init__.py                    # create_app()
│   ├── run.py                         # point d'entrée (app = create_app())
│   ├── backend/
│   │   ├── classes/                   # modèles SQLAlchemy
│   │   │   ├── entitebase.py
│   │   │   ├── utilisateur.py
│   │   │   ├── professeur.py
│   │   │   ├── eleve.py
│   │   │   ├── classe.py
│   │   │   ├── voeu.py
│   │   │   ├── planning.py
│   │   │   ├── creneau.py
│   │   │   ├── creneau_perso.py
│   │   │   ├── objectif.py
│   │   │   ├── evenement.py
│   │   │   ├── notification.py
│   │   │   └── tables_relations.py
│   │   ├── persistence/               # repositories
│   │   │   ├── repository.py
│   │   │   ├── utilisateur_repository.py
│   │   │   ├── professeur_repository.py
│   │   │   ├── eleve_repository.py
│   │   │   ├── classe_repository.py
│   │   │   ├── voeu_repository.py
│   │   │   ├── planning_repository.py
│   │   │   ├── creneau_repository.py
│   │   │   ├── creneau_perso_repository.py
│   │   │   ├── objectif_repository.py
│   │   │   ├── evenement_repository.py
│   │   │   └── notification_repository.py
│   │   ├── routes/                    # endpoints Flask-RESTX
│   │   │   ├── authentification.py
│   │   │   ├── utilisateurs.py
│   │   │   ├── professeurs.py
│   │   │   ├── eleves.py
│   │   │   ├── classes.py
│   │   │   ├── voeux.py
│   │   │   ├── plannings.py
│   │   │   ├── creneaux.py
│   │   │   ├── creneaux_perso.py
│   │   │   ├── objectifs.py
│   │   │   ├── evenements.py
│   │   │   ├── notifications.py
│   │   │   └── calendrier.py
│   │   └── services/                  # façades + services
│   │       ├── facade.py
│   │       ├── auth_facade.py
│   │       ├── classe_voeu_facade.py
│   │       ├── planning_creneau_facade.py
│   │       ├── objectif_evenement_notification_facade.py
│   │       ├── email_service.py       # Brevo
│   │       └── fcm_service.py         # Firebase Cloud Messaging
│   ├── documentations/
│   │   ├── Projet_Portfolio_MVP.pdf
│   │   └── Projet-Porfolio_Technical_Documentation.pdf
│   ├── frontend/
│   │   ├── images/
│   │   └── pages/
│   └── unittests/                     # tests unitaires (pytest)
└── tests/                             # scripts de test API (curl)
    ├── test_auth.sh
    ├── test_setup.sh
    ├── test_classes.sh
    ├── test_voeux.sh
    └── test_planning.sh
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

# 6. Commande pour tout suprimer
sudo -u postgres psql -d planifpro -c "TRUNCATE utilisateurs CASCADE;"

# 7. Commande pour lancer le serveur backend
python -m planifPro.run
```

> Les scripts 2 à 5 s'enchaînent et réutilisent les données créées par les précédents.
> Relance la chaîne sur une base propre : les plannings sont générés une seule fois par classe
> (une 2ᵉ génération renvoie une erreur `409`).

# Installation : PlanifPro Frontend (React PWA)

Le frontend est une PWA développée avec **React + Vite**, stylée avec **Tailwind CSS v4**,
et installable grâce à **vite-plugin-pwa**. Il vit dans le dossier `planifPro/frontend/`.

## Prérequis
- Node.js 20+ (LTS recommandé)
- npm 10+

Vérifier l'installation :

```bash
node -v && npm -v
```

---

## 1. Initialiser le projet React avec Vite

Depuis la racine du projet, se placer dans le dossier frontend, puis scaffolder Vite **dans** ce dossier :

```bash
cd planifPro/frontend
npm create vite@latest .
```

Répondre aux questions :
- **Select a framework** → `React`
- **Select a variant** → `JavaScript` (sans React Compiler)
- **Install with npm and start now?** → `Yes`

Cela génère le squelette du projet, installe les dépendances (`node_modules/`) et lance le serveur de développement sur `http://localhost:5173`.

> Pour arrêter le serveur : `Ctrl + C`. Pour le relancer : `npm run dev`.

---

## 2. Nettoyer le boilerplate de démo

Repartir d'une base propre :
- `src/App.jsx` → composant minimal (voir ci-dessous)
- `src/index.css` → ne garder que l'import Tailwind (étape 3)
- Supprimer `src/App.css`

Contenu minimal de `src/App.jsx` (aucun import nécessaire) :

```jsx
function App() {
  return (
    <div className="text-2xl font-bold text-blue-700">
      PlanifPro
    </div>
  )
}

export default App
```

---

## 3. Configurer Tailwind CSS v4

Installer Tailwind et son plugin officiel pour Vite :

```bash
npm install -D tailwindcss @tailwindcss/vite
```

Brancher le plugin dans `vite.config.js` :

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

Importer Tailwind dans `src/index.css` (obligatoirement en **première ligne**) :

```css
@import "tailwindcss";
```

> En Tailwind v4, plus besoin de `tailwind.config.js`. La configuration (couleurs, polices)
> se fait directement dans le CSS via le bloc `@theme`.

Charte graphique de PlanifPro (à ajouter juste après l'import dans `src/index.css`) :

```css
@theme {
  --color-bleu-nuit: #0C2863;
  --color-bleu-marine: #181F72;
  --color-bleu-roi: #223397;
  --color-bleu-moyen: #4065B6;
  --color-bleu-ciel: #4975BF;
  --color-bleu-clair: #4C7AC3;
  --color-or: #D59813;
  --color-or-clair: #D5AE13;
  --color-violet: #9095F5;
}
```

Ces couleurs deviennent alors des classes utilitaires : `bg-bleu-nuit`, `text-or`, `border-violet`, etc.

---

## 4. Configurer la PWA (manifest + service worker)

Installer le plugin :

```bash
npm install -D vite-plugin-pwa
```

Ajouter `VitePWA` dans `vite.config.js` :

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',     // le service worker se met à jour tout seul
      devOptions: { enabled: true },  // permet de tester la PWA en mode dev
      manifest: {
        name: 'PlanifPro',
        short_name: 'PlanifPro',
        description: 'Gestion de planning pédagogique entre professeurs et élèves',
        theme_color: '#0C2863',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        icons: [
          { src: 'pwa-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
    }),
  ],
})
```

Placer deux icônes carrées au format PNG dans `public/` :
- `pwa-192.png` (192×192 px)
- `pwa-512.png` (512×512 px)

> Vérifier le manifest : DevTools (`F12`) → onglet **Application** → **Manifest**.
> Les icônes du manifest ne s'affichent pas dans la page : elles servent à l'installation de l'appli.

---

## 5. Configurer les variables d'environnement

Dans Vite, une variable doit commencer par `VITE_` pour être accessible côté React
(lecture via `import.meta.env.VITE_API_URL`).

Créer `planifPro/frontend/.env` (ignoré par Git) :

```
VITE_API_URL=http://localhost:5000/api/v1
```

Créer `planifPro/frontend/.env.example` (modèle versionné) avec la même ligne.

> Redémarrer le serveur après toute modification du `.env` :
> Vite ne lit les variables qu'au démarrage.

---

## 6. Lancer le frontend

```bash
cd planifPro/frontend
npm run dev
```

L'application est servie sur `http://localhost:5173`.

---

## Dépendances frontend principales

| Paquet | Usage |
|--------|-------|
| `react` / `react-dom` | Bibliothèque d'interface |
| `vite` | Outil de build et serveur de développement |
| `tailwindcss` + `@tailwindcss/vite` | Styles utility-first (v4) |
| `vite-plugin-pwa` | Manifest + service worker (PWA installable) |
| `react-router-dom` | Routage entre les pages |
| `@fullcalendar/react` (+ `timegrid`, `daygrid`, `interaction`) | Calendrier hebdomadaire interactif |
| `lucide-react` | Icônes |

---

## Structure du dossier frontend

```
planifPro/frontend/
├── public/                 # fichiers statiques (icônes PWA, favicon)
│   ├── pwa-192.png
│   └── pwa-512.png
├── src/
│   ├── assets/                 # images importées (logo…)
│   ├── pages/                  # pages routées
│   │   ├── Connexion.jsx
│   │   ├── Inscription.jsx
│   │   └── DashboardProfesseur.jsx
│   ├── components/             # composants de l'interface
│   │   ├── EnTete.jsx
│   │   ├── BarreLaterale.jsx
│   │   ├── Calendrier.jsx
│   │   ├── EspaceClasse.jsx
│   │   ├── FicheEleve.jsx
│   │   ├── FicheEvenement.jsx
│   │   ├── MenuBurger.jsx
│   │   ├── PanneauNotifications.jsx
│   │   ├── PanneauVoeux.jsx
│   │   ├── PanneauEleves.jsx
│   │   ├── PiedDePage.jsx
│   │   ├── RouteProtegee.jsx
│   │   ├── Popup… .jsx          # popups (créer/modifier classe, créneaux, objectifs, événements…)
│   │   └── ui/                  # petits composants (CarteStat…)
│   ├── services/
│   │   └── helper.js           # appels API (token, erreurs)
│   ├── utils/
│   │   └── creneaux.js         # conversion créneaux → événements FullCalendar
│   ├── App.jsx                 # routes (react-router)
│   ├── main.jsx                # point d'entrée
│   └── index.css               # import Tailwind + charte (@theme)
├── .env / .env.example
├── index.html
├── vite.config.js
└── package.json
```
## Fonctionnalités

### Espace professeur (complet)
- **Authentification** : inscription avec choix du rôle, connexion JWT, validation par la touche Entrée
- **Classes** : création (couleur, horaires, période), modification, copie du code d'invitation, configuration de la durée de cours par élève
- **Invitations** : invitation d'élèves par email (Brevo), individuellement ou depuis la barre latérale
- **Vœux & plannings** : collecte des vœux, génération de 3 propositions de planning, sélection, déplacement et échange de créneaux, suppression, validation
- **Planning global** : calendrier hebdomadaire (FullCalendar) de tous les créneaux validés, colorés par classe
- **Gestion des créneaux de cours** : ajout, modification/remplacement et suppression avec portée — ce jour, plusieurs jours, ou toute la période
- **Créneaux personnels** : ajout, modification et suppression de rendez-vous ponctuels au clic sur le planning
- **Suivi pédagogique** : objectifs datés par élève (depuis la fiche élève ou le planning), avec modification et suppression
- **Événements** : création avec notification ciblée (toutes les classes / classes spécifiques / élèves spécifiques), modification, suppression
- **Notifications** : cloche avec compteur de non-lues, panneau dédié, marquage « tout comme lu »
- **Navigation** : menu burger (profil, déconnexion), logo cliquable ramenant au planning

### Espace élève
- En cours de développement : soumission des vœux, consultation et confirmation du créneau attribué, consultation des objectifs, notifications, export Google Calendar.

---

## Architecture frontend

Le frontend suit quelques principes réutilisés dans tout le projet :
- **Helper API centralisé** (`src/services/helper.js`) : gère l'URL de base, le token JWT et les erreurs.
- **Popups réutilisables** : un même patron (overlay, fermeture, parent responsable de l'appel API et du rechargement).
- **Communication par callbacks** : les composants enfants remontent les actions au parent, qui détient l'état.
- **Conversion des créneaux** (`src/utils/creneaux.js`) : transforme les créneaux du back en événements FullCalendar (récurrents pour les cours, ponctuels pour les rendez-vous personnels).
