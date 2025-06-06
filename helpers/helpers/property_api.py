import requests
import os

def get_property_data(street, city, state, zip_code):
    token = os.getenv("ESTATED_API_KEY", "")
    base_url = "https://apis.estated.com/v4/property"
    params = {
        "token": token,
        "street_address": street,
        "city": city,
        "state": state,
        "zip_code": zip_code
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    return None
