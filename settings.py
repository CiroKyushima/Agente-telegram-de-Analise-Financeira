import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    BOT_NAME = os.getenv("BOT_NAME", "BolsaIA_Bot")
    MODEL_NAME = "gpt-4-turbo-preview"

settings = Settings()