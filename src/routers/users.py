from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Schéma Pydantic pour valider les données d'entrée
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Initialiser le contexte de hachage pour les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

# Route pour créer un utilisateur
@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Route pour récupérer tous les utilisateurs
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Route pour compter le nombre total d'utilisateurs
@router.get("/count")
def count_users(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {"total_users": count}

