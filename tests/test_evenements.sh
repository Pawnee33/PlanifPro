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

# ----- RECUPERATION CLASSE + ELEVE (pour les destinataires) -----
echo "----- RECUPERATION CLASSE + ELEVE -----"
CLASSE_ID=$(curl -s -X GET $BASE_URL/classes/ -H "Authorization: Bearer $PROF_TOKEN" \
| python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['id'] if d else '')")
ELEVES=$(curl -s -X GET $BASE_URL/eleves/ -H "Authorization: Bearer $PROF_TOKEN")
ELEVE_ID=$(echo "$ELEVES" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['id'] if d else '')")
ELEVE_EMAIL=$(echo "$ELEVES" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0].get('email','') if d else '')")
if [ -z "$CLASSE_ID" ] || [ -z "$ELEVE_ID" ]; then echo "❌ Classe ou élève introuvable (lance test_classes)"; exit 1; fi
echo "✅ Classe ${CLASSE_ID:0:8} / élève ${ELEVE_ID:0:8} ($ELEVE_EMAIL)"; echo ""

# ----- CREATION EVENEMENTS (1 PAR TYPE DE DESTINATAIRES) -----
echo "----- CREATION EVENEMENTS -----"
# type toutes_classes (on garde cet ID pour détail / modif / suppression)
RESP=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"Audition de fin d annee\",\"description\":\"Audition au conservatoire\",\"date_heure\":\"2026-06-28T18:00:00\",\"destinataires\":{\"type\":\"toutes_classes\"}}")
CODE=$(echo "$RESP" | tail -n1); BODY=$(echo "$RESP" | sed '$d')
verifier 201 "$CODE" "POST /evenements (toutes_classes)"
EVENEMENT_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# type classes
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"Repetition par classe\",\"description\":\"Repetition\",\"date_heure\":\"2026-06-20T17:00:00\",\"destinataires\":{\"type\":\"classes\",\"ids\":[\"$CLASSE_ID\"]}}")
verifier 201 "$CODE" "POST /evenements (classes)"

# type eleves
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"Cours particulier supplementaire\",\"description\":\"Rattrapage\",\"date_heure\":\"2026-06-22T15:00:00\",\"destinataires\":{\"type\":\"eleves\",\"ids\":[\"$ELEVE_ID\"]}}")
verifier 201 "$CODE" "POST /evenements (eleves)"

# type mixte
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"Concert de classe\",\"description\":\"Concert\",\"date_heure\":\"2026-06-30T19:00:00\",\"destinataires\":{\"type\":\"mixte\",\"classes_ids\":[\"$CLASSE_ID\"],\"eleves_ids\":[\"$ELEVE_ID\"]}}")
verifier 201 "$CODE" "POST /evenements (mixte)"
echo ""

# ----- LECTURES COTE PROFESSEUR -----
echo "----- LECTURES PROFESSEUR -----"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/evenements/ -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "GET /evenements (liste prof)"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/evenements/$EVENEMENT_ID -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "GET /evenements/<id> (détail)"
echo ""

# ----- MODIFICATION -----
echo "----- MODIFICATION EVENEMENT -----"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $BASE_URL/evenements/$EVENEMENT_ID \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"Audition de fin d annee (reportee)\",\"description\":\"Nouvelle date\",\"date_heure\":\"2026-07-05T18:00:00\",\"destinataires\":{\"type\":\"toutes_classes\"}}")
verifier 200 "$CODE" "PUT /evenements/<id>"
echo ""

# ----- LECTURE COTE ELEVE -----
echo "----- LECTURE COTE ELEVE -----"
LOGIN_ELEVE=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d "{\"email\":\"$ELEVE_EMAIL\",\"mot_de_passe\":\"motdepasse123\"}")
ELEVE_TOKEN=$(echo $LOGIN_ELEVE | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$ELEVE_TOKEN" ]; then echo "❌ Connexion élève échouée"; exit 1; fi
RESP=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/evenements/ -H "Authorization: Bearer $ELEVE_TOKEN")
CODE=$(echo "$RESP" | tail -n1); BODY=$(echo "$RESP" | sed '$d')
verifier 200 "$CODE" "GET /evenements (l'élève lit ses événements)"
echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  {len(d)} événement(s) visible(s) par l élève')" 2>/dev/null
echo ""

# ----- CAS D'ERREUR -----
echo "----- CAS D'ERREUR -----"
# 400 : titre vide
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"\",\"description\":\"x\",\"date_heure\":\"2026-06-28T18:00:00\",\"destinataires\":{\"type\":\"toutes_classes\"}}")
verifier 400 "$CODE" "POST /evenements titre vide"
# 400 : titre trop long (> 50 caractères)
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\",\"description\":\"x\",\"date_heure\":\"2026-06-28T18:00:00\",\"destinataires\":{\"type\":\"toutes_classes\"}}")
verifier 400 "$CODE" "POST /evenements titre > 50 car."
# 400 : destinataires vide
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"Test\",\"description\":\"x\",\"date_heure\":\"2026-06-28T18:00:00\",\"destinataires\":{}}")
verifier 400 "$CODE" "POST /evenements destinataires vide"
# 403 : élève tente de créer
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/evenements/ \
-H "Authorization: Bearer $ELEVE_TOKEN" -H "Content-Type: application/json" \
-d "{\"titre\":\"Test\",\"description\":\"x\",\"date_heure\":\"2026-06-28T18:00:00\",\"destinataires\":{\"type\":\"toutes_classes\"}}")
verifier 403 "$CODE" "POST /evenements en tant qu'élève (refusé)"
# 404 : événement inexistant
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/evenements/$FAKE_UUID -H "Authorization: Bearer $PROF_TOKEN")
verifier 404 "$CODE" "GET /evenements/<inexistant>"
echo ""

# ----- SUPPRESSION -----
echo "----- SUPPRESSION EVENEMENT -----"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE $BASE_URL/evenements/$EVENEMENT_ID -H "Authorization: Bearer $PROF_TOKEN")
verifier 200 "$CODE" "DELETE /evenements/<id>"
echo ""

echo "----- TESTS EVENEMENTS TERMINÉS ✅ -----"
