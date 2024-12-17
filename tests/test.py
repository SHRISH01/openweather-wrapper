from openweather.weather import OpenWeather

api_key = "Your API Key"
weather_api = OpenWeather(api_key)

weather_api.plot_weather(city="Delhi")