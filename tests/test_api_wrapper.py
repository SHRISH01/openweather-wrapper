import unittest
from unittest.mock import patch, MagicMock
from openweather.weather import OpenWeather, OpenWeatherError

class TestOpenWeather(unittest.TestCase):

    @patch('requests.get')
    def test_get_weather_by_city(self, mock_get):
        """Test getting current weather data by city name."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 285.15}
        }
        mock_get.return_value = mock_response
        
        api = OpenWeather(api_key="mock_api_key")
        weather = api.get_weather(city="London")
        self.assertEqual(weather["weather"][0]["description"], "clear sky")
        self.assertEqual(weather["main"]["temp"], 285.15)
    
    @patch('requests.get')
    def test_get_weather_by_coordinates(self, mock_get):
        """Test getting current weather data by GPS coordinates."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 285.15}
        }
        mock_get.return_value = mock_response
        
        api = OpenWeather(api_key="mock_api_key")
        weather = api.get_weather(lat=51.5074, lon=-0.1278)
        self.assertEqual(weather["weather"][0]["description"], "clear sky")
        self.assertEqual(weather["main"]["temp"], 285.15)

    @patch('requests.get')
    def test_get_hourly_forecast(self, mock_get):
        """Test getting hourly weather forecast."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "list": [{"dt_txt": "2024-12-18 12:00:00", "main": {"temp": 285.15}}]
        }
        mock_get.return_value = mock_response
        
        api = OpenWeather(api_key="mock_api_key")
        hourly_forecast = api.get_hourly_forecast(city="London")
        self.assertEqual(len(hourly_forecast), 1)
        self.assertEqual(hourly_forecast[0]["dt_txt"], "2024-12-18 12:00:00")

    @patch('requests.get')
    def test_get_seven_day_forecast(self, mock_get):
        """Test getting 7-day weather forecast."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "list": [{"dt_txt": "2024-12-18 12:00:00", "main": {"temp": 285.15}}]
        }
        mock_get.return_value = mock_response
        
        api = OpenWeather(api_key="mock_api_key")
        seven_day_forecast = api.get_seven_day_forecast(city="London")
        self.assertEqual(len(seven_day_forecast), 1)
        self.assertEqual(seven_day_forecast[0]["dt_txt"], "2024-12-18 12:00:00")

    @patch('requests.get')
    def test_plot_weather(self, mock_get):
        """Test plotting the weather data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "list": [{"dt_txt": "2024-12-18 12:00:00", "main": {"temp": 285.15}}]
        }
        mock_get.return_value = mock_response
        
        api = OpenWeather(api_key="mock_api_key")
        try:
            api.plot_weather(city="London")
        except Exception as e:
            self.fail(f"plot_weather raised Exception unexpectedly: {e}")

if __name__ == '__main__':
    unittest.main()
