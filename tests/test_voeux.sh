#!/bin/bash
BASE_URL="http://127.0.0.1:5000/api/v1"

# Génère les vœux à partir du jours_horaires réel + du nombre de vœux requis
# (privé = 1 horaire convenu ; public = 3 vœux, 3 jours ou 2+1)
gen_voeux() {
    python3 -c "
import json, sys
jh = json.loads(sys.argv[1]); i = int(sys.argv[2]); nb = int(sys.argv[3])
jours = list(jh.keys()); n = len(jours)

def heure(jour, offset):
    d = int(jh[jour]['debut'].split(':')[0])
    f = int(jh[jour]['fin'].split(':')[0])
    h = d + (offset % max(1, f - d - 1))
    return f'{h:02d}:00'

if nb <= 1:
    # cours privé : un seul horaire convenu
    j = jours[(i-1) % n]
    voeux = {'voeu1': {'jour': j, 'heure': heure(j, i)}}
elif i % 2 == 0:
    # public : 3 jours différents
    j1 = jours[(i-1) % n]; j2 = jours[i % n]; j3 = jours[(i+1) % n]
    voeux = {
      'voeu1': {'jour': j1, 'heure': heure(j1, i)},
      'voeu2': {'jour': j2, 'heure': heure(j2, i)},
      'voeu3': {'jour': j3, 'heure': heure(j3, i)},
    }
else:
    # public : 2 vœux le même jour + 1 autre jour
    ja = jours[(i-1) % n]; jb = jours[i % n]
    voeux = {
      'voeu1': {'jour': ja, 'heure': heure(ja, i)},
      'voeu2': {'jour': ja, 'heure': heure(ja, i+1)},
      'voeu3': {'jour': jb, 'heure': heure(jb, i)},
    }
print(json.dumps(voeux))
" "$1" "$2" "$3"
}

# ----- CONNEXION PROFESSEUR -----
echo "----- CONNEXION PROFESSEUR -----"
LOGIN_PROF=$(curl -s -X POST $BASE_URL/authentification/connexion \
-H "Content-Type: application/json" \
-d '{"email":"prof@planifpro.com","mot_de_passe":"motdepasse123"}')
PROF_TOKEN=$(echo $LOGIN_PROF | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$PROF_TOKEN" ]; then echo "❌ Connexion professeur échouée"; exit 1; fi
echo "✅ Token professeur obtenu"; echo ""

# ----- RECUPERATION DES CLASSES -----
echo "----- RECUPERATION DES CLASSES -----"
CLASSES=$(curl -s -X GET $BASE_URL/classes/ -H "Authorization: Bearer $PROF_TOKEN")
CONSERVATOIRE_ID=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['id'] for c in json.load(sys.stdin) if c['nom']=='Conservatoire'),''))")
PRIVE_ID=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['id'] for c in json.load(sys.stdin) if c['nom']=='Cours Privé'),''))")
JH_C=$(echo $CLASSES | python3 -c "import sys,json; print(json.dumps(next(c['jours_horaires'] for c in json.load(sys.stdin) if c['nom']=='Conservatoire')))")
JH_P=$(echo $CLASSES | python3 -c "import sys,json; print(json.dumps(next(c['jours_horaires'] for c in json.load(sys.stdin) if c['nom']=='Cours Privé')))")
NB_C=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['nombre_voeux_requis'] for c in json.load(sys.stdin) if c['nom']=='Conservatoire'),3))")
NB_P=$(echo $CLASSES | python3 -c "import sys,json; print(next((c['nombre_voeux_requis'] for c in json.load(sys.stdin) if c['nom']=='Cours Privé'),1))")
if [ -z "$CONSERVATOIRE_ID" ] || [ -z "$PRIVE_ID" ]; then echo "❌ Classe(s) introuvable(s)"; exit 1; fi
echo "✅ Conservatoire : $CONSERVATOIRE_ID (vœux requis : $NB_C)"
echo "✅ Cours Privé   : $PRIVE_ID (vœux requis : $NB_P)"; echo ""

# ----- VOEUX CONSERVATOIRE -----
echo "----- VOEUX CONSERVATOIRE (10 élèves) -----"
for i in {1..10}; do
    LOGIN=$(curl -s -X POST $BASE_URL/authentification/connexion -H "Content-Type: application/json" \
    -d "{\"email\":\"eleve.conservatoire.$i@planifpro.com\",\"mot_de_passe\":\"motdepasse123\"}")
    TOKEN=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
    CREN=$(gen_voeux "$JH_C" "$i" "$NB_C")
    VOEU=$(curl -s -X POST $BASE_URL/voeux/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d "{\"classe_id\":\"$CONSERVATOIRE_ID\",\"creneaux_souhaites\":$CREN}")
    echo "Conservatoire-$i : $VOEU"
    if [ "$i" -eq 1 ]; then
        ELEVE_TOKEN=$TOKEN
        VOEU_ID=$(echo $VOEU | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
        ELEVE_ID=$(echo $VOEU | python3 -c "import sys,json; print(json.load(sys.stdin).get('eleve_id',''))")
    fi
done
echo ""

# ----- VOEUX COURS PRIVÉ -----
echo "----- VOEUX COURS PRIVÉ (10 élèves) -----"
for i in {1..10}; do
    LOGIN=$(curl -s -X POST $BASE_URL/authentification/connexion -H "Content-Type: application/json" \
    -d "{\"email\":\"eleve.privee.$i@planifpro.com\",\"mot_de_passe\":\"motdepasse123\"}")
    TOKEN=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
    CREN=$(gen_voeux "$JH_P" "$i" "$NB_P")
    VOEU=$(curl -s -X POST $BASE_URL/voeux/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d "{\"classe_id\":\"$PRIVE_ID\",\"creneaux_souhaites\":$CREN}")
    echo "Privée-$i : $VOEU"
done
echo ""

# ===== TESTS DES ENDPOINTS (sur Conservatoire) =====
echo "----- SOUMISSION INSUFFISANTE (attendu : 400) -----"
curl -s -X POST $BASE_URL/voeux/ -H "Authorization: Bearer $ELEVE_TOKEN" -H "Content-Type: application/json" \
-d "{\"classe_id\":\"$CONSERVATOIRE_ID\",\"creneaux_souhaites\":{\"voeu1\":{\"jour\":\"jeudi\",\"heure\":\"15:00\"}}}"
echo ""; echo ""

echo "----- SOUMISSION PAR UN PROFESSEUR (attendu : 403) -----"
curl -s -X POST $BASE_URL/voeux/ -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"classe_id\":\"$CONSERVATOIRE_ID\",\"creneaux_souhaites\":{\"voeu1\":{\"jour\":\"mercredi\",\"heure\":\"10:00\"},\"voeu2\":{\"jour\":\"jeudi\",\"heure\":\"15:00\"},\"voeu3\":{\"jour\":\"vendredi\",\"heure\":\"16:00\"}}}"
echo ""; echo ""

echo "----- LISTE DES VOEUX (ELEVE) -----"
curl -s -X GET $BASE_URL/voeux/ -H "Authorization: Bearer $ELEVE_TOKEN"; echo ""; echo ""

echo "----- LISTE DES VOEUX (PROFESSEUR) -----"
curl -s -X GET $BASE_URL/voeux/ -H "Authorization: Bearer $PROF_TOKEN"; echo ""; echo ""

echo "----- STATUT DES VOEUX (PROFESSEUR) -----"
curl -s -X GET $BASE_URL/voeux/statut/$CONSERVATOIRE_ID -H "Authorization: Bearer $PROF_TOKEN"; echo ""; echo ""

echo "----- STATUT DES VOEUX (ELEVE) (attendu : 403) -----"
curl -s -X GET $BASE_URL/voeux/statut/$CONSERVATOIRE_ID -H "Authorization: Bearer $ELEVE_TOKEN"; echo ""; echo ""

echo "----- DETAIL D'UN VOEU -----"
curl -s -X GET $BASE_URL/voeux/$VOEU_ID -H "Authorization: Bearer $ELEVE_TOKEN"; echo ""; echo ""

echo "----- DETAIL D'UN VOEU INEXISTANT (attendu : 404) -----"
curl -s -X GET $BASE_URL/voeux/id-bidon-1234 -H "Authorization: Bearer $ELEVE_TOKEN"; echo ""; echo ""

echo "----- MODIFICATION D'UN VOEU -----"
curl -s -X PUT $BASE_URL/voeux/$VOEU_ID -H "Authorization: Bearer $ELEVE_TOKEN" -H "Content-Type: application/json" \
-d "{\"classe_id\":\"$CONSERVATOIRE_ID\",\"creneaux_souhaites\":{\"voeu1\":{\"jour\":\"mercredi\",\"heure\":\"10:00\"},\"voeu2\":{\"jour\":\"jeudi\",\"heure\":\"15:00\"},\"voeu3\":{\"jour\":\"vendredi\",\"heure\":\"16:00\"}}}"
echo ""; echo ""

echo "----- RELANCE DES ELEVES (PROFESSEUR) -----"
curl -s -X POST $BASE_URL/voeux/relancer -H "Authorization: Bearer $PROF_TOKEN" -H "Content-Type: application/json" \
-d "{\"classe_id\":\"$CONSERVATOIRE_ID\",\"eleve_ids\":[\"$ELEVE_ID\"]}"
echo ""; echo ""

echo "----- TESTS VOEUX TERMINÉS ✅ -----"