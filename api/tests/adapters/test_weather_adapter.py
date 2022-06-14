import pytest
import requests
from faker import Faker

from api.adapters.api import WeatherAPIAdapter
from api.errors.api_key_not_set import ApiKeyNotSetError
from api.errors.endpoint_not_set import EndpointNotSetError

fake = Faker()


class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


@pytest.fixture
def mock_get_request(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_not_get_request(monkeypatch):
    monkeypatch.delattr(requests, "get", raising=True)


@pytest.fixture
def mock_weather_endpoint(monkeypatch):
    monkeypatch.setenv("WEATHER_ENDPOINT", "https://mygreatendpoint.com")


@pytest.fixture
def mock_weather_api_key(monkeypatch):
    monkeypatch.setenv("WEATHER_APP_ID", "MY_API_ID")


@pytest.fixture
def mock_weather_endpoint_missing(monkeypatch):
    monkeypatch.delenv("WEATHER_ENDPOINT", raising=False)


@pytest.fixture
def mock_weather_api_key_missing(monkeypatch):
    monkeypatch.delenv("WEATHER_APP_ID", raising=False)


def test_request_weather_data(mock_get_request, mock_weather_endpoint, mock_weather_api_key):
    weather_adapter = WeatherAPIAdapter()
    city = fake.city()
    country = fake.country_code()
    result = weather_adapter.get_weather_data(city, country)
    assert result["mock_key"] == "mock_response"


def test_should_raise_EndpointNotSetError_on_endpoint_missing(mock_not_get_request,
                                                              mock_weather_endpoint_missing,
                                                              mock_weather_api_key):
    weather_adapter = WeatherAPIAdapter()
    with pytest.raises(EndpointNotSetError):
        city = fake.city()
        country = fake.country_code()
        _ = weather_adapter.get_weather_data(city, country)


def test_should_raise_APIKeyNotSetError_on_api_key_missing(mock_not_get_request,
                                                           mock_weather_endpoint,
                                                           mock_weather_api_key_missing):
    weather_adapter = WeatherAPIAdapter()
    with pytest.raises(ApiKeyNotSetError):
        city = fake.city()
        country = fake.country_code()
        _ = weather_adapter.get_weather_data(city, country)
