# Image de base légère avec Python 3.12
FROM python:3.12-slim

# Bonnes pratiques Python en conteneur
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Dossier de travail dans l'image
WORKDIR /app

# 1. Copier d'abord les dépendances (cache Docker : ré-installe seulement si requirements.txt change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copier le reste du code
COPY . .

# Port exposé (documentaire — Render fournit la variable $PORT)
EXPOSE 5000

# Lancement en production via gunicorn
# ${PORT:-5000} : utilise $PORT si défini (Render), sinon 5000 en local
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} "planifPro.run:app"
