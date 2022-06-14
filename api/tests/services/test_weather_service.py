import pytest

from faker import Faker

from api.routes.weather import WeatherAPIAdapter, WeatherService

fake = Faker('es_CO')


class MockWeatherDataResponse:
    @staticmethod
    def get_weather_data(city, country):
        return {"mock_key": "mock_response"}


@pytest.fixture(autouse=True)
def mock_response(monkeypatch):
    def get_weather_data(*args, **kwargs):
        city = fake.city()
        country = fake.country_code()
        return MockWeatherDataResponse().get_weather_data(city, country)

    monkeypatch.setattr(WeatherAPIAdapter, "get_weather_data", get_weather_data)


def test_get_weather_data():
    city = fake.city()
    country = fake.country_code()
    result = WeatherService.get_weather_data(city, country)
    assert result['mock_key'] == 'mock_response'
