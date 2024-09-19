# Utilise l'image de base Python 3.8.10
FROM python:3.8.10

# Définit le répertoire de travail
WORKDIR /app

# Copie tous les fichiers du projet dans le conteneur
COPY . /app

# Installer une version spécifique de pip
RUN python -m pip install pip==20.0.2

# Installer les dépendances du fichier requirements.txt
RUN pip install -r /app/requirements.txt

# Expose le port 5000
EXPOSE 5000

# Commande pour démarrer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]

