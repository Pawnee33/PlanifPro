#!/bin/bash
BASE_URL="http://127.0.0.1:5000/api/v1"
FAKE_UUID="00000000-0000-0000-0000-000000000000"

# Vérifie qu'un code HTTP correspond à l'attendu
verifier() {
    local attendu=$1; local code=$2; local libelle=$3
    if [ "$code" = "$attendu" ]; then
        echo "✅ $libelle ($code)"
    else
        echo "❌ $libelle (attendu $attendu, reçu $code)"
    fi
}

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
LOGIN_PROF=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d '{"email":"prof@planifpro.com","mot_de_passe":"motdepasse123"}')
PROF_TOKEN=$(echo $LOGIN_PROF | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion professeur échouée"; exit 1; fi
echo "✅ Token professeur obtenu"; echo ""

# ----- RECUPERATION D'UN CRENEAU VALIDE (planning global) -----
echo "----- RECUPERATION D'UN CRENEAU VALIDE -----"
GLOBAL=$(curl -s -X GET $BASE_URL/plannings/global -H "Authorization: Bearer $PROF_TOKEN")
read CRENEAU_ID ELEVE_ID <<< "$(echo $GLOBAL | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    d = []
c = next((x for x in d if isinstance(x, dict) and x.get('eleve_id')), None) if isinstance(d, list) else None
print(c['id'], c['eleve_id']) if c else print('', '')
")"
if [ -z "$CRENEAU_ID" ]; then echo "❌ Aucun créneau validé trouvé (lance test_planning + validation)"; exit 1; fi
echo "✅ Créneau ${CRENEAU_ID:0:8} (élève ${ELEVE_ID:0:8})"; echo ""

# ----- EMAIL DE L'ELEVE (pour la lecture côté élève) -----
ELEVE_EMAIL=$(curl -s -X GET $BASE_URL/eleves/$ELEVE_ID -H "Authorization: Bearer $PROF_TOKEN" \
| python3 -c "import sys,json; print(json.load(sys.stdin).get('email',''))")
echo "Élève ciblé : $ELEVE_EMAIL"; echo ""

# ----- CREATION OBJECTIF (NOMINAL) -----
echo "----- CREATION OBJECTIF -----"
RESP=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/objectifs/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"eleve_id\":\"$ELEVE_ID\",\"creneau_id\":\"$CRENEAU_ID\",\"contenu\":\"Travailler la gamme de Do majeur\",\"conseils\":\"Lentement au métronome à 60 bpm\"}")
CODE=$(echo "$RESP" | tail -n1); BODY=$(echo "$RESP" | sed '$d')
verifier 201 "$CODE" "POST /objectifs (prof écrit l'objectif du prochain cours)"
OBJECTIF_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo ""

# ----- LECTURES COTE PROFESSEUR -----
echo "----- LECTURES PROFESSEUR -----"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/objectifs/ -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "GET /objectifs (liste prof)"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/objectifs/creneau/$CRENEAU_ID -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "GET /objectifs/creneau/<id>"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/objectifs/eleve/$ELEVE_ID -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "GET /objectifs/eleve/<id>"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/objectifs/$OBJECTIF_ID -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "GET /objectifs/<id> (détail)"
echo ""

# ----- MODIFICATION -----
echo "----- MODIFICATION OBJECTIF -----"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $BASE_URL/objectifs/$OBJECTIF_ID \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"eleve_id\":\"$ELEVE_ID\",\"creneau_id\":\"$CRENEAU_ID\",\"contenu\":\"Gamme de Do majeur + arpèges\",\"conseils\":\"Métronome à 72 bpm\"}")
verifier 200 "$CODE" "PUT /objectifs/<id>"
echo ""

# ----- LECTURE COTE ELEVE -----
echo "----- LECTURE COTE ELEVE -----"
LOGIN_ELEVE=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d "{\"email\":\"$ELEVE_EMAIL\",\"mot_de_passe\":\"motdepasse123\"}")
ELEVE_TOKEN=$(echo $LOGIN_ELEVE | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$ELEVE_TOKEN" ]; then echo "❌ Connexion élève échouée"; exit 1; fi
RESP=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/objectifs/ -H "Authorization: Bearer $ELEVE_TOKEN")
CODE=$(echo "$RESP" | tail -n1); BODY=$(echo "$RESP" | sed '$d')
verifier 200 "$CODE" "GET /objectifs (l'élève lit ses objectifs)"
echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  {len(d)} objectif(s) visible(s) par l élève')" 2>/dev/null
echo ""

# ----- CAS D'ERREUR -----
echo "----- CAS D'ERREUR -----"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/objectifs/ \
-H "Authorization: Bearer $ELEVE_TOKEN" -H "Content-Type: application/json" \
-d "{\"eleve_id\":\"$ELEVE_ID\",\"creneau_id\":\"$CRENEAU_ID\",\"contenu\":\"x\",\"conseils\":\"y\"}")
verifier 403 "$CODE" "POST /objectifs en tant qu'élève (refusé)"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/objectifs/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"eleve_id\":\"$ELEVE_ID\",\"creneau_id\":\"$FAKE_UUID\",\"contenu\":\"x\",\"conseils\":\"y\"}")
verifier 404 "$CODE" "POST /objectifs avec créneau inexistant"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/objectifs/$FAKE_UUID -H "Authorization: Bearer $PROF_TOKEN")
verifier 404 "$CODE" "GET /objectifs/<inexistant>"
echo ""

# ----- SUPPRESSION -----
echo "----- SUPPRESSION OBJECTIF -----"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE $BASE_URL/objectifs/$OBJECTIF_ID -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "DELETE /objectifs/<id>"
echo ""

echo "----- TESTS OBJECTIFS TERMINÉS ✅ -----"
