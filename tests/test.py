from openweather.weather import OpenWeather

api_key = "2c93339e7879008704993fef099aba90"
weather_api = OpenWeather(api_key)

weather_api.create_weather_alert_notification('Delhi')
