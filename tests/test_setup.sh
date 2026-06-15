#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

# ----- INSCRIPTION PROFESSEUR -----
echo "----- INSCRIPTION PROFESSEUR -----"
INSCRIPTION_PROF=$(curl -s -X POST $BASE_URL/authentification/inscription \
-H "Content-Type: application/json" \
-d '{"prenom":"Pauline","nom":"Defize","email":"prof@planifpro.com","mot_de_passe":"motdepasse123","role":"professeur"}')
echo $INSCRIPTION_PROF

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
LOGIN_PROF=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d '{"email":"prof@planifpro.com","mot_de_passe":"motdepasse123"}')
PROF_TOKEN=$(echo $LOGIN_PROF | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion professeur échouée"; exit 1; fi
echo "✅ Token professeur obtenu"
echo ""

# ----- INSCRIPTION 10 ELEVES CLASSE Conservatoire -----
echo "----- INSCRIPTION ELEVES CLASSE Conservatoire -----"
PRENOMS_C1=("Emma" "Lucas" "Léa" "Noah" "Chloé" "Louis" "Manon" "Hugo" "Camille" "Nathan")
NOMS_C1=("Bernard" "Petit" "Dubois" "Thomas" "Robert" "Richard" "Simon" "Laurent" "Michel" "Garcia")

for i in {1..10}; do
    idx=$((i-1))
    PRENOM=${PRENOMS_C1[$idx]}
    NOM=${NOMS_C1[$idx]}
    INSCRIPTION=$(curl -s -X POST $BASE_URL/authentification/inscription \
    -H "Content-Type: application/json" \
    -d "{\"prenom\":\"$PRENOM\",\"nom\":\"$NOM\",\"email\":\"eleve.conservatoire.$i@planifpro.com\",\"mot_de_passe\":\"motdepasse123\",\"role\":\"eleve\"}")
    echo "Élève Conservatoire-$i ($PRENOM $NOM) : $INSCRIPTION"
done
echo ""

# ----- INSCRIPTION 10 ELEVES CLASSE Privée -----
echo "----- INSCRIPTION ELEVES CLASSE Privée -----"
PRENOMS_C2=("Inès" "Théo" "Jade" "Mathis" "Lola" "Arthur" "Zoé" "Raphaël" "Alice" "Tom")
NOMS_C2=("Martin" "Leroy" "Moreau" "Lefebvre" "Roux" "David" "Bertrand" "Morel" "Fournier" "Girard")

for i in {1..10}; do
    idx=$((i-1))
    PRENOM=${PRENOMS_C2[$idx]}
    NOM=${NOMS_C2[$idx]}
    INSCRIPTION=$(curl -s -X POST $BASE_URL/authentification/inscription \
    -H "Content-Type: application/json" \
    -d "{\"prenom\":\"$PRENOM\",\"nom\":\"$NOM\",\"email\":\"eleve.privee.$i@planifpro.com\",\"mot_de_passe\":\"motdepasse123\",\"role\":\"eleve\"}")
    echo "Élève Privée-$i ($PRENOM $NOM) : $INSCRIPTION"
done
echo ""

echo "PROF_TOKEN=$PROF_TOKEN"
echo "----- SETUP TERMINÉ ✅ -----"
