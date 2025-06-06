
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def search_property_google(address):
    # Fuzzy search by querying broader real estate terms
    query = f"{address} real estate OR home for sale OR property listing"
    url = f"https://www.google.com/search?q={quote_plus(query)}"

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
        if href and any(site in href for site in ["zillow.com", "redfin.com", "realtor.com", "trulia.com"]):
            title = link.get_text(strip=True)
            cleaned_url = href.replace("/url?q=", "").split("&")[0]
            results.append({
                "title": title,
                "link": cleaned_url
            })

    return results

# Very basic autocomplete (Option B)
def suggest_addresses(partial_input):
    # Use DuckDuckGo as a free autocomplete service (non-API fallback)
    query = f"https://duckduckgo.com/ac/?q={quote_plus(partial_input)}"
    try:
        res = requests.get(query, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == 200:
            suggestions = [item["phrase"] for item in res.json()]
            return suggestions[:5]  # Return top 5 suggestions
    except:
        return []
    return []
