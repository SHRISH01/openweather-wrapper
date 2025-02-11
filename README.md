# OpenWeather Wrapper

`OpenWeather Wrapper` is a Python package that provides an easy-to-use interface for interacting with various weather APIs like OpenWeatherMap and WeatherStack. It allows users to retrieve current weather data, hourly forecasts, and 7-day weather forecasts for a specified city or geographical coordinates (latitude and longitude). The package also supports data caching, error handling, and data visualization.

## Features

- **Weather Data Fetching**: Fetch current weather data by city name or geographical coordinates (latitude/longitude).
- **Hourly Forecast**: Retrieve hourly weather forecast data for the next 24 hours.
- **7-Day Forecast**: Get the 7-day weather forecast.
- **Error Handling**: Custom error handling for API-related issues.
- **Data Caching**: Cache weather data to reduce API calls using `requests_cache`.
- **Data Visualization**: Plot temperature data for the next 24 hours using `matplotlib`.

## Installation 

<pre><code>pip install openweather-wrapper</pre></code>



### Option 2: Install from GitHub (for local development)
<pre><code>git clone https://github.com/yourusername/openweather-wrapper.git
cd openweather-wrapper
pip install .</pre></code>

## Requirements

* Python 3.6 or higher
* requests
* requests_cache
* matplotlib

You can install the required dependencies using pip:

<pre><code>pip install -r requirements.txt</pre></code>

## Usage

#### Initialize the OpenWeather class

To use the package, you'll need to initialize the OpenWeather class with your API key. You can get your API key by signing up at OpenWeatherMap or WeatherStack.

<pre><code>from openweather.weather import OpenWeather
# Initialize the OpenWeather class with your API key
api_key = "your_api_key_here"
weather_api = OpenWeather(api_key)
</pre></code>

#### Get Current Weather Data
You can fetch current weather data by either providing a city name or geographical coordinates (latitude and longitude).

##### By City Name:

<pre><code>weather = weather_api.get_weather(city="London")
print(weather)</pre></code>

##### By Latitude and Longitude:

<pre><code>weather = weather_api.get_weather(lat=51.5074, lon=-0.1278)  # Coordinates for London
print(weather)</pre></code>

#### Get Hourly Forecast (Next 24 Hours)

<pre><code>hourly_forecast = weather_api.get_hourly_forecast(city="Delhi")
print(hourly_forecast)</pre></code>

#### Get 7-Day Forecast

<pre><code>seven_day_forecast = weather_api.get_seven_day_forecast(city="London")
print(seven_day_forecast)</pre></code>

#### Plot Weather Data (Temperature)

<pre><code>weather_api.plot_weather(city="Delhi")</code></pre>

---

### Caching

The package uses requests_cache to cache API responses for a specified duration. This reduces the number of requests made to the API and improves performance for subsequent calls. The default cache duration is 1 hour (3600 seconds), but you can modify it when initializing the class.

<pre><code>weather_api = OpenWeather(api_key="your_api_key_here", cache_duration=3600)  # 1 hour cache duration</pre></code>

### License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Contributing

We welcome contributions! If you would like to contribute to this project, please fork the repository and submit a pull request. Make sure to follow the coding guidelines and write tests for any new functionality.

## Contact

For any questions or support, feel free to open an issue on the GitHub repository or contact us directly at <span style="color:green">shrishkamboz@gmail.com</span>.
