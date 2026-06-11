#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

PROF_EMAIL="prof@planifpro.com"
PROF_PASSWORD="motdepasse123"

ELEVE_EMAIL="eleve@planifpro.com"
ELEVE_PASSWORD="motdepasse456"

# ----- INSCRIPTION PROFESSEUR -----
echo "----- INSCRIPTION PROFESSEUR -----"
INSCRIPTION_PROF=$(curl -s -X POST $BASE_URL/authentification/inscription \
-H "Content-Type: application/json" \
-d "{\"prenom\":\"Pauline\",\"nom\":\"Defize\",\"email\":\"$PROF_EMAIL\",\"mot_de_passe\":\"$PROF_PASSWORD\",\"role\":\"professeur\"}")
echo $INSCRIPTION_PROF
echo ""

# ----- INSCRIPTION EMAIL DEJA UTILISE -----
echo "----- INSCRIPTION EMAIL DEJA UTILISE -----"
INSCRIPTION_DOUBLON=$(curl -s -X POST $BASE_URL/authentification/inscription \
-H "Content-Type: application/json" \
-d "{\"prenom\":\"Pauline\",\"nom\":\"Defize\",\"email\":\"$PROF_EMAIL\",\"mot_de_passe\":\"$PROF_PASSWORD\",\"role\":\"professeur\"}")
echo $INSCRIPTION_DOUBLON
echo ""

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
LOGIN_PROF=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d "{\"email\":\"$PROF_EMAIL\",\"mot_de_passe\":\"$PROF_PASSWORD\"}")
echo $LOGIN_PROF
PROF_TOKEN=$(echo $LOGIN_PROF | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion professeur échouée"; exit 1; fi
echo "✅ Token professeur obtenu"
echo ""

# ----- CONNEXION MAUVAIS MOT DE PASSE -----
echo "----- CONNEXION MAUVAIS MOT DE PASSE -----"
LOGIN_MAUVAIS=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d "{\"email\":\"$PROF_EMAIL\",\"mot_de_passe\":\"mauvais_mdp\"}")
echo $LOGIN_MAUVAIS
echo ""

# ----- INSCRIPTION ELEVE -----
echo "----- INSCRIPTION ELEVE -----"
INSCRIPTION_ELEVE=$(curl -s -X POST $BASE_URL/authentification/inscription \
-H "Content-Type: application/json" \
-d "{\"prenom\":\"Cléo\",\"nom\":\"Martin\",\"email\":\"$ELEVE_EMAIL\",\"mot_de_passe\":\"$ELEVE_PASSWORD\",\"role\":\"eleve\"}")
echo $INSCRIPTION_ELEVE
echo ""

# ----- CONNEXION ELEVE -----
echo "----- CONNEXION ELEVE -----"
LOGIN_ELEVE=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d "{\"email\":\"$ELEVE_EMAIL\",\"mot_de_passe\":\"$ELEVE_PASSWORD\"}")
echo $LOGIN_ELEVE
ELEVE_TOKEN=$(echo $LOGIN_ELEVE | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$ELEVE_TOKEN" ]; then echo "❌ Connexion élève échouée"; exit 1; fi
echo "✅ Token élève obtenu"
echo ""

echo "----- TESTS AUTH TERMINÉS ✅ -----"
