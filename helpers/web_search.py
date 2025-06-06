
import requests
import os

def search_property_google(address):
    api_key = os.getenv("SERPAPI_KEY", "")
    query = address.replace(" ", "+")
    url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        print("SerpAPI Error:", response.status_code, response.text)
        return None
    except Exception as e:
        print("Google search error:", str(e))
        return None
