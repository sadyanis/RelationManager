import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool , create_engine
from alembic import context
from models.userModel import User  
from models.matchModel import Match  
from models.feedbackModel import Feedback  
from models.userMusicStatModel import UserMusicStat  
# Ajoute le dossier `app/` au chemin des modules Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ➜ Importer la configuration de la base de données depuis FastAPI
from database import Base, SYNC_DATABASE_URL  # 

# Charger la configuration Alembic
config = context.config
fileConfig(config.config_file_name)


config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)


target_metadata = Base.metadata  

def run_migrations_offline():
    """Exécuter les migrationss en mode 'offline' (sans connexion à la BDD)."""
    context.configure(url=SYNC_DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Exécuter les migrations en mode 'online' (connecté à la BDD)."""
    #connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    connectable = create_engine(SYNC_DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
