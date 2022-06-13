import requests

from api.adapters.weather import WeatherAdapter


class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


def test_request_weather_data(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = WeatherAdapter.get_weather_data("https://myweatherservice")
    assert result["mock_key"] == "mock_response"
