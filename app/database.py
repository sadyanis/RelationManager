from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connexion à PostgreSQL (remplace les valeurs selon ta configuration)
# Then
# DATABASE_URL = "postgresql://user:password@db:5432/mydb"
#engine = create_engine(DATABASE_URL)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base = declarative_base()
# Now
DATABASE_URL = "postgresql://user:password@db:5432/mydb"

# engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocal = sessionmaker(
    # bind=engine,
    # class_=AsyncSession,
    # expire_on_commit=False,
# )
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db =  SessionLocal() #SessionLocal()
    try:
        yield db
    finally:
        db.close()
