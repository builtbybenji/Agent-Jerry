
import requests
from bs4 import BeautifulSoup

def search_property_google(address):
    query = f"{address} site:zillow.com OR site:redfin.com OR site:realtor.com"
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for link in soup.select("a"):
        href = link.get("href")
        if href and ("zillow.com" in href or "redfin.com" in href or "realtor.com" in href):
            title = link.get_text(strip=True)
            cleaned_url = href.replace("/url?q=", "").split("&")[0]
            results.append({
                "title": title,
                "link": cleaned_url
            })

    return results
