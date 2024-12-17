import requests
import requests_cache
import matplotlib.pyplot as plt
import numpy as np

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

    @staticmethod
    def convert_temperature(temp, from_unit='K', to_unit='C'):
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()
        if from_unit == to_unit:
            return temp
        if from_unit == 'K':
            if to_unit == 'C':
                return temp - 273.15
            elif to_unit == 'F':
                return (temp - 273.15) * 9/5 + 32     
        elif from_unit == 'C':
            if to_unit == 'K':
                return temp + 273.15
            elif to_unit == 'F':
                return temp * 9/5 + 32      
        elif from_unit == 'F':
            if to_unit == 'K':
                return (temp - 32) * 5/9 + 273.15
            elif to_unit == 'C':
                return (temp - 32) * 5/9 
        raise ValueError(f"Invalid temperature units. Use 'K', 'C', or 'F'. Got {from_unit} and {to_unit}")
    
    def plot_detailed_forecast(self, city):
        import matplotlib.pyplot as plt
        
        hourly_data = self.get_hourly_forecast(city)
        if not hourly_data:
            raise OpenWeatherError("No hourly data available.")
        
        # Extract data
        times = [data['dt_txt'] for data in hourly_data]
        temperatures = [data['main']['temp'] for data in hourly_data]
        feels_like = [data['main']['feels_like'] for data in hourly_data]
        humidity = [data['main']['humidity'] for data in hourly_data]
        wind_speeds = [data['wind']['speed'] for data in hourly_data]
        
        # Create a multi-subplot figure
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
        
        # Temperature subplot
        ax1.plot(times, temperatures, marker='o', label='Temperature (K)')
        ax1.plot(times, feels_like, marker='x', label='Feels Like (K)')
        ax1.set_title(f"Detailed Weather Forecast for {city}")
        ax1.set_ylabel("Temperature")
        ax1.legend()
        ax1.grid(True)
        
        # Humidity subplot
        ax2.plot(times, humidity, marker='o', color='green')
        ax2.set_ylabel("Humidity (%)")
        ax2.grid(True)
        
        # Wind speed subplot
        ax3.plot(times, wind_speeds, marker='o', color='red')
        ax3.set_ylabel("Wind Speed (m/s)")
        ax3.set_xlabel("Time")
        ax3.grid(True)
        
        # Rotate and align the tick labels
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        
        # Adjust layout and display
        plt.tight_layout()
        plt.show()
  
    def compare_city_weather(self, cities):
        weather_comparisons = {}
        
        for city in cities:
            try:
                weather_data = self.get_weather(city)
                weather_comparisons[city] = {
                    'temperature': weather_data['main']['temp'],
                    'feels_like': weather_data['main']['feels_like'],
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'description': weather_data['weather'][0]['description']
                }
            except OpenWeatherError as e:
                weather_comparisons[city] = {'error': str(e)}
        
        return weather_comparisons

    def get_nearby_cities_weather(self, lat, lon, radius=50):
        try:
            nearby_cities = self._find_nearby_cities(lat, lon, radius)
            nearby_weather = []
            
            for city in nearby_cities:
                try:
                    city_weather = self.get_weather(city)
                    nearby_weather.append({
                        'city': city,
                        'weather': city_weather
                    })
                except OpenWeatherError:
                    continue
            
            return nearby_weather
        except Exception as e:
            raise OpenWeatherError(f"Error finding nearby cities: {str(e)}")

    def _find_nearby_cities(self, lat, lon, radius):
        return [
            "New York", "Jersey City", "Newark", 
            "Brooklyn", "Queens", "Bronx"
        ]
    def get_air_quality(self, city=None, lat=None, lon=None):
        aqi_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        
        # Determine location parameters
        if city:
            # First, get coordinates for the city
            city_data = self.get_weather(city)
            lat = city_data['coord']['lat']
            lon = city_data['coord']['lon']
        
        if lat is None or lon is None:
            raise OpenWeatherError("Must provide either a city or latitude/longitude")
        
        # Parameters for AQI request
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key
        }
        
        # Make API request
        response = requests.get(aqi_url, params=params)
        
        if response.status_code != 200:
            raise OpenWeatherError(f"Error fetching air quality data: {response.status_code}")
        
        # Process and interpret AQI data
        aqi_data = response.json()
        
        # Extract main AQI information
        if not aqi_data.get('list'):
            raise OpenWeatherError("No air quality data available")
        
        aqi_details = aqi_data['list'][0]
        
        # Interpret AQI components
        components = aqi_details.get('components', {})
        aqi_level = aqi_details.get('main', {}).get('aqi')
        
        # AQI level interpretation
        aqi_interpretations = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        
        return {
            'aqi_level': aqi_level,
            'aqi_description': aqi_interpretations.get(aqi_level, "Unknown"),
            'components': {
                'carbon_monoxide': components.get('co', 0),
                'nitrogen_monoxide': components.get('no', 0),
                'nitrogen_dioxide': components.get('no2', 0),
                'ozone': components.get('o3', 0),
                'sulfur_dioxide': components.get('so2', 0),
                'fine_particles_pm2_5': components.get('pm2_5', 0),
                'fine_particles_pm10': components.get('pm10', 0),
                'ammonia': components.get('nh3', 0)
            }
        }

    def plot_air_quality_trend(self, city):
        hourly_data = self.get_hourly_forecast(city)
        if not hourly_data:
            raise OpenWeatherError("No hourly data available for air quality analysis")
        first_data = hourly_data[0]
        lat = first_data['coord']['lat']
        lon = first_data['coord']['lon']
        times = []
        pm25_values = []
        pm10_values = []
        o3_values = []
        
        for data_point in hourly_data:
            try:
                aqi_data = self.get_air_quality(lat=lat, lon=lon)
                times.append(data_point['dt_txt'])
                pm25_values.append(aqi_data['components']['fine_particles_pm2_5'])
                pm10_values.append(aqi_data['components']['fine_particles_pm10'])
                o3_values.append(aqi_data['components']['ozone'])
            except Exception:
                continue
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(times, pm25_values, label='PM2.5', marker='o')
        plt.plot(times, pm10_values, label='PM10', marker='x')
        plt.plot(times, o3_values, label='Ozone', marker='^')
        
        plt.title(f"Air Quality Components Trend for {city}")
        plt.xlabel("Time")
        plt.ylabel("Concentration")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def get_weather_alerts(self, city=None, lat=None, lon=None):
        # Note: This uses OpenWeatherMap's One Call API (requires different endpoint)
        alerts_url = "https://api.openweathermap.org/data/2.5/onecall"
        
        # Determine location parameters
        if city:
            # First, get coordinates for the city
            city_data = self.get_weather(city)
            lat = city_data['coord']['lat']
            lon = city_data['coord']['lon']
        
        if lat is None or lon is None:
            raise OpenWeatherError("Must provide either a city or latitude/longitude")
        
        # Parameters for alerts request
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "exclude": "current,minutely,hourly,daily"  # Focus on alerts
        }
        
        # Make API request
        response = requests.get(alerts_url, params=params)
        
        if response.status_code != 200:
            raise OpenWeatherError(f"Error fetching weather alerts: {response.status_code}")
        
        # Process alerts data
        alerts_data = response.json()
        
        # Extract and process alerts
        alerts = alerts_data.get('alerts', [])
        
        processed_alerts = []
        for alert in alerts:
            processed_alerts.append({
                'event': alert.get('event', 'Unknown Event'),
                'start': alert.get('start'),
                'end': alert.get('end'),
                'description': alert.get('description', 'No additional details'),
                'severity': self._interpret_alert_severity(alert.get('severity'))
            })
        
        return {
            'total_alerts': len(processed_alerts),
            'alerts': processed_alerts
        }

    def _interpret_alert_severity(self, severity):
        severity_map = {
            'extreme': 'Extreme Danger - Immediate Action Required',
            'severe': 'Severe - Take Precautions',
            'moderate': 'Moderate - Stay Informed',
            'minor': 'Minor - Monitor Conditions',
            'unknown': 'Unknown Severity'
        }
        
        return severity_map.get(severity.lower(), 'Unknown Severity')

    def create_weather_alert_notification(self, city):
        try:
            alerts = self.get_weather_alerts(city)
            
            if alerts['total_alerts'] == 0:
                return f"No active weather alerts for {city}. Stay safe!"
            
            # Construct detailed alert message
            alert_message = f"⚠️ WEATHER ALERTS FOR {city.upper()} ⚠️\n\n"
            alert_message += f"Total Active Alerts: {alerts['total_alerts']}\n\n"
            
            for i, alert in enumerate(alerts['alerts'], 1):
                alert_message += f"Alert {i}:\n"
                alert_message += f"Event: {alert['event']}\n"
                alert_message += f"Severity: {alert['severity']}\n"
                alert_message += f"Description: {alert['description']}\n"
                alert_message += f"Start: {alert['start']}\n"
                alert_message += f"End: {alert['end']}\n\n"
            
            return alert_message
        
        except Exception as e:
            return f"Unable to retrieve weather alerts: {str(e)}"
        
    def get_historical_weather(self, city, date):
    
        historical_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
        
        city_data = self.get_weather(city)
        lat = city_data['coord']['lat']
        lon = city_data['coord']['lon']
        
        # Convert date to Unix timestamp
        timestamp = int(date.timestamp())
        
        params = {
            "lat": lat,
            "lon": lon,
            "dt": timestamp,
            "appid": self.api_key
        }
        
        response = requests.get(historical_url, params=params)
        
        if response.status_code != 200:
            raise OpenWeatherError(f"Error fetching historical weather data: {response.status_code}")
        
        historical_data = response.json()
        
        return {
            'temperature': historical_data.get('current', {}).get('temp'),
            'feels_like': historical_data.get('current', {}).get('feels_like'),
            'humidity': historical_data.get('current', {}).get('humidity'),
            'wind_speed': historical_data.get('current', {}).get('wind_speed'),
            'weather_description': historical_data.get('current', {}).get('weather', [{}])[0].get('description')
        }

    def compare_climate_trends(self, city, base_year, comparison_year):
        from datetime import datetime, timedelta
        
        def get_yearly_average(year):
            yearly_temps = []
            for month in range(1, 13):
                try:
                    sample_date = datetime(year, month, 15)
                    historical_data = self.get_historical_weather(city, sample_date)
                    yearly_temps.append(historical_data['temperature'])
                except Exception:
                    continue
            
            return {
                'average_temperature': sum(yearly_temps) / len(yearly_temps) if yearly_temps else None,
                'total_samples': len(yearly_temps)
            }
        
        base_year_data = get_yearly_average(base_year)
        comparison_year_data = get_yearly_average(comparison_year)

        temp_change = None
        if base_year_data['average_temperature'] and comparison_year_data['average_temperature']:
            temp_change = comparison_year_data['average_temperature'] - base_year_data['average_temperature']
        
        return {
            'city': city,
            'base_year': {
                'year': base_year,
                'average_temperature': base_year_data['average_temperature'],
                'samples': base_year_data['total_samples']
            },
            'comparison_year': {
                'year': comparison_year,
                'average_temperature': comparison_year_data['average_temperature'],
                'samples': comparison_year_data['total_samples']
            },
            'temperature_change': temp_change,
            'change_percentage': (temp_change / base_year_data['average_temperature'] * 100) if temp_change is not None else None
        }

    def visualize_climate_trend(self, city, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        temperatures = []

        for year in years:
            try:
                yearly_data = self.compare_climate_trends(city, year, year)
                if yearly_data['base_year']['average_temperature'] is None:
                    print(f"Warning: No temperature data available for {year}. Skipping this year.")
                    temperatures.append(None)
                else:
                    # Convert the temperature to Celsius (instead of Kelvin)
                    avg_temp_celsius = self.convert_temperature(yearly_data['base_year']['average_temperature'], 'K', 'C')
                    temperatures.append(avg_temp_celsius)
            except Exception as e:
                print(f"Could not retrieve data for {year}: {e}")
                temperatures.append(None)

        valid_years = [year for year, temp in zip(years, temperatures) if temp is not None]
        valid_temps = [temp for temp in temperatures if temp is not None]

        # If no valid data exists, display a message and exit the function
        if not valid_years or not valid_temps:
            print(f"No valid data available for the specified years ({start_year}-{end_year}) in {city}.")
            return

        # Proceed with plotting if valid data exists
        plt.figure(figsize=(12, 6))
        plt.plot(valid_years, valid_temps, marker='o')
        plt.title(f"Yearly Average Temperatures for {city}")
        plt.xlabel("Year")
        plt.ylabel("Average Temperature (°C)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
