import os
from dotenv import load_dotenv

load_dotenv()

def get_config(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)
