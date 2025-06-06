
import requests
import os

def search_property_google(address):
    api_key = os.getenv("SERPAPI_KEY", "")
    query = address.replace(" ", "+")
    url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print("Google search error:", str(e))
        return None
