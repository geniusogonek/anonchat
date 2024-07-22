import os

from dotenv import load_dotenv

load_dotenv()


DB_CONNECTION = os.getenv("DB_CONNECTION")
JWT_SECRET = os.getenv("JWT_SECRET")