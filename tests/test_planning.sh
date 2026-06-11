#!/bin/bash
BASE_URL="http://127.0.0.1:5000/api/v1"

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
LOGIN_PROF=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d '{"email":"prof@planifpro.com","mot_de_passe":"motdepasse123"}')
PROF_TOKEN=$(echo $LOGIN_PROF | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion professeur échouée"; exit 1; fi
echo "✅ Token professeur obtenu"; echo ""

CLASSES=$(curl -s -X GET $BASE_URL/classes/ -H "Authorization: Bearer $PROF_TOKEN")
CONSERVATOIRE_ID=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['id'] for c in json.load(sys.stdin) if c['nom']=='Conservatoire'),''))")
PRIVE_ID=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['id'] for c in json.load(sys.stdin) if c['nom']=='Cours Privé'),''))")

tester_classe() {
    local CLASSE_ID=$1
    local NOM=$2
    echo "=============================================="
    echo "   CLASSE : $NOM"
    echo "=============================================="

    # ----- Durées variées (30/45/60) -----
    echo "----- DEFINITION DES DUREES -----"
    local STATUT=$(curl -s -X GET $BASE_URL/voeux/statut/$CLASSE_ID -H "Authorization: Bearer $PROF_TOKEN")
    local ELEVE_IDS=$(echo $STATUT | python3 -c "import sys,json; print(' '.join(sorted({v['eleve_id'] for v in json.load(sys.stdin)})))")
    if [ -z "$ELEVE_IDS" ]; then echo "❌ Aucun vœu (lance test_voeux.sh)"; return; fi
    local i=0
    for EID in $ELEVE_IDS; do
        local DUREE=$(( 30 + (i % 3) * 15 ))
        curl -s -X PUT $BASE_URL/eleves/$EID -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
        -d "{\"classe_id\":\"$CLASSE_ID\",\"duree_minutes\":$DUREE}" >/dev/null
        echo "Élève ${EID:0:8} -> $DUREE min"
        i=$((i+1))
    done
    echo ""

    # ----- Génération -----
    echo "----- GENERATION -----"
    local PLANNINGS=$(curl -s -X POST $BASE_URL/plannings/generer -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
    -d "{\"classe_id\":\"$CLASSE_ID\"}")
    echo $PLANNINGS
    local PLANNING_IDS=$(echo $PLANNINGS | python3 -c "import sys,json; d=json.load(sys.stdin); print(' '.join(p['id'] for p in d) if isinstance(d,list) else '')")
    if [ -z "$PLANNING_IDS" ]; then echo "❌ Génération échouée (déjà généré ?)"; return; fi
    echo ""

    # ----- Vérification des créneaux par proposition -----
    local NB=$(echo $ELEVE_IDS | wc -w)
    for PID in $PLANNING_IDS; do
        echo "----- CRENEAUX PROPOSITION ($PID) -----"
        local CRENEAUX=$(curl -s -X GET $BASE_URL/plannings/$PID/creneaux -H "Authorization: Bearer $PROF_TOKEN")
        echo $CRENEAUX | python3 -c "
import sys, json
c = json.load(sys.stdin)
places = {x['eleve_id'] for x in c if x.get('eleve_id')}
print(f'{len(c)} créneaux, {len(places)} élèves placés (attendu : $NB)')
for x in sorted(c, key=lambda x: (x['jour'], x['heure_debut'])):
    eid = (x['eleve_id'] or 'VIDE')[:8]
    print(f\"  {x['jour']:10} {x['heure_debut']}-{x['heure_fin']}  {eid}\")
"
        echo ""
    done
}

tester_classe "$CONSERVATOIRE_ID" "Conservatoire"
tester_classe "$PRIVE_ID" "Cours Privé"

echo "----- TESTS PLANNING TERMINÉS ✅ -----"
