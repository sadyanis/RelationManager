#  Relation Manager - Music-Based Matchmaking Microservice

Un microservice de calcul de compatibilité entre utilisateurs basé sur les goûts musicaux, développé avec FastAPI et containerisé avec Docker.

##  Fonctionnalités

- **Calcul de compatibilité** : Score de matching basé sur les préférences musicales
- **API RESTful** : Interface complète pour la gestion des relations
- **Authentication sécurisée** : Intégration Keycloak pour la protection des routes
- **Communication asynchrone** : Utilisation de Kafka pour l'interconnexion des microservices
- **Containerisation** : Déploiement Docker complet avec Docker Compose
- **Hot-reload** : Développement avec rechargement automatique

##  Architecture Technique

### Stack Technique
- **Backend** : FastAPI (Python 3.11)
- **Base de données** : PostgreSQL 16
- **Authentication** : Keycloak
- **Message Broker** : Apache Kafka
- **Embeddings** : Sentence Transformers (all-mpnet-base-v2)
- **Containerisation** : Docker & Docker Compose
- **Serveur** : Uvicorn

## 📋 API Endpoints

### 🔐 Endpoints Authentifiés
- `GET /` - Page d'accueil (Admin seulement)
- `GET /health` - Statut du service (Admin seulement)

### 🤝 Gestion des Matchs
- `POST /match` - Calcul de compatibilité avec goûts musicaux
- `POST /matchwithoutmusic` - Matching basique sans musique
- `GET /matching/{user_id1}/{user_id2}` - Matching entre deux utilisateurs
- `GET /matching/{user_id}` - Liste des matchs potentiels
- `GET /Savematches/{user_id}` - Sauvegarde des matchs

###  Feedback & Gestion
- `GET /getFeedback/{match_id}` - Récupération des feedbacks
- `POST /changefeedback` - Modification des feedbacks
- `POST /updateUserInf` - Mise à jour des informations utilisateur
- `GET /match/delete/{match_id}` - Suppression d'un match

##  Installation & Déploiement

### Prérequis
- Docker
- Docker Compose

### Déploiement Rapide

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd relation-manager
```
### Démarrage des services
```bash
docker-compose up -d
```
### Vérification du déploiement
```bash
curl http://localhost:8000/health
```
### Accès aux services
- **API Relation Manager**:http://localhost:8000
- **Documentation FastAPI** : http://localhost:8000/docs
- **Base de données PostgreSQL** : localhost:5432
- **Keycloak** : http://localhost:8080
## Développement
### Construction manuelle de l'image
```bash
docker build -t relation-manager .
```
### Exécution en mode développement
```bash
docker-compose up --build
```
## Sécurité
- **Keycloak** : Gestion centralisée des authentifications.
- **Protection des routes**:  Middleware d'authentification via dépendances FastAPI.
- **Validation des données**: Schémas Pydantic pour la validation des entrées
## Algorithme de Matching
Le système utilise un moteur de matching sophistiqué :
1. **Embeddings musicaux** : Conversion des préférences musicales en vecteurs avec all-mpnet-base-v2
2. **Similarité sémantique** : Calcul de similarité cosinus entre les embeddings
3. **Facteurs multiples** : Combinaison avec d'autres critères de compatibilité
4. **Score personnalisé** : Génération d'un pourcentage de matching
## Auteurs
**SADOUN YANIS** - Développeur Principal - @sadyanis




