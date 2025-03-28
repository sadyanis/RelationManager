
FROM python:3.11-slim

#  répertoire de travail
WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install alembic

COPY . .

EXPOSE 8000

# lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]