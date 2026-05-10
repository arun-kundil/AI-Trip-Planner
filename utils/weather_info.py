import requests

class WeatherForecastTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/"

    def get_current_weather(self, place: str):
        """Fetch current weather data for a given location."""
        try:
            url = f"{self.base_url}weather"
            params = {
                "q": place,
                "appid": self.api_key,
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching current weather: {e}")
            raise e
        
    def get_weather_forecast(self, place: str):
        """Fetch weather forecast data for a given location."""
        try:
            url = f"{self.base_url}forecast"
            params = {
                "q": place,
                "appid": self.api_key,
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching weather forecast: {e}")
            raise e