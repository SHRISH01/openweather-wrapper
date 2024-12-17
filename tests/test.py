from openweather.weather import OpenWeather

api_key = "Your API Key"
weather_api = OpenWeather(api_key)

result = weather_api.convert_temperature(300, 'K', 'C')
print(result)