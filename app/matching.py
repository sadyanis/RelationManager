# from sentence_transformers import util
# import numpy as np

# class MusicMatchEngine:
#     def __init__(self, model):
#         self.model = model

#     def preprocess_profile(self, user: dict) -> str:
#         """Convertit un profil utilisateur en texte pour l'embedding"""
#         return f"""
#         Genre: {user['gender']} | Target: {user['targeted_gender']}
#         Age: {user['birthdate'][:4]} | AgeGap: {user['accepted_age_gap']}
#         Style: {user['favorite_musical_style']}
#         Artists: {' '.join(user['top_Listened_Artist'])}
#         Tracks: {' '.join(user['top_Listened_Music'])}
#         """

#     def calculate_compatibility(self, user1: dict, user2: dict) -> dict:
#         # 1. Vérification des critères de base
#         age1 = int(user1['birthdate'][:4])
#         age2 = int(user2['birthdate'][:4])
#         age_gap = abs(age1 - age2)

#         if age_gap > min(user1['accepted_age_gap'], user2['accepted_age_gap']):
#             return {"match_percentage": 0, "reason": "Écart d'âge trop important"}

#         if not (user1['gender'] in user2['targeted_gender'] and 
#                 user2['gender'] in user1['targeted_gender']):
#             return {"match_percentage": 0, "reason": "Incompatibilité de genre"}

#         # 2. Calcul de la similarité musicale
#         text1 = self.preprocess_profile(user1)
#         text2 = self.preprocess_profile(user2)
        
#         emb1 = self.model.encode(text1, convert_to_tensor=True)
#         emb2 = self.model.encode(text2, convert_to_tensor=True)
        
#         music_similarity = util.cos_sim(emb1, emb2).item()

#         # 3. Score composite (ajustez les poids selon vos besoins)
#         match_percentage = int((music_similarity * 0.7 + 0.3) * 100)  # Garantit un minimum de 30%

#         return {
#             "match_percentage": min(match_percentage, 100),  # Max 100%
#             "age_compatibility": f"{age_gap} ans (toléré: {user1['accepted_age_gap']}/{user2['accepted_age_gap']})",
#             "music_similarity": f"{music_similarity:.2f}",
#             "top_common_artists": self._find_common_artists(user1, user2)
#         }

#     def _find_common_artists(self, user1: dict, user2: dict) -> list:
#         """Trouve des artistes similaires (même partiellement)"""
#         from difflib import get_close_matches
#         common = []
#         for artist in user1['top_Listened_Artist']:
#             matches = get_close_matches(artist, user2['top_Listened_Artist'], cutoff=0.6)
#             common.extend(matches)
#         return list(set(common))