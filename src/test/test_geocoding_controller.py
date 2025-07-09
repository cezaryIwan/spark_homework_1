import requests
from ..main.python.geocoding_controller import get_response
def test_get_response_valid_address(monkeypatch):
    mock_response = {
        'results': [{
            'geometry': {
                'lat': 52.2297,
                'lng': 21.0122
            }
        }]
    }

    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def raise_for_status(self): pass
        def json(self): return mock_response

    monkeypatch.setattr('requests.get', lambda url, params: MockResponse())

    result = get_response('Warsaw, Poland')

    assert result == mock_response


def test_get_response_api_failure(monkeypatch):
    def mock_requests_get(url, params):
        raise requests.RequestException('API error')

    monkeypatch.setattr('requests.get', mock_requests_get)

    invalid_address = 'invalid adress'
    result = get_response(invalid_address)

    assert result is None

def test_get_response_real_api_call():
    address = 'Berlin, Germany'

    result = get_response(address)

    assert result is not None, 'API returned None'
    assert 'results' in result, "'results' key not in response"
    assert len(result['results']) > 0, 'No results in response'

    geometry = result['results'][0].get('geometry', {})
    assert 'lat' in geometry and 'lng' in geometry, 'Coordinates not found in response'

