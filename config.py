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

    # --- Authentification par cookie httpOnly ---
    # Le token n'est plus lu dans l'en-tête Authorization mais dans un cookie.
    JWT_TOKEN_LOCATION = ['cookies']
    # Le cookie est envoyé sur toutes les routes de l'API.
    JWT_COOKIE_CSRF_PROTECT = False   # protection CSRF (obligatoire avec les cookies)
    JWT_COOKIE_SAMESITE = 'None'     # nécessaire car front et back sont sur des domaines différents
    JWT_COOKIE_SECURE = True         # cookie envoyé uniquement en HTTPS


class DevelopmentConfig(Config):
    DEBUG = True
    # En local on est en HTTP (pas HTTPS), donc on assouplit :
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'Lax'


class ProductionConfig(Config):
    pass   # garde Secure=True et SameSite=None (cross-domain Vercel ↔ Render)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False},
        'poolclass': StaticPool,
    }
    JWT_SECRET_KEY = 'cle-jwt-de-test-pour-les-tests-unitaires-planifpro'

    # Les tests utilisent l'en-tête Authorization, pas les cookies
    JWT_TOKEN_LOCATION = ['headers']
    JWT_COOKIE_CSRF_PROTECT = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
