import pytest
import requests
from faker import Faker


from api.routes.weather import WeatherAPIAdapter, ApiKeyNotSetError, EndpointNotSetError
from api.routes.weather import CityNotFoundException, CountryNotFoundException, WeatherService


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


def mock_valid_city():
    return fake.city()


def mock_valid_country():
    return fake.country_code()


def test_request_weather_data(mock_get_request, mock_weather_endpoint, mock_weather_api_key):
    weather_adapter = WeatherAPIAdapter()
    city = mock_valid_city()
    country = mock_valid_country()
    result = weather_adapter.get_weather_data(city, country)
    assert result["mock_key"] == "mock_response"


def test_should_rise_CityNotFoundException_on_missing_city(mock_get_request, mock_weather_endpoint, mock_weather_api_key):
    with pytest.raises(CityNotFoundException):
        weather_service = WeatherService()
        city = None
        country = mock_valid_country()
        _ = weather_service.get_weather_data(city, country)


def test_should_rise_CountryNotFoundException_on_missing_city(mock_get_request, mock_weather_endpoint, mock_weather_api_key):
    with pytest.raises(CountryNotFoundException):
        weather_service = WeatherService()
        city = mock_valid_city()
        country = None
        _ = weather_service.get_weather_data(city, country)


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
