from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

games_db = [
    {
        "id": 1,
        "titulo": "Cyberpunk 2077",
        "descricao": "RPG futurista",
        "nota_media": 4.2
    },
    {
        "id": 2,
        "titulo": "Hollow Knight",
        "descricao": "Metroidvania indie",
        "nota_media": 4.8
    }
]

class LibraryCreate(BaseModel):
    user_id: int
    game_id: int
    status: str

@app.get("/games")
def listar_jogos():
    return games_db

@app.get("/games/{game_id}")
def search_game(game_id:int):
    for game in games_db:
        if game["id"] == game_id:
            return game