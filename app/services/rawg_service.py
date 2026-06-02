import httpx
from app.core.config import RAWG_API_KEY

RAWG_BASE_URL = "https://api.rawg.io/api"

def buscar_jogos_rawg(nome: str):
    url = f"{RAWG_BASE_URL}/games"
    params = {
        "key": RAWG_API_KEY,
        "search": nome,
        "page_size": 10
    }
    response = httpx.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()