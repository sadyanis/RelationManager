FROM python:3.11-slim

#  dépendances système 
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install -U sentence-transformers


# RUN mkdir -p /app/model_cache


COPY . .

# Télécharger le modèle de SentenceTransformer
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-mpnet-base-v2', cache_folder='/app/model_cache')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



# FROM python:3.11-slim

# WORKDIR /app


# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt && pip install alembic

# COPY . .

# EXPOSE 8000

# # lancer l'application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]