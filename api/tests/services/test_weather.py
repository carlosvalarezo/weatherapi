from services.weather import WeatherService


class TestWeatherService:
    def test_request_weather_data(self):
        weather_service = WeatherService()
        assert isinstance(weather_service, WeatherService)



