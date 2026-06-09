"""
Service d'envoi d'emails via Brevo pour PlanifPro.
"""
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os


def envoyer_email(destinataire_email, destinataire_nom, sujet, contenu):
    """
    Envoie un email via Brevo.

    Arguments :
        destinataire_email (str) : Email du destinataire.
        destinataire_nom (str) : Nom du destinataire.
        sujet (str) : Sujet de l'email.
        contenu (str) : Contenu HTML de l'email.

    Retourne :
        bool : True si succès, False si échec.
    """
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{'email': destinataire_email, 'name': destinataire_nom}],
        sender={'email': os.getenv('BREVO_FROM_EMAIL'), 'name': 'PlanifPro'},
        subject=sujet,
        html_content=contenu
    )

    try:
        api_instance.send_transac_email(email)
        return True
    except ApiException as e:
        print(f"Erreur envoi email : {e}")
        return False
