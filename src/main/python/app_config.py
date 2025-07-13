import os

def load_config(keys: list[str]) -> dict[str, str | None]:
    return {key: os.getenv(key) for key in keys}

CONFIG_KEYS = [
    'AZURE_STORAGE_ACCOUNT_NAME',
    'AZURE_STORAGE_ACCOUNT_KEY',
    'AZURE_CONTAINER_NAME',
    'AES_ENCRYPTION_KEY',
    'STORAGE_PATH',
    'STORAGE_WEATHER_SUBPATH',
    'STORAGE_HOTELS_SUBPATH',
    'OPENCAGE_API_KEY'
]

app_config = load_config(CONFIG_KEYS)