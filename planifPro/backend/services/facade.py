"""
Facade principale de PlanifPro.

Ce module définit la classe PlanifProFacade qui centralise
la logique métier et fait le lien entre la couche API
et la couche de persistance.
"""
from planifPro.backend.services.auth_facade import AuthFacade
from planifPro.backend.services.classe_voeu_facade import ClasseVoeuFacade
from planifPro.backend.services.planning_creneau_facade import PlanningCreneauFacade
from planifPro.backend.services.objectif_evenement_notification_facade import ObjectifEvenementNotificationFacade


class PlanifProFacade(AuthFacade, ClasseVoeuFacade, PlanningCreneauFacade, ObjectifEvenementNotificationFacade):
    """
    Facade principale de PlanifPro.

    Centralise la logique métier et abstrait l'accès direct
    aux repositories. Fait le lien entre les routes API
    et la couche de persistance.
    """
    def __init__(self):
        AuthFacade.__init__(self)
        ClasseVoeuFacade.__init__(self)
        PlanningCreneauFacade.__init__(self)
        ObjectifEvenementNotificationFacade.__init__(self)
