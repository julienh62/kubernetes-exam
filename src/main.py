from fastapi import FastAPI
from src.routers import users
from src.database import engine
from src.models import Base

app = FastAPI()

# Créer toutes les tables au démarrage
Base.metadata.create_all(bind=engine)

# Inclure le routeur d'utilisateurs
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Streaming Service API!"}

