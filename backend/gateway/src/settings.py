import os
from dotenv import load_dotenv

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
print(f"load env: {load_dotenv(dotenv_path=f"./resources/.env")}")
CLOUD_AMQP = os.environ.get("CLOUD_AMQP", "amqp://guest:guest@localhost:5672")
OPEN_API_PATH = os.environ.get("OPEN_API_PATH", "/openapi.json")
TOKEN_COOKIE_NAME = os.environ.get("TOKEN_COOKIE_NAME", "__quark_cookie")
