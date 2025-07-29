from geocoding_controller import get_response

def get_coordinates(address: str) -> dict[str, float] | None:
    response = get_response(address)
    return extract_coordinates(response)

def extract_coordinates(response_json: dict | None) -> dict[str, float] | None:
    coordinates = {}
    if response_json and response_json.get('results'):
        coordinates = response_json['results'][0].get('geometry', {})
    return {'lat': coordinates.get('lat'), 'lng': coordinates.get('lng')}