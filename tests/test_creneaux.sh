#!/bin/bash
BASE_URL="http://127.0.0.1:5000/api/v1"

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
PROF_TOKEN=$(curl -s -X POST $BASE_URL/authentification/connexion -H "Content-Type: application/json" \
-d '{"email":"prof@planifpro.com","mot_de_passe":"motdepasse123"}' \
| python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion prof échouée"; exit 1; fi
echo "✅ Token prof obtenu"; echo ""

# ----- CLASSE + PERIODE -----
CLASSES=$(curl -s -X GET $BASE_URL/classes/ -H "Authorization: Bearer $PROF_TOKEN")
CONSERVATOIRE_ID=$(echo "$CLASSES" | python3 -c "import sys,json; print(next((c['id'] for c in json.load(sys.stdin) if c['nom']=='Conservatoire'),''))")
DATE_DEBUT=$(echo "$CLASSES" | python3 -c "import sys,json; print(next((c['date_debut'][:10] for c in json.load(sys.stdin) if c['nom']=='Conservatoire'),''))")
DJ=$(python3 -c "from datetime import date,timedelta; print(date.fromisoformat('$DATE_DEBUT')+timedelta(days=30))")
FJ=$(python3 -c "from datetime import date,timedelta; print(date.fromisoformat('$DATE_DEBUT')+timedelta(days=37))")

# ----- RECUPERATION DES CRENEAUX VALIDES (Conservatoire) -----
CRJSON=$(curl -s -X GET $BASE_URL/creneaux/ -H "Authorization: Bearer $PROF_TOKEN")
get() { echo "$CRJSON" | python3 -c "import sys,json; cs=[c for c in json.load(sys.stdin) if c['classe_id']=='$CONSERVATOIRE_ID']; $1"; }
CR1=$(get "print(cs[0]['id'])"); PLANNING_ID=$(get "print(cs[0]['planning_id'])")
CR2=$(get "print(cs[1]['id'])"); CR3=$(get "print(cs[2]['id'])")
if [ -z "$CR1" ] || [ -z "$CR2" ] || [ -z "$CR3" ]; then echo "❌ Créneaux validés introuvables (lance test_planning.sh)"; exit 1; fi
echo "✅ Créneaux : CR1=${CR1:0:8} CR2=${CR2:0:8} CR3=${CR3:0:8} (planning ${PLANNING_ID:0:8})"; echo ""

# ----- LECTURE -----
echo "----- LECTURE -----"
echo "détail CR1          : $(curl -s -o /dev/null -w '%{http_code}' -X GET $BASE_URL/creneaux/$CR1 -H "Authorization: Bearer $PROF_TOKEN") (attendu 200)"
echo "détail id bidon     : $(curl -s -o /dev/null -w '%{http_code}' -X GET $BASE_URL/creneaux/id-bidon -H "Authorization: Bearer $PROF_TOKEN") (attendu 404)"
echo ""

# ----- DEPLACER -----
echo "----- DEPLACER -----"
EL=$(curl -s -X POST $BASE_URL/authentification/connexion -H "Content-Type: application/json" \
-d '{"email":"eleve.conservatoire.1@planifpro.com","mot_de_passe":"motdepasse123"}' \
| python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
MOVE='{"jour":"dimanche","heure_debut":"11:00","heure_fin":"11:30"}'
echo "déplacer par élève  : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/$CR1/deplacer -H "Authorization: Bearer $EL" -H "Content-Type: application/json" -d "$MOVE") (attendu 403)"
echo "déplacer CR1 (prof) : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/$CR1/deplacer -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "$MOVE") (attendu 200, pas de check chevauchement)"
echo ""

# ----- ECHANGER -----
echo "----- ECHANGER -----"
echo "échanger CR2/CR3    : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/echanger -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "{\"creneau_id_1\":\"$CR2\",\"creneau_id_2\":\"$CR3\"}") (attendu 200)"
echo "échanger id bidon   : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/echanger -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "{\"creneau_id_1\":\"$CR2\",\"creneau_id_2\":\"id-bidon\"}") (attendu 404)"
echo ""

# ----- AJOUTER UN ELEVE -----
echo "----- AJOUTER UN ELEVE -----"
ELEVE_ID=$(get "print(cs[0]['eleve_id'])")
CLASSE_ID=$(get "print(cs[0]['classe_id'])")
TYPE=$(get "print(cs[0]['type'])")
BODY="{\"planning_id\":\"$PLANNING_ID\",\"eleve_id\":\"$ELEVE_ID\",\"classe_id\":\"$CLASSE_ID\",\"type\":\"$TYPE\",\"jour\":\"samedi\",\"heure_debut\":\"08:00\",\"heure_fin\":\"08:30\",\"duree_minutes\":30,\"date_debut\":\"$DJ\",\"date_fin\":\"$FJ\"}"
echo "ajout (samedi 08:00): $(curl -s -o /dev/null -w '%{http_code}' -X POST $BASE_URL/creneaux/ -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "$BODY") (attendu 201)"
echo "ré-ajout même slot  : $(curl -s -o /dev/null -w '%{http_code}' -X POST $BASE_URL/creneaux/ -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "$BODY") (attendu 409)"
echo "ajout par élève     : $(curl -s -o /dev/null -w '%{http_code}' -X POST $BASE_URL/creneaux/ -H "Authorization: Bearer $EL" -H "Content-Type: application/json" -d "$BODY") (attendu 403)"
echo "ajout planning bidon: $(curl -s -o /dev/null -w '%{http_code}' -X POST $BASE_URL/creneaux/ -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "{\"planning_id\":\"id-bidon\",\"eleve_id\":\"$ELEVE_ID\",\"classe_id\":\"$CLASSE_ID\",\"type\":\"$TYPE\",\"jour\":\"samedi\",\"heure_debut\":\"09:00\",\"heure_fin\":\"09:30\",\"duree_minutes\":30}") (attendu 404)"
VIS=$(curl -s -X GET $BASE_URL/plannings/global -H "Authorization: Bearer $PROF_TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print('OUI' if isinstance(d,list) and any(c['jour']=='samedi' for c in d) else 'NON')")
echo "samedi visible dashboard : $VIS (attendu OUI)"
echo ""

# ----- MODIFIER (scope) -----
echo "----- MODIFIER (scope) -----"
echo "scope invalide      : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/$CR1 -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d '{"scope":"bidon"}') (attendu 400)"
echo "ce_jour sans dates  : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/$CR1 -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d '{"scope":"ce_jour"}') (attendu 400)"
echo "ce_jour ($DJ)       : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/$CR1 -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "{\"scope\":\"ce_jour\",\"debut_jour\":\"$DJ\"}") (attendu 200)"
echo "plusieurs_jours     : $(curl -s -o /dev/null -w '%{http_code}' -X PUT $BASE_URL/creneaux/$CR1 -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "{\"scope\":\"plusieurs_jours\",\"debut_jour\":\"$DJ\",\"fin_jour\":\"$FJ\"}") (attendu 200)"
echo ""

# ----- SUPPRIMER (scope) -----
echo "----- SUPPRIMER (scope) -----"
echo "scope invalide      : $(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$BASE_URL/creneaux/$CR3?scope=bidon" -H "Authorization: Bearer $PROF_TOKEN") (attendu 400)"
echo "ce_jour sans dates  : $(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$BASE_URL/creneaux/$CR3?scope=ce_jour" -H "Authorization: Bearer $PROF_TOKEN") (attendu 400)"
echo "toute_la_periode    : $(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$BASE_URL/creneaux/$CR3?scope=toute_la_periode" -H "Authorization: Bearer $PROF_TOKEN") (attendu 200)"
echo "re-suppression      : $(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$BASE_URL/creneaux/$CR3?scope=toute_la_periode" -H "Authorization: Bearer $PROF_TOKEN") (attendu 404)"
echo ""

echo "----- TESTS CRENEAUX TERMINÉS ✅ -----"
