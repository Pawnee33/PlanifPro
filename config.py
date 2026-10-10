import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool


load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # ----- JWT stocké dans un cookie HttpOnly -----
    # Le token n'est plus lu dans l'en-tête Authorization mais dans un cookie
    # que le JavaScript ne peut pas lire (protection contre le vol par XSS).
    JWT_TOKEN_LOCATION = ['cookies']
    # False : le cookie survit à la fermeture du navigateur (comme l'ancien
    # localStorage) ; c'est l'expiration du JWT (8 h) qui termine la session.
    JWT_SESSION_COOKIE = False
    # En production (HTTPS) : JWT_COOKIE_SECURE=true.
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'false').lower() == 'true'
    # 'Lax' si le front et l'API sont sur le même site (localhost, ou API
    # servie derrière le domaine du front). 'None' s'ils sont sur deux domaines
    # différents (exige JWT_COOKIE_SECURE=true).
    JWT_COOKIE_SAMESITE = os.getenv('JWT_COOKIE_SAMESITE', 'Lax')
    # Protection CSRF : toute requête POST / PUT / PATCH / DELETE doit porter
    # l'en-tête X-CSRF-TOKEN. Le jeton est renvoyé dans la réponse de connexion
    # (et non dans un cookie, illisible par le front s'il est sur un autre domaine).
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_IN_COOKIES = False
 
    # Origines autorisées à appeler l'API avec le cookie (séparées par des
    # virgules). Par défaut : l'URL du frontend.
    CORS_ORIGINS = [
        origine.strip().rstrip('/')
        for origine in os.getenv(
            'CORS_ORIGINS', os.getenv('FRONTEND_URL', 'http://localhost:5173')
        ).split(',')
    ]
 

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False},
        'poolclass': StaticPool,
    }
    JWT_SECRET_KEY = 'cle-jwt-de-test-pour-les-tests-unitaires-planifpro'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
