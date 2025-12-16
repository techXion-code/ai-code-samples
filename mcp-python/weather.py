import requests

def fetch_weather(city):
    coords = get_geocoordinates(city)
    latitude = coords["latitude"]
    longitude = coords["longitude"]

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    res = requests.get(url)
    weather_data = res.json()
    return weather_data["current_weather"]


def get_geocoordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    res = requests.get(url)
    geo_data = res.json()
    return geo_data["results"][0]