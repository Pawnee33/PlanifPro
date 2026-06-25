#!/bin/bash
BASE_URL="http://127.0.0.1:5000/api/v1"
CODE_CHANTECLER="7CBAC995"

# 3 élèves de test pour Chantecler
PRENOMS=("Sophie" "Adam" "Lina")
NOMS=("Durand" "Faure" "Roussel")

for i in {1..3}; do
  idx=$((i-1))
  PRENOM=${PRENOMS[$idx]}
  NOM=${NOMS[$idx]}
  EMAIL="eleve.chantecler.$i@planifpro.com"

  # 1) Inscription de l'élève
  curl -s -X POST $BASE_URL/authentification/inscription \
    -H "Content-Type: application/json" \
    -d "{\"prenom\":\"$PRENOM\",\"nom\":\"$NOM\",\"email\":\"$EMAIL\",\"mot_de_passe\":\"motdepasse123\",\"role\":\"eleve\"}" > /dev/null

  # 2) Connexion → récupérer le token de l'élève
  LOGIN=$(curl -s -X POST $BASE_URL/authentification/connexion \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"mot_de_passe\":\"motdepasse123\"}")
  TOKEN=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

  # 3) Rejoindre Chantecler avec le code
  REJOINDRE=$(curl -s -X POST $BASE_URL/classes/rejoindre \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"code_unique\":\"$CODE_CHANTECLER\"}")
  echo "$PRENOM $NOM → $REJOINDRE"
done
