from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv


ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
print(f"load env: {load_dotenv(dotenv_path=f"./resources/.env")}")

SQL_URI = os.environ.get("SQL_URI", None)


PASSWORD_SALT = os.environ.get("PASSWORD_SALT")
SYSTEM_ENCRYPT_KEY = os.environ.get("SYSTEM_ENCRYPT_KEY")
SIGNING_KEY = os.environ.get("SIGNING_KEY")


def generate_encrypt_key():
    return Fernet.generate_key()
