import pytest
import requests

from api.adapters.weather import WeatherAdapter
from api.errors.endpoint_not_found import EndpointNotSetError


class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


@pytest.fixture
def mock_weather_endpoint_missing(monkeypatch):
    monkeypatch.delenv("WEATHER_ENDPOINT", raising=False)


@pytest.fixture
def mock_weather_endpoint(monkeypatch):
    monkeypatch.setenv("WEATHER_ENDPOINT", "https://mygreatendpoint.com")


@pytest.fixture
def mock_get_request(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_not_get_request(monkeypatch):
    monkeypatch.delattr(requests, "get", raising=True)


def test_request_weather_data(mock_get_request, mock_weather_endpoint):
    weather_adapter = WeatherAdapter()
    result = weather_adapter.get_weather_data()
    assert result["mock_key"] == "mock_response"


def test_should_raise_EndpointNotSetError_on_endpoint_missing(mock_not_get_request, mock_weather_endpoint_missing):
    weather_adapter = WeatherAdapter()
    with pytest.raises(EndpointNotSetError):
        _ = weather_adapter.get_weather_data()
        print(f"ABC = {_}")
