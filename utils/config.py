import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
    BASE_URL = os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", 10000))
    VALID_USER_EMAIL=str(os.getenv("VALID_USER_EMAIL", "customer@practicesoftwaretesting.com"))
    VALID_USER_PASSWORD=str(os.getenv("VALID_USER_PASSWORD", "welcome01"))