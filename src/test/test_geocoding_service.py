import pytest
from unittest.mock import patch
from ..main.python.services import geocoding_service

def test_get_coordinates_calls_get_response():
    with patch.object(geocoding_service, 'get_response') as mock_get_response:
        geocoding_service.get_coordinates('some address')
        mock_get_response.assert_called_once_with('some address')


@pytest.mark.parametrize(
    'response_json, expected',
    [
        (
            {'results': [{'geometry': {'lat': 52.23, 'lng': 21.01}}]},
            {'lat': 52.23, 'lng': 21.01}
        ),
        (
            {'results': [{'geometry': {'lat': 52.23}}]},
            {'lat': 52.23, 'lng': None}
        ),
        (
            {'results': [{'geometry': {'lng': 21.01}}]},
            {'lat': None, 'lng': 21.01}
        ),
        (
            {'results': []},
            {'lat': None, 'lng': None}
        ),
        (
            None,
            {'lat': None, 'lng': None}
        )
    ]
)
def test_extract_coordinates(response_json, expected):
    assert geocoding_service.extract_coordinates(response_json) == expected

@pytest.mark.parametrize('response', [
    None,
    {},
    {'results': []},
    {'results': [{}]},
    {'results': [{'geometry': {}}]}
])
def test_extract_coordinates_invalid(response):
    result = geocoding_service.extract_coordinates(response)
    assert result == {'lat': None, 'lng': None}
    
def test_get_coordinates_real_api_call():
    result = geocoding_service.get_coordinates('London')
    assert isinstance(result, dict)
    assert 'lat' in result
    assert 'lng' in result
    assert result['lat'] is None or isinstance(result['lat'], float)
    assert result['lng'] is None or isinstance(result['lng'], float)