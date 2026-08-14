import requests

def get_weather(latitude, longitude):

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["current"]

    return None