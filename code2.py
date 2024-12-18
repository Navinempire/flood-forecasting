import pandas as pd
import requests

def fetch_weather_data(city_name, api_key):
    """Fetch current weather data from OpenWeatherMap API."""
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Extract relevant information
        rainfall = data.get('rain', {}).get('1h', 0)  # Rainfall in the last hour (if available)
        temperature = data['main']['temp']  # Current temperature
        weather_description = data['weather'][0]['description']  # Weather description
        return rainfall, temperature, weather_description
    
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred for {city_name}: {err}")
        return None, None, None
    except Exception as e:
        print(f"An error occurred for {city_name}: {e}")
        return None, None, None

def load_historical_data(excel_file):
    """Load historical flood data from an Excel file."""
    df = pd.read_excel(excel_file)
    return df

def get_current_weather(city_name, api_key):
    """Fetch current weather data when historical data is not available."""
    return fetch_weather_data(city_name, api_key)

def check_flood_risk(district_name, historical_data, api_key):
    """Check flood risk based on weather data for a given district."""
    # Check if the district is in the historical data
    if district_name not in historical_data['District'].values:
        print(f"No historical flood data found for {district_name}. Fetching today's weather instead.")
        
        rainfall, temperature, weather_description = get_current_weather(district_name, api_key)
        
        if rainfall is not None:
            print(f"District: {district_name}")
            print(f"Current Temperature: {temperature}°C")
            print(f"Weather Description: {weather_description.capitalize()}")
            print(f"Rainfall (last hour): {rainfall} mm")
            return
        
    # If historical data exists, check flood risk
    rainfall, temperature, weather_description = fetch_weather_data(district_name, api_key)
    
    if rainfall is not None:
        flood_risk = "No Flood Risk"
        
        # Define your own threshold for flood risk here
        if rainfall > 10:  # Example threshold: if rainfall > 10 mm in the last hour
            flood_risk = "Flood Risk Detected"
        
        print(f"District: {district_name}")
        print(f"Current Temperature: {temperature}°C")
        print(f"Weather Description: {weather_description.capitalize()}")
        print(f"Rainfall (last hour): {rainfall} mm")
        print(f"Flood Risk: {flood_risk}")
    else:
        print("Could not retrieve weather data.")

def main():
    excel_file = 'D:\\flood forcasting\\flood data.xlsx'  # Path to your Excel file
    api_key = '1b4b391bd5623f17abfd8d1219da95ff'   # Replace with your OpenWeatherMap API key
    
    # Load historical flood data
    historical_data = load_historical_data(excel_file)
    
    # Get user input for district name
    district_name = input("Enter the district name: ")
    
    check_flood_risk(district_name, historical_data, api_key)

if __name__ == "__main__":
    main()
