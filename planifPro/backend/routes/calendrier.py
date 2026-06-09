"""
Endpoints de gestion du calendrier Google de PlanifPro.

Ce module définit les routes REST liées à l'intégration
Google Calendar, permettant aux utilisateurs d'autoriser
l'accès et d'exporter leurs créneaux.
"""
from flask import request, redirect
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from google_auth_oauthlib.flow import Flow
from planifPro.backend.services.facade import PlanifProFacade
import os

facade = PlanifProFacade()

api = Namespace('calendrier', description='Opération Google Calendar')

export_model = api.model('Export', {
    'creneau_ids': fields.List(fields.String, required=True, description='IDs des créneaux à exporter')
})

SCOPES = ['https://www.googleapis.com/auth/calendar']