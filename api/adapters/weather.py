import requests


class WeatherAdapter:
    @staticmethod
    def get_weather_data(url):
        r = requests.get(url)
        return r.json()
