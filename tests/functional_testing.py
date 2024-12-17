import pytest
from openweather.weather import OpenWeather, OpenWeatherError

# Mock response using pytest's monkeypatch
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    
    def json(self):
        return self.json_data

@pytest.fixture
def openweather_instance():
    api_key = "API"
    return OpenWeather(api_key)

def test_get_weather_success(monkeypatch, openweather_instance):
    def mock_get(*args, **kwargs):
        return MockResponse({"main": {"temp": 300}, "coord": {"lat": 10, "lon": 20}}, 200)
    
    monkeypatch.setattr("requests.get", mock_get)
    response = openweather_instance.get_weather(city="TestCity")
    assert response["main"]["temp"] == 300

def test_get_weather_failure(monkeypatch, openweather_instance):
    def mock_get(*args, **kwargs):
        return MockResponse({}, 404)
    
    monkeypatch.setattr("requests.get", mock_get)
    with pytest.raises(OpenWeatherError):
        openweather_instance.get_weather(city="InvalidCity")


def test_get_hourly_forecast(monkeypatch, openweather_instance):
    def mock_get(*args, **kwargs):
        return MockResponse({"list": [{"dt_txt": "2024-06-01 12:00:00", "main": {"temp": 298}}]}, 200)
    
    monkeypatch.setattr("requests.get", mock_get)
    response = openweather_instance.get_hourly_forecast(city="TestCity")
    assert len(response) == 1
    assert response[0]["main"]["temp"] == 298

def test_plot_weather(monkeypatch, openweather_instance):
    def mock_get(*args, **kwargs):
        return MockResponse({"list": [{"dt_txt": "2024-06-01 12:00:00", "main": {"temp": 298}}]}, 200)
    
    monkeypatch.setattr("requests.get", mock_get)
    try:
        openweather_instance.plot_weather(city="TestCity")
    except Exception as e:
        pytest.fail(f"plot_weather raised an exception: {e}")

def test_invalid_temperature_conversion():
    with pytest.raises(ValueError):
        OpenWeather.convert_temperature(300, 'X', 'Y')
