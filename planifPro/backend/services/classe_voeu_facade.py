"""
Facade de gestion des classes et des vœux de PlanifPro.

Ce module définit la classe ClasseVoeuFacade qui gère la logique
métier liée aux classes et aux vœux des élèves.
"""
from planifPro.backend.persistence import SQLAlchemyRepository
from planifPro.backend.persistence.classe_repository import ClasseRepository
from planifPro.backend.persistence.voeu_repository import VoeuRepository
from planifPro.backend.classes.classe import Classe
from planifPro.backend.classes.voeu import Voeu
import uuid


class ClasseVoeuFacade:
    """
    Facade pour la gestion des classes et des vœux.

    Centralise la logique métier liée à la création et gestion
    des classes ainsi qu'à la collecte et soumission des vœux.
    Fait le lien entre les routes API et les repositories correspondants.
    """
    def __init__(self):
        self.classe_repo = ClasseRepository()
        self.voeu_repo = VoeuRepository()

    # Classe
    def creer_classe(self, donnees):
        """
        Crée une nouvelle classe dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            de la classe (professeur_id, nom, date_debut, date_fin,
            jours_horaires, nombre_propositions, nombre_voeux_requis,
            nombre_jours_min).

        Retourne :
            dict : Dictionnaire contenant les informations
            de la classe créée.
        """
        classe = Classe(
            professeur_id=donnees['professeur_id'],
            nom=donnees['nom'],
            date_debut=donnees['date_debut'],
            date_fin=donnees['date_fin'],
            jours_horaires=donnees['jours_horaires'],
            nombre_propositions=donnees['nombre_propositions'],
            nombre_voeux_requis=donnees['nombre_voeux_requis'],
            nombre_jours_min=donnees['nombre_jours_min'],
            code_classe=str(uuid.uuid4())[:8].upper(),# création de code unique convertit en string de 8 caractères en majuscules
            statut='classe_active',
        )
        self.classe_repo.ajouter(classe)
        return classe.to_dict()

    def obtenir_classe(self, classe_id):
        """obtenir_classe permet de récupère une classe"""
        classe = self.classe_repo.obtenir(classe_id)
        if not classe:
            return None
        return classe.to_dict()

    def obtenir_tout_classes(self):
        """obtenir_tout_classes permet de récupérer toute les classes"""
        tout_classes = self.classe_repo.tout_obtenir()
        if not tout_classes:
            return None
        return [classe.to_dict() for classe in tout_classes]

    def mettre_a_jour_classe(self, classe_id, donnees_classe):
        """Mettre à jour une classe existant"""
        classe = self.classe_repo.obtenir(classe_id)
        if not classe:
            return None
        self.classe_repo.mis_a_jour(classe_id, donnees_classe)
        return self.classe_repo.obtenir(classe_id).to_dict()

    def obtenir_classes_par_professeur(self, professeur_id):
        """
        obtenir_classe_par_professeur permet de récupérer
        les classes à partir de ID du professeur.
        """
        classes = self.classe_repo.obtenir_classes_par_professeur(professeur_id)
        if not classes:
            return None
        return [classe.to_dict() for classe in classes]

    def obtenir_classe_par_code(self, code_classe):
        """
        obtenir_classe_par_code permet de récupérer
        une classe à partir du code le classe.
        """
        classe = self.classe_repo.obtenir_classe_code(code_classe)
        if not classe:
            return None
        return classe.to_dict()

    def lancer_collecte(self, classe_id):
        """
        Lance la collecte des vœux pour une classe.

        Vérifie que la classe est active avant de passer
        le statut à 'collecte_active'.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            dict : Dictionnaire contenant les informations
            de la classe mise à jour.

        Lève :
            ValueError : Si la classe n'est pas en statut 'classe_active'.
        """
        classe = self.classe_repo.obtenir(classe_id)
        if not classe:
            return None
        if classe.statut != 'classe_active':
            raise ValueError("La collecte ne peut être lancée que si la classe est active")
        classe.statut = 'collecte_active'
        self.classe_repo.mis_a_jour(classe_id, {'statut': 'collecte_active'})
         # TODO: envoyer une notification FCM à tous les élèves de la classe
        return classe.to_dict()

    def supprimer_classe(self, classe_id):
        """Supprimer un classe existant et toutes les données associées (cascade)."""
        self.classe_repo.supprime(classe_id)

    # Voeu
    def creer_voeu(self, donnees):
        """
        Crée un nouveau vœu dans le système.

        Arguments :
            donnees (dict) : Dictionnaire contenant les informations
            du vœu (eleve_id, classe_id, creneaux_souhaites).

        Retourne :
            dict : Dictionnaire contenant les informations
            du vœu créé.
        """
        voeu = Voeu(
            eleve_id=donnees['eleve_id'],
            classe_id=donnees['classe_id'],
            creneaux_souhaites=donnees['creneaux_souhaites'],
            statut='en_attente'
        )
        self.voeu_repo.ajouter(voeu)
        return voeu.to_dict()

    def obtenir_voeu(self, voeu_id):
        """obtenir_voeu permet de récupérer un voeu"""
        voeu = self.voeu_repo.obtenir(voeu_id)
        if not voeu:
            return None
        return voeu.to_dict()

    def obtenir_tout_voeux(self):
        """obtenir_tout_voeus permet de récupérer tout les voeus"""
        tout_voeux = self.voeu_repo.tout_obtenir()
        if not tout_voeux:
            return None
        return [voeu.to_dict() for voeu in tout_voeux]

    def mettre_a_jour_voeu(self, voeu_id, donnees_voeu):
        """Mettre à jour d'un voeu existant"""
        voeu = self.voeu_repo.obtenir(voeu_id)
        if not voeu:
            return None
        self.voeu_repo.mis_a_jour(voeu_id, donnees_voeu)
        return self.voeu_repo.obtenir(voeu_id).to_dict()

    def obtenir_voeu_par_classe(self, classe_id):
        """
        Récupère tous les vœux d'une classe.

        Arguments :
            classe_id (str) : Identifiant unique de la classe.

        Retourne :
            list : Liste des vœux de la classe ou None si aucun trouvé.
        """
        voeux = self.voeu_repo.obtenir_voeux_par_classe(classe_id)
        if not voeux:
            return None
        return [voeu.to_dict() for voeu in voeux]

    def obtenir_voeux_par_eleve(self, eleve_id):
        """
        Récupère tous les vœux d'un élève.

        Arguments :
            eleve_id (str) : Identifiant unique de l'élève.

        Retourne :
            list : Liste des vœux de l'élève ou None si aucun trouvé.
        """
        voeux = self.voeu_repo.obtenir_voeux_par_eleve(eleve_id)
        if not voeux:
            return None
        return [voeu.to_dict() for voeu in voeux]

    def supprimer_voeu(self, voeu_id):
        """Supprimer un voeu existant et toutes les données associées (cascade)."""
        self.voeu_repo.supprime(voeu_id)