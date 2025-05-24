from fastapi import FastAPI, HTTPException, Depends
from schemas.UserInput import UserInput, MatchRequest
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from matching import MusicMatchEngine
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from kafka.kafka_consumer import consume_messages
from kafka.kafka_producer import * 
from schemas.feedback import FeedbackCreate
from schemas.User import UserBase
from models.userModel import User
from routers import matches
import services.relationService as relationService
import os
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion complète du cycle de vie de l'application"""
    # Phase de démarrage
    print("Chargement du modèle...")
    try:
        # Initialisation des ressources
        app.state.model = SentenceTransformer(
            "all-mpnet-base-v2",
            cache_folder=os.getenv('MODEL_CACHE_PATH', '/model_cache'),
            device='cpu'
        )
        app.state.match_engine = MusicMatchEngine(app.state.model)
        
        # Démarrage du consommateur Kafka
        app.state.kafka_consumer_task = asyncio.create_task(consume_messages())
        print("Modèle, moteur et consommateur Kafka prêts")
        
        yield
        
    except Exception as e:
        print(f"Erreur de chargement: {str(e)}")
        raise
        
    finally:
        # Phase d'arrêt
        print("Nettoyage des ressources...")
        if hasattr(app.state, 'kafka_consumer_task'):
            app.state.kafka_consumer_task.cancel()
            try:
                await app.state.kafka_consumer_task
            except asyncio.CancelledError:
                pass
                
        if hasattr(app.state, 'model'):
            del app.state.model
        if hasattr(app.state, 'match_engine'):
            del app.state.match_engine

app = FastAPI(lifespan=lifespan)
app.include_router(matches.router)

@app.get("/")
async def root():
    return {"message": "Hello there"}
#match avec music taste
@app.post("/match") # getMatchs
async def match_users(user1: dict, user2: dict):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )
    result = await app.state.match_engine.calculate_compatibility(user1, user2)
    return result
#match without music taste
@app.post("/matchwithoutmusic")
async def match_users_without_music(user1: UserBase, user2: UserBase):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )
   
    result = await app.state.match_engine.calculate_compatibility_from_dicts(user1, user2)
    return result

@app.get("/health")
async def health_check():
    status = {
        "status": "ready" if hasattr(app.state, 'match_engine') else "loading",
        "model": "all-mpnet-base-v2",
        "kafka": "running" if hasattr(app.state, 'kafka_consumer_task') else "stopped"
    }
    return status

@app.get("/matching/{user_id1}/{user_id2}")
async def match_users(
    user_id1: int, 
    user_id2: int, 
    db: Session = Depends(get_db)
):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )
    
    user1 = await app.state.match_engine.get_user_data(db, user_id1)
    user2 = await app.state.match_engine.get_user_data(db, user_id2)
    result = await app.state.match_engine.calculate_compatibility(user1, user2)
    return result

@app.get("/matching/{user_id}")
async def get_potential_matches(
    user_id: int, 
    db: Session = Depends(get_db)
):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non charcé"
        )
    
    user = await app.state.match_engine.get_user_data(db, user_id)
    users_ids = await app.state.match_engine.get_users_id(db, user_id)
    
    results = []
    for other_user_id in users_ids:
        # ajouter une methode qui verifie si il existe deja un match entre les deux utilisateurs
        # si oui, on ne fait pas le calcul de compatibilité
        # sinon on le fait
        if not relationService.checkMatchExists(user_id, other_user_id, db):
            other_user = await app.state.match_engine.get_user_data(db, other_user_id)
            result = await app.state.match_engine.calculate_compatibility(user, other_user)
            results.append(result)
    
    return results
@app.get("/Savematches/{user_id}")
async def save_matches(
    user_id: int, 
    db: Session = Depends(get_db),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer)
):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )
    return await relationService.getMatches(user_id, db, app.state.match_engine, kafka_producer)
    
@app.get("/getFeedback/{match_id}")
async def get_feedback(
    match_id: int, 
    db: Session = Depends(get_db)
):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )
    feedback = await relationService.getFeedBack(match_id, db)
    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback non trouvé"
        )
    return feedback

@app.post("/changefeedback")
async def change_feedback(feedback:FeedbackCreate, db: Session = Depends(get_db)):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )

    feedback = await relationService.changeFeedback(feedback.match_id, feedback.user_id, feedback.score, db)
    return feedback
  
@app.post("/updateUserInf")
async def update_user_information(user: UserBase, db: Session = Depends(get_db)):
    user1 = await relationService.updateUserInformation(user, db)
    return user1

@app.get("/match/delete/{match_id}")
async def delete_match(
    match_id: int, 
    db: Session = Depends(get_db)
):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )
    match = await relationService.deleteMatch(match_id, db)
    if not match:
        raise HTTPException(
            status_code=404,
            detail="match non trouvé"
        )
    return match
















# from fastapi import FastAPI, HTTPException
# from schemas.UserInput  import UserInput, MatchRequest
# from contextlib import asynccontextmanager
# from sentence_transformers import SentenceTransformer
# from matching import MusicMatchEngine
# from sqlalchemy.orm import Session
# from database import get_db, SessionLocal
# from kafka.kafka_consumer import consume_messages  
# from routers import matches
# #import Depends
# from fastapi import Depends
# import os
# import asyncio

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Gestion du cycle de vie avec async/await"""
#     # Phase de démarrage (avant yield)
#     print(" Chargement du modèle...")
#     try:
#         app.state.model = SentenceTransformer(
#             "all-mpnet-base-v2",
#             cache_folder=os.getenv('MODEL_CACHE_PATH', '/model_cache'),
#             device='cpu'
#         )
#         app.state.match_engine = MusicMatchEngine(app.state.model)
#         print(" Modèle et moteur prêts")
#         yield
#     except Exception as e:
#         print(f" Erreur de chargement: {str(e)}")
#         raise
#     finally:
#         # Phase d'arrêt (après yield)
#         print(" Nettoyage des ressources...")
#         if hasattr(app.state, 'model'):
#             del app.state.model
#         if hasattr(app.state, 'match_engine'):
#             del app.state.match_engine

# # Intégration du lifespan handler
# app = FastAPI(lifespan=lifespan)
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(consume_messages())  # Démarre la consommation des messages Kafka
# app.include_router(matches.router)
# @app.get("/")
# async def root():
#     return {"message": "Hello there"}

# @app.post("/match")
# async def match_users(user1: dict, user2: dict):
#     if not hasattr(app.state, 'match_engine'):
#         raise HTTPException(
#             status_code=503,
#             detail="Service non prêt: moteur de matching non chargé"
#         )
#     result = await app.state.match_engine.calculate_compatibility(user1,user2)
#     return result
# @app.get("/health")
# async def health_check():
#     status = {
#         "status": "ready" if hasattr(app.state, 'match_engine') else "loading",
#         "model": "all-mpnet-base-v2"
#     }
#     return status
# @app.get("/matching/{user_id1}/{user_id2}")
# async def match(user_id1: int, user_id2: int, db: Session = Depends(get_db)):
#     if not hasattr(app.state, 'match_engine'):
#         raise HTTPException(
#             status_code=503,
#             detail="Service non prêt: moteur de matching non chargé"
#         )
#     # Appel de la méthode de matching
#     user1 = await app.state.match_engine.get_user_data(db,user_id1)
#     user2 = await app.state.match_engine.get_user_data(db,user_id2)
#     result = await app.state.match_engine.calculate_compatibility(user1, user2)
#     return result

# @app.get("/matching/{user_id}")
# async def match(user_id: int, db: Session = Depends(get_db)):
#     if not hasattr(app.state, 'match_engine'):
#         raise HTTPException(
#             status_code=503,
#             detail="Service non prêt: moteur de matching non chargé"
#         )
#     # Appel de la méthode de matching
#     user = await app.state.match_engine.get_user_data(db,user_id)
#     users = await app.state.match_engine.get_users_id(db,user_id)
#     results = []
#     user1 = await app.state.match_engine.get_user_data(db,user_id)
#     for user2 in users:
#         user2 = await app.state.match_engine.get_user_data(db,user2)
#         result = await app.state.match_engine.calculate_compatibility(user1, user2)
#         results.append(result)
#     return results

