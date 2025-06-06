
import requests
from bs4 import BeautifulSoup
import re

def extract_property_details_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    details = {
        "price": None,
        "beds": None,
        "baths": None,
        "sqft": None,
        "description": None
    }

    text = soup.get_text(separator=" ").replace("\n", " ").lower()

    # Try to match price, bed/bath, sqft using regex
    price_match = re.search(r"\$[\d,]+", text)
    if price_match:
        details["price"] = price_match.group()

    beds_match = re.search(r"(\d+)\s*(bed|beds)", text)
    if beds_match:
        details["beds"] = beds_match.group(1)

    baths_match = re.search(r"(\d+(\.\d+)?)\s*(bath|baths)", text)
    if baths_match:
        details["baths"] = baths_match.group(1)

    sqft_match = re.search(r"([\d,]+)\s*(sqft|square feet)", text)
    if sqft_match:
        details["sqft"] = sqft_match.group(1)

    # Try to find a description paragraph
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        if len(p.get_text()) > 100:
            details["description"] = p.get_text().strip()
            break

    return details

def scrape_listing_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return extract_property_details_from_html(response.text)
    except Exception as e:
        print("Scraping error:", e)
    return None
