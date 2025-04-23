# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Firebase
FIREBASE_CREDENTIALS_PATH = "certificates/db-connection-private-key.json"

# CSV
CSV_FILE_PATH = "CSV/inscriptions.csv"
CSV_COLUMNS = ["name", "surname", "email", "phone", "dni"]

# Email
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_FROM = "SUGUS"
EMAIL_SUBJECT = "ENTRADA 47CON 2025"

# Secret
SECRET_KEY = os.getenv("SECRET_KEY")

# Assets
BANNER_IMAGE_PATH = "assets/imgs/banner_sugus.png"

# Consola
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"