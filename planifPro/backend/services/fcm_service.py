"""
Service Firebase Cloud Messaging (FCM) de PlanifPro.

Ce module gère l'initialisation de Firebase et l'envoi
des notifications push aux utilisateurs de l'application.
"""
import firebase_admin
from firebase_admin import credentials, messaging
import os


def initialiser_firebase():
    """
    Initialise l'application Firebase avec les credentials
    définis dans les variables d'environnement.
    """
    chemin = os.getenv('FIREBASE_CREDENTIALS')
    cred = credentials.Certificate(chemin)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)


def envoyer_notification(token, titre, contenu):
    """
    Envoie une notification push via Firebase Cloud Messaging.

    Arguments :
        token (str) : Token FCM de l'appareil destinataire.
        titre (str) : Titre de la notification.
        contenu (str) : Corps du message de la notification.

    Retourne :
        bool : True si l'envoi est réussi, False en cas d'erreur.
    """
    try:
        msg = messaging.Message(
            notification=messaging.Notification(
                title=titre,
                body=contenu
            ),
            token=token
        )
        messaging.send(msg)
    except Exception as e:
        return False
    return True
        