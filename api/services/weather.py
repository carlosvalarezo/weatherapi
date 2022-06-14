from api.adapters.api import WeatherAPIAdapter


class WeatherService:
    @staticmethod
    def get_weather_data(city, country):
        return WeatherAPIAdapter.get_weather_data(city, country)
