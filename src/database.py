from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@db/storedb"

# Créer un moteur de base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Créer une session locale pour communiquer avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer une classe de base pour définir les modèles SQLAlchemy
Base = declarative_base()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

