import requests
import requests_cache
import matplotlib.pyplot as plt

class OpenWeatherError(Exception):
    """Custom exception for OpenWeather API errors."""
    pass

class OpenWeather:
    def __init__(self, api_key, source="openweathermap", cache_duration=3600):
        self.api_key = api_key
        self.source = source.lower()
        
        # Enable caching
        requests_cache.install_cache("weather_cache", expire_after=cache_duration)
        
        # Define base URLs for different APIs
        self.base_urls = {
            "openweathermap": "http://api.openweathermap.org/data/2.5/weather",
            "weatherstack": "http://api.weatherstack.com/current",
            "forecast": "http://api.openweathermap.org/data/2.5/forecast"
        }
    
    def get_weather(self, city=None, lat=None, lon=None):
        """Fetch current weather data based on city name or latitude/longitude."""
        if not city and (lat is None or lon is None):
            raise OpenWeatherError("Must provide either a city or latitude/longitude")
        
        url = self.base_urls.get(self.source, None)
        if not url:
            raise OpenWeatherError("Unsupported weather source")
        
        params = {"appid": self.api_key}
        if city:
            params["q"] = city
        if lat and lon:
            params["lat"] = lat
            params["lon"] = lon
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise OpenWeatherError(f"Error fetching weather data: {response.status_code}")
        
        return response.json()

    def get_hourly_forecast(self, city):
        """Fetch hourly forecast for the next 24 hours."""
        url = self.base_urls["forecast"]
        params = {"q": city, "appid": self.api_key}
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise OpenWeatherError(f"Error fetching hourly forecast: {response.status_code}")
        
        return response.json().get("list", [])

    def get_seven_day_forecast(self, city):
        """Fetch 7-day forecast data."""
        url = self.base_urls["forecast"]
        params = {"q": city, "cnt": 7, "appid": self.api_key}
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise OpenWeatherError(f"Error fetching 7-day forecast: {response.status_code}")
        
        return response.json().get("list", [])

    def plot_weather(self, city):
        """Plot temperature data for the next 24 hours."""
        hourly_data = self.get_hourly_forecast(city)
        if not hourly_data:
            raise OpenWeatherError("No hourly data available.")
        
        times = [data["dt_txt"] for data in hourly_data]
        temperatures = [data["main"]["temp"] for data in hourly_data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(times, temperatures, marker='o')
        plt.xticks(rotation=45)
        plt.title(f"24-hour Weather Forecast for {city}")
        plt.xlabel("Time")
        plt.ylabel("Temperature (K)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

