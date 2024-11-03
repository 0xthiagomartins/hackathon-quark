import os
from dotenv import load_dotenv

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
print(f"load env: {load_dotenv(dotenv_path=f"./resources/.env")}")
CLOUD_AMQP = os.environ.get("CLOUD_AMQP", "amqp://guest:guest@localhost:5672")
SQL_URI = os.environ.get("SQL_URI", "amqp://guest:guest@localhost:5672")
