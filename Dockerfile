# Étape 1 : Utilisez une image Python officielle
FROM python:3.11-slim

# Étape 2 : Définissez le répertoire de travail
WORKDIR /app

# Étape 3 : Copiez les dépendances et installez-les
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# Étape 4 : Copiez le code de l'application
COPY ./app /app

# Étape 5 : Exposez le port utilisé par FastAPI
EXPOSE 8000

# Étape 6 : Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]