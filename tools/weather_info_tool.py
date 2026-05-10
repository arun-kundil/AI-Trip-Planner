import os
from typing import Any, Dict, Optional, List
from dotenv import load_dotenv
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool

class WeatherInfoTool():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self.__setup_tools()

    def __setup_tools(self) -> List:
        """Setup the weather tools."""
        @tool
        def get_current_weather(city: str) -> str:
            """Get the current weather for a given city."""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp_kelvin = weather_data.get("main", {}).get("temp", "N/A")
                if temp_kelvin != "N/A":
                    temp_celsius = round(temp_kelvin - 273.15, 1)
                else:
                    temp_celsius = "N/A"
                desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
                return f"The current weather in {city} is {desc} with a temperature of {temp_celsius}°C."
            return f"Sorry, I couldn't fetch the weather data for {city}."

        @tool
        def get_weather_forecast(city: str) -> str:
            """Get the weather forecast for a given location."""
            forecast_data = self.weather_service.get_weather_forecast(city)
            if forecast_data and "list" in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data["list"])):
                    item = forecast_data["list"][i]
                    date = item['dt_txt'].split(" ")[0]
                    temp_kelvin = item['main']['temp']
                    temp_celsius = round(temp_kelvin - 273.15, 1)
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {desc}, {temp_celsius}°C")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Sorry, I couldn't fetch the weather forecast for {city}."
        return [get_current_weather, get_weather_forecast]
