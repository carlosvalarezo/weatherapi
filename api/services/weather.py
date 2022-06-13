from api.adapters.weather import WeatherAdapter


class WeatherService:
    @staticmethod
    def get_weather_data(url):
        return WeatherAdapter.get_weather_data(url)
