import pytest
from api.adapters.weather import WeatherAdapter
from api.services.weather import WeatherService


class MockWeatherDataResponse:
    @staticmethod
    def get_weather_data():
        return {"mock_key": "mock_response"}


@pytest.fixture(autouse=True)
def mock_response(monkeypatch):
    def get_weather_data(*args, **kwargs):
        return MockWeatherDataResponse().get_weather_data()

    monkeypatch.setattr(WeatherAdapter, "get_weather_data", get_weather_data)


def test_get_weather_data():
    result = WeatherService.get_weather_data("https://myfavurl")
    assert result['mock_key'] == 'mock_response'
