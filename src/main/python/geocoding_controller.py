import requests

from config import get_config

def get_response(address: str) -> dict | None:
    endpoint = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": address,
        "key": get_config("OPENCAGE_API_KEY"),
        "limit": 1,
        "no_annotations": 1
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
