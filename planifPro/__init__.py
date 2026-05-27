"""
Fonction de création de l'application PlanifPro.

Ce module fournit la fonction de création de l'application Flask,
configure l'instance de l'application, initialise l'API REST
et enregistre tous les namespaces.
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
cors = CORS()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Crée et configure l'application Flask.

    Cette fonction initialise l'instance de l'application Flask,
    configure l'API Flask-RESTX avec ses métadonnées et son endpoint
    de documentation, et enregistre tous les namespaces de l'API.

    Retourne :
        Flask : Instance de l'application Flask configurée.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)
    

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from planifPro.backend.routes.authentification import api as authentification_ns
    from planifPro.backend.routes.calendrier import api as calendrier_ns
    from planifPro.backend.routes.classes import api as classes_ns
    from planifPro.backend.routes.creneaux import api as creneaux_ns
    from planifPro.backend.routes.eleves import api as eleves_ns
    from planifPro.backend.routes.evenements import api as evenements_ns
    from planifPro.backend.routes.notifications import api as notifications_ns
    from planifPro.backend.routes.objectifs import api as objectifs_ns
    from planifPro.backend.routes.plannings import api as plannings_ns
    from planifPro.backend.routes.professeurs import api as professeurs_ns
    from planifPro.backend.routes.utilisateurs import api as utilisateurs_ns
    from planifPro.backend.routes.voeux import api as voeux_ns

    api = Api(
        app,
        version='1.0',
        title='PlanifPro API',
        description='PlanifPro Application API',
        doc='/api/v1/'
    )

    # Enregistrement des namespaces
    api.add_namespace(authentification_ns, path='/api/v1/authentification')
    api.add_namespace(calendrier_ns, path='/api/v1/calendrier')
    api.add_namespace(classes_ns, path='/api/v1/classes')
    api.add_namespace(creneaux_ns, path='/api/v1/creneaux')
    api.add_namespace(eleves_ns, path="/api/v1/eleves")
    api.add_namespace(evenements_ns, path='/api/v1/evenements')
    api.add_namespace(notifications_ns, path='/api/v1/notifications')
    api.add_namespace(objectifs_ns, path='/api/v1/objectifs')
    api.add_namespace(plannings_ns, path='/api/v1/plannings')
    api.add_namespace(professeurs_ns, path='/api/v1/professeurs')
    api.add_namespace(utilisateurs_ns, path='/api/v1/utilisateurs')
    api.add_namespace(voeux_ns, path='/api/v1/voeux')

    return app
