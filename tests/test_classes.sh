#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
LOGIN_PROF=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d '{"email":"prof@planifpro.com","mot_de_passe":"motdepasse123"}')
PROF_TOKEN=$(echo $LOGIN_PROF | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion professeur échouée"; exit 1; fi
echo "✅ Token professeur obtenu"
echo ""

# ----- CREATION CLASSE CONSERVATOIRE -----
echo "----- CREATION CLASSE CONSERVATOIRE -----"
CREATE_C1=$(curl -s -X POST $BASE_URL/classes/ \
-H "Authorization: Bearer $PROF_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "nom": "Conservatoire",
    "date_debut": "2026-09-01",
    "date_fin": "2027-06-30",
    "jours_horaires": {
        "mercredi": {"debut": "10:00", "fin": "13:30"},
        "jeudi": {"debut": "15:00", "fin": "20:30"},
        "vendredi": {"debut": "15:00", "fin": "20:30"}
    },
    "nombre_propositions": 3,
    "nombre_voeux_requis": 3,
    "nombre_jours_min": 2
}')
echo $CREATE_C1
CLASSE_C1_ID=$(echo $CREATE_C1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
if [ -z "$CLASSE_C1_ID" ]; then echo "❌ Création classe Conservatoire échouée"; exit 1; fi
CODE_C1=$(echo $CREATE_C1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('code_classe',''))")
echo "✅ Classe Conservatoire créée : $CLASSE_C1_ID (code: $CODE_C1)"
echo ""

# ----- CREATION CLASSE PRIVEE -----
echo "----- CREATION CLASSE PRIVEE -----"
CREATE_C2=$(curl -s -X POST $BASE_URL/classes/ \
-H "Authorization: Bearer $PROF_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "nom": "Cours Privé",
    "date_debut": "2026-09-01",
    "date_fin": "2027-06-30",
    "jours_horaires": {
        "lundi": {"debut": "09:00", "fin": "20:00"},
        "mardi": {"debut": "09:00", "fin": "20:00"},
        "mercredi": {"debut": "09:00", "fin": "20:00"},
        "jeudi": {"debut": "09:00", "fin": "20:00"},
        "vendredi": {"debut": "09:00", "fin": "20:00"}
    },
    "nombre_propositions": 3,
    "nombre_voeux_requis": 3,
    "nombre_jours_min": 2
}')
echo $CREATE_C2
CLASSE_C2_ID=$(echo $CREATE_C2 | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
if [ -z "$CLASSE_C2_ID" ]; then echo "❌ Création classe Privée échouée"; exit 1; fi
CODE_C2=$(echo $CREATE_C2 | python3 -c "import sys,json; print(json.load(sys.stdin).get('code_classe',''))")
echo "✅ Classe Privée créée : $CLASSE_C2_ID (code: $CODE_C2)"
echo ""

# ----- ELEVES CONSERVATOIRE REJOIGNENT LA CLASSE -----
echo "----- ELEVES CONSERVATOIRE REJOIGNENT LA CLASSE -----"
for i in {1..10}; do
    LOGIN=$(curl -s -X POST $BASE_URL/authentification/connexion \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"eleve.conservatoire.$i@planifpro.com\",\"mot_de_passe\":\"motdepasse123\"}")
    TOKEN=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

    REJOINDRE=$(curl -s -X POST $BASE_URL/professeurs/rejoindre \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"code_unique\":\"$CODE_C1\"}")
    echo "Élève Conservatoire-$i : $REJOINDRE"
done
echo ""

# ----- ELEVES PRIVEE REJOIGNENT LA CLASSE -----
echo "----- ELEVES PRIVEE REJOIGNENT LA CLASSE -----"
for i in {1..10}; do
    LOGIN=$(curl -s -X POST $BASE_URL/authentification/connexion \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"eleve.privee.$i@planifpro.com\",\"mot_de_passe\":\"motdepasse123\"}")
    TOKEN=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

    REJOINDRE=$(curl -s -X POST $BASE_URL/professeurs/rejoindre \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"code_unique\":\"$CODE_C2\"}")
    echo "Élève Privée-$i : $REJOINDRE"
done
echo ""

echo "CLASSE_C1_ID=$CLASSE_C1_ID"
echo "CLASSE_C2_ID=$CLASSE_C2_ID"
echo "PROF_TOKEN=$PROF_TOKEN"
echo "----- TESTS CLASSES TERMINÉS ✅ -----"
