
import requests
from serpapi import GoogleSearch
import os

def search_property_google(address):
    params = {
        "engine": "google",
        "q": f"{address} site:zillow.com OR site:redfin.com OR site:realtor.com",
        "api_key": os.getenv("SERPAPI_KEY"),
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results
