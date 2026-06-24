"""
Facade de gestion des classes et des vœux de PlanifPro.

Ce module définit la classe PlanningCreneauFacade qui gère la logique
métier liée aux plannings et aux créneaux des élèves.
"""
from planifPro import db
from planifPro.backend.persistence.repository import SQLAlchemyRepository
from planifPro.backend.persistence.planning_repository import PlanningRepository
from planifPro.backend.persistence.creneau_repository import CreneauRepository
from planifPro.backend.persistence.classe_repository import ClasseRepository
from planifPro.backend.persistence.creneau_perso_repository import CreneauPersoRepository
from planifPro.backend.persistence.voeu_repository import VoeuRepository
from planifPro.backend.classes.planning import Planning
from planifPro.backend.classes.creneau import Creneau
from planifPro.backend.classes.creneau_perso import CreneauPerso
from planifPro.backend.classes.voeu import Voeu
from planifPro.backend.classes.tables_relations import eleve_classe
from planifPro.backend.services.fcm_service import envoyer_notification
from datetime import datetime, timezone, timedelta, time
import random


class PlanningCreneauFacade:
    """
    Facade pour la gestion des plannings et des créneaux.

    Centralise la logique métier liée à la création et gestion
    des plannings ainsi que la gestion des créneaux.
    Fait le lien entre les routes API et les repositories correspondants.
    """
    def __init__(self):
        self.planning_repo = PlanningRepository()
        self.creneau_repo = CreneauRepository()
        self.classe_repo = ClasseRepository()
        self.creneau_perso_repo = CreneauPersoRepository()
        self.voeu_repo = VoeuRepository()

    def _parser_date(self, valeur):
        """Convertit une chaîne 'AAAA-MM-JJ' en objet date. Tolère None et date déjà parsée."""
        if valeur is None:
            return None
        if isinstance(valeur, str):
            return datetime.strptime(valeur, '%Y-%m-%d').date()
        return valeur

    def _parser_heure(self, valeur):
        """Convertit 'HH:MM' ou 'HH:MM:SS' en objet time. Tolère None et time déjà parsé."""
        if valeur is None:
            return None
        if isinstance(valeur, str):
            for fmt in ('%H:%M:%S', '%H:%M'):
                try:
                    return datetime.strptime(valeur, fmt).time()
                except ValueError:
                    continue
            raise ValueError("Heure invalide (format attendu HH:MM)")
        return valeur

    # Planning
    def creer_planning(self, donnees):
        """
        Crée un nouveau planning dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            du planning (classe_id, numero_proposition).

        Retourne :
            dict : Dictionnaire contenant les informations
            du planning créé.
        """
        planning = Planning(
            classe_id=donnees['classe_id'],
            numero_proposition=donnees['numero_proposition'],
            statut='genere'
        )
        self.planning_repo.ajouter(planning)
        return planning.to_dict()

    def obtenir_planning(self, planning_id):
        """obtenir_planning permet de récupère un planning"""
        planning = self.planning_repo.obtenir(planning_id)
        if not planning:
            return None
        return planning.to_dict()

    def obtenir_tout_plannings(self):
        """obtenir_tout_plannings permet de récupérer toute les plannings"""
        tout_plannings = self.planning_repo.tout_obtenir()
        if not tout_plannings:
            return None
        return [planning.to_dict() for planning in tout_plannings]

    def mettre_a_jour_planning(self, planning_id, donnees_planning):
        """Mettre à jour un planning existant"""
        planning = self.planning_repo.obtenir(planning_id)
        if not planning:
            return None
        self.planning_repo.mis_a_jour(planning_id, donnees_planning)
        return self.planning_repo.obtenir(planning_id).to_dict()

    def obtenir_plannings_par_classe(self, classe_id):
        """
        obtenir_plannings_par_classe permet de récupérer
        les plannings à partir de ID de la classe.
        """
        plannings = self.planning_repo.obtenir_plannings_par_classe(classe_id)
        if not plannings:
            return None
        return [planning.to_dict() for planning in plannings]

    def obtenir_planning_valide(self, classe_id):
        """
        obtenir_planning_valide permet de récupérer
        un planning à partir d'une classe validé.
        """
        planning = self.planning_repo.obtenir_planning_valide(classe_id)
        if not planning:
            return None
        return planning.to_dict()

    def _heure_en_minutes(self, heure):
        """Convertit 'HH:MM' en minutes depuis minuit."""
        heure, minutes = heure.split(':')
        return int(heure) * 60 + int(minutes)

    def _minutes_en_heure(self, minutes):
        """Convertit des minutes depuis minuit en objet time."""
        return time(hour=minutes // 60, minute=minutes % 60)

    def _duree_eleve(self, eleve_id, classe_id):
        """Récupère la durée de cours d'un élève dans une classe (60 par défaut)."""
        resultat = db.session.execute(
            eleve_classe.select().where(
                eleve_classe.c.eleve_id == eleve_id,
                eleve_classe.c.classe_id == classe_id
            )
        ).fetchone()
        return resultat.duree_minutes if resultat and resultat.duree_minutes else 60

    def _creneau_libre(self, jour, debut_min, duree, jours_horaires, occupe):
        """Vérifie qu'un créneau tient dans la plage du jour et ne chevauche rien."""
        fin_min = debut_min + duree
        horaires = jours_horaires[jour]
        if debut_min < self._heure_en_minutes(horaires['debut']):
            return False
        if fin_min > self._heure_en_minutes(horaires['fin']):
            return False
        for occupe_debut, occupe_fin in occupe[jour]:
            # chevauchement
            if debut_min < occupe_fin and fin_min > occupe_debut:
                return False
        return True

    def _placer_eleve(self, voeu, duree, jours_horaires, occupe):
        """
        Trouve un emplacement pour un élève : d'abord ses vœux (par
        priorité), sinon le premier créneau libre de la dispo.

        Retourne (jour, debut_min) ou None si la dispo est pleine.
        """
        # Les vœux de l'élève, dans l'ordre voeu1, voeu2, voeu3
        for souhait in voeu.creneaux_souhaites.values():
            jour = souhait['jour']
            if jour not in jours_horaires:
                continue
            debut_min = self._heure_en_minutes(souhait['heure'])
            if self._creneau_libre(jour, debut_min, duree, jours_horaires, occupe):
                return (jour, debut_min)

        # Fallback : premier créneau libre de la disponibilité
        for jour, horaires in jours_horaires.items():
            temps = self._heure_en_minutes(horaires['debut'])
            fin_jour = self._heure_en_minutes(horaires['fin'])
            while temps + duree <= fin_jour:
                if self._creneau_libre(jour, temps, duree, jours_horaires, occupe):
                    return (jour, temps)
                temps += duree
        return None

    def generer_planning(self, classe_id):
        """Génère les 3 propositions de planning pour une classe."""
        plannings_existants = self.planning_repo.obtenir_plannings_par_classe(classe_id)
        if plannings_existants:
            raise ValueError("Un planning a déjà été généré pour cette classe")

        classe = self.classe_repo.obtenir(classe_id)
        jours_horaires = classe.jours_horaires
        voeux = self.voeu_repo.obtenir_voeux_par_classe(classe_id) or []

        # Proposition 1 : ordre de soumission (premier arrivé)
        voeux_1 = sorted(voeux, key=lambda v: v.soumis_le)
        self._helper_proposition(jours_horaires, voeux_1, classe, 1)

        # Proposition 2 : ordre aléatoire
        voeux_2 = voeux.copy()
        random.shuffle(voeux_2)
        self._helper_proposition(jours_horaires, voeux_2, classe, 2)

        # Proposition 3 : ordre de soumission inversé
        voeux_3 = sorted(voeux, key=lambda v: v.soumis_le, reverse=True)
        self._helper_proposition(jours_horaires, voeux_3, classe, 3)

        return self.obtenir_plannings_par_classe(classe_id)

    def _helper_proposition(self, jours_horaires, voeux, classe, numero_proposition):
        """Génère une proposition : place chaque élève et crée un Creneau par placement."""
        # occupe[jour] = intervalles déjà pris (debut_min, fin_min)
        occupe = {jour: [] for jour in jours_horaires}

        planning = Planning(
            classe_id=classe.id,
            numero_proposition=numero_proposition,
            statut='genere'
        )
        self.planning_repo.ajouter(planning)

        for voeu in voeux:
            duree = self._duree_eleve(voeu.eleve_id, classe.id)
            place = self._placer_eleve(voeu, duree, jours_horaires, occupe)
            if not place:
                # dispo pleine (cas extrême)
                continue  
            jour, debut_min = place
            occupe[jour].append((debut_min, debut_min + duree))

            creneau = Creneau(
                planning_id=planning.id,
                eleve_id=voeu.eleve_id,
                classe_id=classe.id,
                type=classe.nom,
                jour=jour,
                heure_debut=self._minutes_en_heure(debut_min),
                heure_fin=self._minutes_en_heure(debut_min + duree),
                duree_minutes=duree,
                semaine_alternance=None,
                date_debut=classe.date_debut,
                date_fin=classe.date_fin,
                statut='en_attente'
            )
            self.creneau_repo.ajouter(creneau)

    def selectionner_planning(self, planning_id):
        """
        Sélectionne un planning parmi les propositions générées.

        Vérifie que le planning est généré avant de passer
        le statut à 'selectionne'.

        Arguments :
            planning_id (str) : Identifiant unique du planning.

        Retourne :
            dict : Dictionnaire contenant les informations
            du planning sélectionné.

        Lève :
            ValueError : Si le planning n'est pas en statut 'genere'.
        """
        planning = self.planning_repo.obtenir(planning_id)
        if not planning:
            return None

        if planning.statut not in ['genere', 'selectionne']:
            raise ValueError("Le planning ne peut être selectionné que s'il est généré")

        autres = self.planning_repo.obtenir_plannings_par_classe(planning.classe_id)
        for autre in autres:
            if autre.id != planning_id and autre.statut == 'selectionne':
                self.planning_repo.mis_a_jour(autre.id, {'statut': 'genere'})

        planning.statut = 'selectionne'
        self.planning_repo.mis_a_jour(planning_id, {'statut': 'selectionne'})
        return planning.to_dict()

    def modifier_planning(self, planning_id):
        """
        Modifie manuellement un planning sélectionné.

        Vérifie que le planning est généré ou sélectionné avant
        de passer le statut à 'modifie'.

        Arguments :
            planning_id (str) : Identifiant unique du planning.

        Retourne :
            dict : Dictionnaire contenant les informations
            du planning modifié.

        Lève :
            ValueError : Si le planning n'est pas en statut
            'genere' ou 'selectionne'.
        """
        planning = self.planning_repo.obtenir(planning_id)
        if not planning:
            return None
        if planning.statut not in ['genere', 'selectionne']:
            raise ValueError("Le planning ne peut être modifié que s'il est généré et selectionné")
        planning.statut = 'modifie'
        self.planning_repo.mis_a_jour(planning_id, {'statut': 'modifie'})
        return planning.to_dict()

    def valider_planning(self, planning_id):
        """
        Valide un planning sélectionné.

        Vérifie que le planning est dans un statut valide avant
        de passer le statut à 'valide' et d'enregistrer la date
        de validation.

        Arguments :
            planning_id (str) : Identifiant unique du planning.

        Retourne :
            dict : Dictionnaire contenant les informations
            du planning validé.

        Lève :
            ValueError : Si le planning n'est pas en statut
            'genere', 'selectionne' ou 'modifie'.
        """
        planning = self.planning_repo.obtenir(planning_id)
        if not planning:
            return None
        if planning.statut not in ['genere', 'selectionne', 'modifie']:
            raise ValueError("Le planning ne peut être validé que s'il est généré, sélectionné ou modifié")
        planning.statut = 'valide'
        planning.valide_le = datetime.now(timezone.utc)
        self.planning_repo.mis_a_jour(planning_id, {'statut': 'valide', 'valide_le': datetime.now(timezone.utc)})
        # On supprime les autres propositions de la classe (et leurs créneaux, en cascade)
        autres = self.planning_repo.obtenir_plannings_par_classe(planning.classe_id)
        for autre in autres:
            if autre.id != planning_id:
                self.planning_repo.supprime(autre.id)
        # Envoyer une notification FCM à tous les élèves de la classe
        classe = self.classe_repo.obtenir(planning.classe_id)
        for eleve in classe.eleves:
            self.creer_notification({
                'utilisateur_id': eleve.utilisateur_id,
                'type': 'creneau_attribue',
                'titre': 'Planning validé',
                'message': f"Votre planning pour la classe {classe.nom} a été validé",
            })
            if eleve.token_fcm:
                envoyer_notification(
                    eleve.token_fcm,
                    "Planning validé",
                    f"Votre planning pour la classe {classe.nom} a été validé"
                )
        return planning.to_dict()

    def supprimer_planning(self, planning_id):
        """Supprimer un planning existant et toutes les données associées (cascade)."""
        self.planning_repo.supprime(planning_id)

    # Créneaux
    def creer_creneau(self, donnees):
        """
        Crée un nouveau créneau dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            du créneau (planning_id, eleve_id, classe_id, type,
            jour, heure_debut, heure_fin, duree_minutes).

        Retourne :
            dict : Dictionnaire contenant les informations
            du créneau créé.
        """
        heure_debut = self._parser_heure(donnees['heure_debut'])
        heure_fin = self._parser_heure(donnees['heure_fin'])
        creneaux_existants = self.creneau_repo.obtenir_creneaux_par_eleve(donnees['eleve_id'])
        for creneau in creneaux_existants:
            if creneau.jour == donnees['jour']:
                if heure_debut < creneau.heure_fin and heure_fin > creneau.heure_debut:
                    raise ValueError("chevauchement avec un créneau existant")

        creneau = Creneau(
            planning_id=donnees['planning_id'],
            eleve_id=donnees['eleve_id'],
            classe_id=donnees['classe_id'],
            type=donnees['type'],
            jour=donnees['jour'],
            semaine_alternance=donnees.get('semaine_alternance'),
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            duree_minutes=donnees['duree_minutes'],
            date_debut=self._parser_date(donnees.get('date_debut')),
            date_fin=self._parser_date(donnees.get('date_fin')),
            statut=donnees.get('statut', 'en_attente')
        )
        self.creneau_repo.ajouter(creneau)
        return creneau.to_dict()

    def obtenir_creneau(self, creneau_id):
        """obtenir_creneau permet de récupérer un creneau"""
        creneau = self.creneau_repo.obtenir(creneau_id)
        if not creneau:
            return None
        return creneau.to_dict()

    def obtenir_tout_creneaux(self):
        """obtenir_tout_creneaux permet de récupérer tout les creneaux"""
        tout_creneaux = self.creneau_repo.tout_obtenir()
        if not tout_creneaux:
            return None
        return [creneau.to_dict() for creneau in tout_creneaux]

    def mettre_a_jour_creneau(self, creneau_id, donnees_creneau):
        """Mettre à jour un creneau existant"""
        creneau = self.creneau_repo.obtenir(creneau_id)
        if not creneau:
            return None
        self.creneau_repo.mis_a_jour(creneau_id, donnees_creneau)
        return self.creneau_repo.obtenir(creneau_id).to_dict()

    def obtenir_creneau_par_classe(self, classe_id):
        """
        Récupère tous les créneaux d'une classe.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            list : Liste des créneaux de la classe ou None si aucun trouvé.
        """
        creneaux = self.creneau_repo.obtenir_creneaux_par_classe(classe_id)
        if not creneaux:
            return None
        return [creneau.to_dict() for creneau in creneaux]

    def obtenir_creneaux_par_eleve(self, eleve_id):
        """
        Récupère tous les créneaux d'une classe.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            list : Liste des créneaux de la classe ou None si aucun trouvé.
        """
        creneaux = self.creneau_repo.obtenir_creneaux_par_eleve(eleve_id)
        if not creneaux:
            return None
        creneaux = [
            creneau for creneau in creneaux
            if creneau.planning and creneau.planning.statut == 'valide'
        ]
        return [creneau.to_dict() for creneau in creneaux]

    def obtenir_creneaux_par_professeur(self, professeur_id):
        """Retourne tous les créneaux validés des classes d'un professeur."""
        classes = self.classe_repo.obtenir_classes_par_professeur(professeur_id)
        if not classes:
            return None
        creneaux = []
        for classe in classes:
            creneaux_classe = self.creneau_repo.obtenir_creneaux_par_classe(classe.id)
            if creneaux_classe:
                creneaux.extend([
                    creneau.to_dict() for creneau in creneaux_classe
                    if creneau.planning and creneau.planning.statut == 'valide'
                ])
        return creneaux if creneaux else None

    def obtenir_creneaux_par_planning(self, planning_id):
        """
        Récupère tous les créneaux d'un planning.

        Arguments :
            planning_id (str) : Identifiant unique du planning.

        Retourne :
            list : Liste des créneaux du planning ou None si aucun trouvé.
        """
        creneaux = self.creneau_repo.obtenir_creneaux_par_planning(planning_id)
        if not creneaux:
            return None
        return [creneau.to_dict() for creneau in creneaux]

    def echanger_creneaux(self, creneau_id_1, creneau_id_2):
        """Échange deux créneaux entre deux élèves."""
        creneau_1 = self.creneau_repo.obtenir(creneau_id_1)
        creneau_2 = self.creneau_repo.obtenir(creneau_id_2)
        
        if not creneau_1 or not creneau_2:
            return None
        
        if creneau_1.eleve_id == creneau_2.eleve_id:
            raise ValueError("Les deux créneaux appartiennent au même élève")

        # Vérifier chevauchement pour creneau_1 avec le nouvel eleve
        creneaux_eleve_2 = self.creneau_repo.obtenir_creneaux_par_eleve(creneau_2.eleve_id)
        for creneau in creneaux_eleve_2:
            if creneau.id != creneau_id_2 and creneau.jour == creneau_1.jour:
                if creneau_1.heure_debut < creneau.heure_fin and creneau_1.heure_fin > creneau.heure_debut:
                    raise ValueError("chevauchement après échange")

        # Vérifier chevauchement pour creneau_2 avec le nouvel eleve
        creneaux_eleve_1 = self.creneau_repo.obtenir_creneaux_par_eleve(creneau_1.eleve_id)
        for creneau in creneaux_eleve_1:
            if creneau.id != creneau_id_1 and creneau.jour == creneau_2.jour:
                if creneau_2.heure_debut < creneau.heure_fin and creneau_2.heure_fin > creneau.heure_debut:
                    raise ValueError("chevauchement après échange")
        
        # Échanger les eleve_id
        eleve_id_1 = creneau_1.eleve_id
        self.creneau_repo.mis_a_jour(creneau_id_1, {'eleve_id': creneau_2.eleve_id})
        self.creneau_repo.mis_a_jour(creneau_id_2, {'eleve_id': eleve_id_1})
        
        return {
            'creneau_1': self.creneau_repo.obtenir(creneau_id_1).to_dict(),
            'creneau_2': self.creneau_repo.obtenir(creneau_id_2).to_dict()
        }

    def _decouper_periode(self, creneau, debut_jour, fin_jour):
        """
        Retire l'intervalle de dates [debut_jour, fin_jour] de la période
        d'un créneau récurrent. Découpe en 0, 1 ou 2 lignes.

        Arguments :
            creneau : objet Creneau à découper.
            debut_jour (date) : première date à retirer.
            fin_jour (date) : dernière date à retirer.
        """
        # On récupère les bornes actuelles du créneau en base
        date_debut = creneau.date_debut
        date_fin = creneau.date_fin

        # CAS 1 : le jour cible couvre toute la période du créneau
        # On supprime la ligne entière
        if debut_jour <= date_debut and fin_jour >= date_fin:
            self.creneau_repo.supprime(creneau.id)
        # CAS 2 : le jour cible est au début de la période
        # On avance date_debut au lendemain du dernier jour supprimé
        elif debut_jour <= date_debut:
            self.creneau_repo.mis_a_jour(
                creneau.id, {'date_debut': fin_jour + timedelta(days=1)})
        # CAS 3 : le jour cible est à la fin de la période
        # On recule date_fin à la veille du premier jour supprimé
        elif fin_jour >= date_fin:
            self.creneau_repo.mis_a_jour(
                creneau.id, {'date_fin': debut_jour - timedelta(days=1)})
        # CAS 4 : le jour cible est au milieu de la période
        # On coupe en deux : une ligne avant (mois), une ligne après (mois)
        else:
            # La ligne existante devient la partie AVANT le jour supprimé
            self.creneau_repo.mis_a_jour(
                creneau.id, {'date_fin': debut_jour - timedelta(days=1)})
            # On crée une nouvelle ligne pour la partie APRÈS le jour supprimé
            partie_apres = Creneau(
                planning_id=creneau.planning_id, eleve_id=creneau.eleve_id,
                classe_id=creneau.classe_id, type=creneau.type, jour=creneau.jour,
                heure_debut=creneau.heure_debut, heure_fin=creneau.heure_fin,
                duree_minutes=creneau.duree_minutes,
                semaine_alternance=creneau.semaine_alternance,
                statut=creneau.statut,
                date_debut=fin_jour + timedelta(days=1), date_fin=date_fin)
            self.creneau_repo.ajouter(partie_apres)


    def supprimer_creneau(self, creneau_id, scope='toute_la_periode',
                          debut_jour=None, fin_jour=None):
        """Supprime un créneau selon la portée (toute_la_periode / ce_jour / plusieurs_jours)."""
        creneau = self.creneau_repo.obtenir(creneau_id)
        if not creneau:
            return None
        # Si scope = toute_la_periode → suppression simple sans découpage
        if scope == 'toute_la_periode':
            self.creneau_repo.supprime(creneau_id)
            return
        # Sinon (ce_jour ou plusieurs_jours) → on découpe la période
        self._decouper_periode(
            creneau, self._parser_date(debut_jour), self._parser_date(fin_jour))


    def mettre_a_jour_creneau(self, creneau_id, donnees_creneau,
                              scope='toute_la_periode',
                              debut_jour=None, fin_jour=None):
        """Met à jour un créneau selon la portée ; pour ce_jour/plusieurs_jours,
        découpe la récurrence et crée une ligne d'exception."""
        creneau = self.creneau_repo.obtenir(creneau_id)
        if not creneau:
            return None

        # Convertir les heures éventuelles (chaîne -> time) avant toute écriture
        for champ in ('heure_debut', 'heure_fin'):
            if champ in donnees_creneau:
                donnees_creneau[champ] = self._parser_heure(donnees_creneau[champ])
        # Si scope = toute_la_periode → modification simple de tous les lundis
        if scope == 'toute_la_periode':
            self.creneau_repo.mis_a_jour(creneau_id, donnees_creneau)
            return self.creneau_repo.obtenir(creneau_id).to_dict()

        debut = self._parser_date(debut_jour)
        fin = self._parser_date(fin_jour)

        # On crée la ligne d'exception avec les nouvelles valeurs
        # .get('champ', creneau.champ) = si le prof ne change pas ce champ,
        # on garde la valeur d'origine du créneau
        exception = Creneau(
            planning_id=donnees_creneau.get('planning_id', creneau.planning_id),
            eleve_id=donnees_creneau.get('eleve_id', creneau.eleve_id),
            classe_id=donnees_creneau.get('classe_id', creneau.classe_id),
            type=donnees_creneau.get('type', creneau.type),
            jour=donnees_creneau.get('jour', creneau.jour),
            heure_debut=donnees_creneau.get('heure_debut', creneau.heure_debut),
            heure_fin=donnees_creneau.get('heure_fin', creneau.heure_fin),
            duree_minutes=donnees_creneau.get('duree_minutes', creneau.duree_minutes),
            semaine_alternance=donnees_creneau.get('semaine_alternance', creneau.semaine_alternance),
            statut=donnees_creneau.get('statut', creneau.statut),
            # La ligne d'exception couvre exactement le jour ciblé
            date_debut=debut, date_fin=fin)

        # On découpe l'original pour libérer le jour ciblé
        self._decouper_periode(creneau, debut, fin)
        # On insère la ligne d'exception avec les nouvelles valeurs
        self.creneau_repo.ajouter(exception)
        return exception.to_dict()

    # Créneaux personnels
    def creer_creneau_perso(self, donnees):
        """Crée un nouveau créneau personnel."""
        heure_debut = donnees['heure_debut']
        heure_fin = donnees['heure_fin']
        if isinstance(heure_debut, str):
            heure_debut = time.fromisoformat(heure_debut)
        if isinstance(heure_fin, str):
            heure_fin = time.fromisoformat(heure_fin)

        creneau_perso = CreneauPerso(
            utilisateur_id=donnees['utilisateur_id'],
            titre=donnees['titre'],
            description=donnees.get('description'),
            jour=donnees['jour'],
            heure_debut=heure_debut,
            heure_fin=heure_fin
        )
        self.creneau_perso_repo.ajouter(creneau_perso)
        return creneau_perso.to_dict()

    def obtenir_creneau_perso(self, creneau_perso_id):
        """Récupère un créneau personnel par son ID."""
        creneau_perso = self.creneau_perso_repo.obtenir(creneau_perso_id)
        if not creneau_perso:
            return None
        return creneau_perso.to_dict()

    def obtenir_creneaux_perso_par_utilisateur(self, utilisateur_id):
        """Récupère tous les créneaux personnels d'un utilisateur."""
        creneaux = self.creneau_perso_repo.obtenir_creneaux_perso_par_utilisateur(utilisateur_id)
        if not creneaux:
            return None
        return [creneau.to_dict() for creneau in creneaux]

    def mettre_a_jour_creneau_perso(self, creneau_perso_id, donnees):
        """Met à jour un créneau personnel existant."""
        creneau_perso = self.creneau_perso_repo.obtenir(creneau_perso_id)
        if not creneau_perso:
            return None
        for cle in ('heure_debut', 'heure_fin'):
            if isinstance(donnees.get(cle), str):
                donnees[cle] = time.fromisoformat(donnees[cle])
        self.creneau_perso_repo.mis_a_jour(creneau_perso_id, donnees)
        return self.creneau_perso_repo.obtenir(creneau_perso_id).to_dict()

    def supprimer_creneau_perso(self, creneau_perso_id):
        """Supprime un créneau personnel."""
        self.creneau_perso_repo.supprime(creneau_perso_id)
