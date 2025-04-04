from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
# from sentence_transformers import SentenceTransformer
# from matching import MusicMatchEngine
import os
from database import get_db

app = FastAPI()

# app.on_event("startup")
# def load_model():
#     app.state.model = SentenceTransformer("all-mpnet-base-v2",
#     cache_folder=os.getenv('MODEL_CACHE_PATH', '/app/model_cache'),
#     device='cpu' )
#     app.state.match_engine = MusicMatchEngine(app.state.model)
@app.get("/")
async def root():
    return {"message": "Hello World "}


# @app.post("/match")
# async def match_users(user1: dict, user2: dict):
#     return app.state.match_engine.calculate_compatibility(user1, user2)

# @app.get("/health")
# def health_check():
#     return {
#         "status": "ready",
#         "model": "all-mpnet-base-v2",
#         "memory": f"{os.sys.getsizeof(app.state.match_engine.model)/1024/1024:.2f}MB"
#     }