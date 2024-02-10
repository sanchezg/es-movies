import os

from dotenv import load_dotenv

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load minimum env vars needed for .env
env = os.environ.get("ENV", "LOCAL").lower()

# Load .env before other settings to properly set environment defaults from the
# config (those not already set at the OS/instance)
dotenv_path = BASE_DIR + "/config/.env." + env
load_dotenv(dotenv_path=dotenv_path)

BASE_URL = os.environ.get("BASE_URL")

IS_PROD_ENV = env == "prod"
IS_LOCAL_ENV = env == "local"
IS_DEV_ENV = env == "dev"

ES_URI = os.environ.get("ES_URI", "docdb:9200")
