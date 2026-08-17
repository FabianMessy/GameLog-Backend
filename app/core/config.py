import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/db_Gamelog"
    SECRET_KEY = os.getenv("SECRET_KEY")
    RAWG_API_KEY = os.getenv("RAWG_API_KEY")

settings = Settings()