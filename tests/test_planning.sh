#!/bin/bash
BASE_URL="http://127.0.0.1:5000/api/v1"

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
LOGIN_PROF=$(curl -s -X POST $BASE_URL/authentification/connexion -H "Content-Type: application/json" \
-d '{"email":"prof@planifpro.com","mot_de_passe":"motdepasse123"}')
PROF_TOKEN=$(echo $LOGIN_PROF | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion professeur échouée"; exit 1; fi
echo "✅ Token professeur obtenu"; echo ""

CLASSES=$(curl -s -X GET $BASE_URL/classes/ -H "Authorization: Bearer $PROF_TOKEN")
CONSERVATOIRE_ID=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['id'] for c in json.load(sys.stdin) if c['nom']=='Conservatoire'),''))")
PRIVE_ID=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['id'] for c in json.load(sys.stdin) if c['nom']=='Cours Privé'),''))")
echo "✅ Conservatoire : $CONSERVATOIRE_ID"
echo "✅ Cours Privé   : $PRIVE_ID"; echo ""

tester_classe() {
    local CLASSE_ID=$1 NOM=$2 AVEC_ERREURS=$3
    echo "=============================================="
    echo "   CLASSE : $NOM"
    echo "=============================================="

    # ----- DUREES (30/45/50/60) -----
    echo "----- DEFINITION DES DUREES -----"
    local STATUT=$(curl -s -X GET $BASE_URL/voeux/statut/$CLASSE_ID -H "Authorization: Bearer $PROF_TOKEN")
    local ELEVE_IDS=$(echo $STATUT | python3 -c "import sys,json; print(' '.join(sorted({v['eleve_id'] for v in json.load(sys.stdin)})))")
    if [ -z "$ELEVE_IDS" ]; then echo "❌ Aucun vœu (lance test_voeux.sh)"; return; fi
    local DUREES=(30 45 50 60); local i=0
    for EID in $ELEVE_IDS; do
        curl -s -X PUT $BASE_URL/eleves/$EID -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
        -d "{\"classe_id\":\"$CLASSE_ID\",\"duree_minutes\":${DUREES[$(( i % 4 ))]}}" >/dev/null
        echo "Élève ${EID:0:8} -> ${DUREES[$(( i % 4 ))]} min"; i=$((i+1))
    done
    echo ""

    # ----- GENERATION -----
    echo "----- GENERATION -----"
    local PLANNINGS=$(curl -s -X POST $BASE_URL/plannings/generer -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
    -d "{\"classe_id\":\"$CLASSE_ID\"}")
    local PLANNING_IDS=$(echo $PLANNINGS | python3 -c "import sys,json; d=json.load(sys.stdin); print(' '.join(p['id'] for p in d) if isinstance(d,list) else '')")
    if [ -z "$PLANNING_IDS" ]; then echo "❌ Génération échouée : $PLANNINGS"; return; fi
    echo "✅ Propositions : $PLANNING_IDS"; echo ""

    # ----- VERIF DES 3 PROPOSITIONS -----
    local NB=$(echo $ELEVE_IDS | wc -w)
    for PID in $PLANNING_IDS; do
        echo "----- CRENEAUX PROPOSITION ($PID) -----"
        curl -s -X GET $BASE_URL/plannings/$PID/creneaux -H "Authorization: Bearer $PROF_TOKEN" | python3 -c "
import sys, json
c = json.load(sys.stdin)
places = {x['eleve_id'] for x in c if x.get('eleve_id')}
print(f'{len(c)} créneaux, {len(places)} élèves placés (attendu : $NB)')
for x in sorted(c, key=lambda x: (x['jour'], x['heure_debut'])):
    eid = (x['eleve_id'] or 'VIDE')[:8]
    print(f\"  {x['jour']:10} {x['heure_debut']}-{x['heure_fin']}  {eid}\")"
        echo ""
    done

    local P1=$(echo $PLANNING_IDS | cut -d' ' -f1)
    local P2=$(echo $PLANNING_IDS | cut -d' ' -f2)

    # ----- CAS D'ERREUR (une seule fois) -----
    if [ "$AVEC_ERREURS" = "oui" ]; then
        echo "----- CAS D'ERREUR -----"
        local EL=$(curl -s -X POST $BASE_URL/authentification/connexion -H "Content-Type: application/json" \
        -d '{"email":"eleve.conservatoire.1@planifpro.com","mot_de_passe":"motdepasse123"}' \
        | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
        echo "- Sélection par un élève (403) :"; curl -s -X PUT $BASE_URL/plannings/$P1/selectionner -H "Authorization: Bearer $EL"; echo ""; echo ""
        echo "- Sélection inexistant (404) :"; curl -s -X PUT $BASE_URL/plannings/id-bidon/selectionner -H "Authorization: Bearer $PROF_TOKEN"; echo ""; echo ""
        echo "- Modification par un élève (403) :"; curl -s -X PUT $BASE_URL/plannings/$P1/modifier -H "Authorization: Bearer $EL"; echo ""; echo ""
        echo "- Validation par un élève (403) :"; curl -s -X PUT $BASE_URL/plannings/valider -H "Authorization: Bearer $EL" -H "Content-Type: application/json" -d "{\"planning_id\":\"$P1\"}"; echo ""; echo ""
        echo "- Validation inexistant (404) :"; curl -s -X PUT $BASE_URL/plannings/valider -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d '{"planning_id":"id-bidon"}'; echo ""; echo ""
        echo "- Détail inexistant (404) :"; curl -s -X GET $BASE_URL/plannings/id-bidon -H "Authorization: Bearer $PROF_TOKEN"; echo ""; echo ""
    fi

    # ----- SELECTION / MODIFICATION / VALIDATION -----
    echo "----- SELECTION / MODIFICATION / VALIDATION -----"
    echo "- Sélection P1 (200) :"; curl -s -X PUT $BASE_URL/plannings/$P1/selectionner -H "Authorization: Bearer $PROF_TOKEN"; echo ""; echo ""
    echo "- Re-sélection P1 (409) :"; curl -s -X PUT $BASE_URL/plannings/$P1/selectionner -H "Authorization: Bearer $PROF_TOKEN"; echo ""; echo ""
    echo "- Modification P1 (200) :"; curl -s -X PUT $BASE_URL/plannings/$P1/modifier -H "Authorization: Bearer $PROF_TOKEN"; echo ""; echo ""
    echo "- Validation P1 (200) :"; curl -s -X PUT $BASE_URL/plannings/valider -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "{\"planning_id\":\"$P1\"}"; echo ""; echo ""
    echo "- Validation P2 supprimée (404) :"; curl -s -X PUT $BASE_URL/plannings/valider -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d "{\"planning_id\":\"$P2\"}"; echo ""; echo ""
    echo "- Confirmation activer (200) :"; curl -s -X PUT $BASE_URL/plannings/$P1/confirmation -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d '{"confirmation":true}'; echo ""; echo ""
    echo "- Confirmation désactiver (200) :"; curl -s -X PUT $BASE_URL/plannings/$P1/confirmation -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" -d '{"confirmation":false}'; echo ""; echo ""
}

tester_classe "$CONSERVATOIRE_ID" "Conservatoire" "oui"
tester_classe "$PRIVE_ID"         "Cours Privé"   "non"

# ----- PLANNING GLOBAL PROF -----
echo "----- PLANNING GLOBAL PROF (attendu : 200) -----"
curl -s -X GET $BASE_URL/plannings/global -H "Authorization: Bearer $PROF_TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d)} créneaux (attendu : ~20 = 10 Conservatoire + 10 Privé validés)' if isinstance(d,list) else d)"
echo ""

# ----- PLANNING GLOBAL ELEVE -----
echo "----- PLANNING GLOBAL ELEVE (attendu : 200) -----"
EL1=$(curl -s -X POST $BASE_URL/authentification/connexion -H "Content-Type: application/json" \
-d '{"email":"eleve.conservatoire.1@planifpro.com","mot_de_passe":"motdepasse123"}' \
| python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
curl -s -X GET $BASE_URL/plannings/global -H "Authorization: Bearer $EL1" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d)} créneau(x) (attendu : 1, son créneau validé)' if isinstance(d,list) else d)"
echo ""

echo "----- TESTS PLANNING (FLUX COMPLET) TERMINÉS ✅ -----"
