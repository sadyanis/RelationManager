import random
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal  # À créer (voir explications)
from models.userModel import User  
from models.matchModel import Match  
from models.feedbackModel import Feedback  
from models.userMusicStatModel import UserMusicStat  

fake = Faker()

def seed_users(n=10):
    """Insère des utilisateurs fictifs (version synchrone)"""
    with SessionLocal() as db:
        users = [
            User(
                user_id=i + 1,
                is_certified=random.choice([0, 1]),
                is_active=1,
                birthdate=fake.date_of_birth(minimum_age=18, maximum_age=60),
                gender=random.choice(["M", "F"]),
                accepted_age_gap=random.randint(1, 10),
                accepted_distance=random.randint(5, 50),
                targeted_gender=random.choice(["M", "F", "Both"]),
                favorite_musician=fake.name(),
                favorite_music=fake.sentence(nb_words=3),
                favorite_musical_style=fake.word(),
            )
            for i in range(n)
        ]
        db.add_all(users)
        db.commit()

def seed_matches(n=5):
    """Insère des matchs fictifs (version synchrone)"""
    with SessionLocal() as db:
        matches = [
            Match(
                match_id=i + 1,
                user1_id=random.randint(1, 10),
                user2_id=random.randint(1, 10),
                match_compatibility=random.randint(50, 100),  # Correction orthographique
                status_code=random.choice([0, 1, 2]),
            )
            for i in range(n)
        ]
        db.add_all(matches)
        db.commit()

def seed_feedback(n=5):
    """Insère des feedbacks fictifs (version synchrone)"""
    with SessionLocal() as db:
        feedbacks = [
            Feedback(
                match_id=i + 1,
                user1_id=random.randint(1, 10),
                user2_id=random.randint(1, 10),
                score_user1=random.randint(1, 5),
                score_user2=random.randint(1, 5),
            )
            for i in range(n)
        ]
        db.add_all(feedbacks)
        db.commit()

def seed_user_music_stats(n=10):
    """Insère des statistiques musicales fictives (version synchrone)"""
    with SessionLocal() as db:
        music_stats = [
            UserMusicStat(
                user_id=i + 1,
                top_Listened_Artist=[fake.name() for _ in range(3)],
                top_Listened_Music=[fake.sentence(nb_words=3) for _ in range(3)],
            )
            for i in range(n)
        ]
        db.add_all(music_stats)
        db.commit()

def main():
    seed_users(10)
    seed_matches(5)
    seed_feedback(5)
    seed_user_music_stats(10)
    print("Base de données peuplée avec succès !")

if __name__ == "__main__":
    main()
