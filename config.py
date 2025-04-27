import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
