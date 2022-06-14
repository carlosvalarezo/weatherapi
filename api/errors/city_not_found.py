from api.errors.weather import WeatherError


class CityNotFoundException(WeatherError):
    def __init__(self, error, status_code):
        super().__init__(error, status_code)
