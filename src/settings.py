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

ES_URI = os.environ.get("ES_URI", "http://docdb:9200")
ES_CHUNK_SIZE = int(os.environ.get("ES_CHUNK_SIZE", 10000))  # keep it high because docs are lightweight
ES_MAX_SIZE = int(os.environ.get("ES_MAX_SIZE", 1000))  # keep it high because docs are lightweight

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "default": {"handlers": ["default"], "level": "DEBUG"},
    },
}
