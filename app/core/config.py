import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///db_Gamelog.db"
SECRET_KEY = os.getenv("SECRET_KEY")
RAWG_API_KEY = os.getenv("RAWG_API_KEY")