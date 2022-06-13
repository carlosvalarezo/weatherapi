class Weather:

    def __init__(self) -> None:
        self.location_name = ''
        self.temperature = ''
        self.wind = ''
        self.cloudiness = ''
        self.pressure = ''
        self.humidity = ''
        self.sunrise = ''
        self.sunset = ''
        self.geo_coordinates = ''

    def set_location(self, location: str) -> None:
        self.location_name = location

    def set_temperature(self, temperature: str) -> None:
        self.temperature = temperature

    def set_wind(self, wind: str) -> None:
        self.wind = wind

    def set_cloudiness(self, cloudiness: str) -> None:
        self.cloudiness = cloudiness

    def set_pressure(self, pressure: str ) -> None:
        self.pressure = pressure

    def set_humidity(self, humidity: str) -> None:
        self.humidity = humidity

    def set_sunrise(self, sunrise: str) -> None:
        self.sunrise = sunrise

    def set_sunset(self, sunset: str) -> None:
        self.sunset = sunset

    def set_geo_coordinates(self, geo_coordinates: str) -> None:
        self.geo_coordinates = geo_coordinates


