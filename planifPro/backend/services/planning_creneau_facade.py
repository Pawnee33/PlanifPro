"""
Facade de gestion des classes et des vœux de PlanifPro.

Ce module définit la classe PlanningCreneauFacade qui gère la logique
métier liée aux plannings et aux créneaux des élèves.
"""
from planifPro.backend.persistence import SQLAlchemyRepository
from planifPro.backend.persistence.planning_repository import PlanningRepository
from planifPro.backend.persistence.creneau_repository import CreneauRepository
from planifPro.backend.persistence.classe_repository import ClasseRepository
from planifPro.backend.classes.planning import Planning
from planifPro.backend.classes.creneau import Creneau
from planifPro.backend.services.fcm_service import envoyer_notification
from datetime import datetime, timezone


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

    def generer_planning(self, classe_id):
        """
        Génère les propositions de planning pour une classe.
        """
        # TODO: implémenter l'algorithme de génération
        pass

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
        if planning.statut != 'genere':
            raise ValueError("Le planning ne peut être selectionné que s'il est généré")
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
        # Envoyer une notification FCM à tous les élèves de la classe
        classe = self.classe_repo.obtenir(planning.classe_id)
        for eleve in classe.eleves:
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
        creneaux_existants = self.creneau_repo.obtenir_creneaux_par_eleve(donnees['eleve_id'])
        for creneau in creneaux_existants:
            if creneau.jour == donnees['jour']:
                if donnees['heure_debut'] < creneau.heure_fin and donnees['heure_fin'] > creneau.heure_debut:
                    raise ValueError("chevauchement avec un créneau existant")

        creneau = Creneau(
            planning_id=donnees['planning_id'],
            eleve_id=donnees['eleve_id'],
            classe_id=donnees['classe_id'],
            type=donnees['type'],
            jour=donnees['jour'],
            heure_debut=donnees['heure_debut'],
            heure_fin=donnees['heure_fin'],
            duree_minutes=donnees['duree_minutes'],
            statut='en_attente'
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
                creneaux.extend([creneau.to_dict() for creneau in creneaux_classe])
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

    def supprimer_creneau(self, creneau_id):
        """Supprimer un creneau existant et toutes les données associées (cascade)."""
        self.creneau_repo.supprime(creneau_id)
