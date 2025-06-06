
import streamlit as st

# 🔧 Enable test mode to use mock data instead of real scraping and email sending
TEST_MODE = st.sidebar.toggle('🧪 Enable Test Mode', value=True)
DEBUG_LOG = []
import os
import re
from openai import OpenAI
from urllib.parse import quote_plus
import smtplib
from email.message import EmailMessage

from helpers.property_api import get_property_data
from helpers.web_search import search_property_google
from helpers.summary_export import create_pdf_report
from helpers.scraper import scrape_listing_page

def parse_address(raw_input):
    raw = raw_input.strip()
    if "," in raw and len(raw.split(",")) == 4:
        return [x.strip() for x in raw.split(",")]
    pattern = r"(\d+\s[\w\s]+),?\s*([\w\s]+),?\s*([A-Z]{2}),?\s*(\d{5})"
    match = re.search(pattern, raw)
    if match:
        return [match.group(1), match.group(2), match.group(3), match.group(4)]
    return None

api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
client = OpenAI(api_key=api_key)

jerry_personality = """
You are Jerry, a real estate deal analyzer assistant. You collect:
- Property address & condition
- Asking price, repair estimate
You pull comps & ARV using an API, then estimate:
1. A 60% ARV cash offer
2. A creative finance offer with full ask and equity terms
Speak like a confident investment analyst, not a sales rep.
"""

st.set_page_config(page_title="Jerry - Real Estate Deal AI", page_icon="🏠")
st.title("🏠 Jerry – Real Estate Deal Analyzer")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": jerry_personality}]

user_input = st.text_input("Enter property info (full or casual address):")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    parsed_address = parse_address(user_input)
    if parsed_address:
        street, city, state, zip_code = parsed_address
        data = get_property_data(street, city, state, zip_code)

        if data and "data" in data:
            valuation = data["data"].get("valuation", {}).get("value")
            comps = data["data"].get("sales_history", [])
            if valuation:
                cash_offer = int(valuation * 0.6)
                analysis = f"""
📍 **Address:** {street}, {city}, {state} {zip_code}  
💰 **Estimated Value (AVM):** ${valuation:,}  
💸 **60% ARV Cash Offer:** ${cash_offer:,}  
📑 **Creative Subto Offer:** Full price + seller equity payout terms  
🧾 **Last Sale/Comps:** {comps[0] if comps else 'N/A'}
"""
                st.markdown(analysis)

                # PDF generation
                pdf_path = f"/tmp/{street.replace(' ', '_')}_{zip_code}_summary.pdf"
                create_pdf_report(f"{street}, {city}, {state} {zip_code}", valuation, cash_offer, comps, pdf_path)
                with open(pdf_path, "rb") as pdf_file:
                                        # Embedded Google Maps preview
    address_encoded = quote_plus(f"{street}, {city}, {state} {zip_code}")
                                        # Show basic embedded map using a public Google Maps URL
    address_encoded = quote_plus(f"{street}, {city}, {state} {zip_code}")
    st.markdown(f"### 🗺️ Google Maps Preview")
    st.components.v1.iframe(f"https://maps.google.com/maps?q={address_encoded}&output=embed", width=600, height=450)
                                                st.download_button(
        label='📄 Download Property Summary PDF',
        data=pdf_file,
        file_name=os.path.basename(pdf_path),
        mime='application/pdf'
    )

    if DEBUG_LOG:
        st.sidebar.markdown('### 🐞 Debug Log')
        for log in DEBUG_LOG:
            st.sidebar.code(log)
st.download_button(
                        label="📄 Download Property Summary PDF",
                        data=pdf_file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )

                st.session_state.chat_history.append({"role": "assistant", "content": analysis})
            else:
                st.warning("No valuation data available.")
        else:
            
            st.warning("Primary API failed. Trying web search for public data...")
            google_data = search_property_google(f"{street}, {city}, {state} {zip_code}")
            if google_data and "organic_results" in google_data:
                links = google_data["organic_results"]
                found = False
                for item in links[:3]:
                    url = item["link"]
                    image_url = item.get("thumbnail")
                    if TEST_MODE:
                    DEBUG_LOG.append('✅ Using mock property data (Test Mode)')
scraped = {
                        'price': '$450,000',
                        'beds': '3',
                        'baths': '2',
                        'sqft': '1800',
                        'description': 'Test mode: Beautiful 3 bed, 2 bath home with 1800 sqft and a garage.'
                    }
                else:
                    DEBUG_LOG.append('🔍 Scraping listing page for real data')
scraped = scrape_listing_page(url)
                    if scraped and scraped["price"]:
                        found = True
                        price_val = int(scraped["price"].replace("$", "").replace(",", ""))
                        cash_offer = int(price_val * 0.6)
                        st.markdown(f"""
🔗 **Source:** [{item['title']}]({url})

📍 **Address:** {street}, {city}, {state} {zip_code}  
💰 **Listed Price:** {scraped['price']}  
🛏 **Beds:** {scraped.get('beds', 'N/A')}  
🛁 **Baths:** {scraped.get('baths', 'N/A')}  
📐 **Sqft:** {scraped.get('sqft', 'N/A')}  
📝 **Description:** {scraped.get('description', 'N/A')[:300]}...

💸 **60% ARV Cash Offer:** ${cash_offer:,}  
📑 **Creative Subto Offer:** Full price + seller equity payout terms  
                        """)

                        # Generate PDF
                        pdf_path = f"/tmp/{street.replace(' ', '_')}_{zip_code}_scraped_summary.pdf"
                        create_pdf_report(f"{street}, {city}, {state} {zip_code}", price_val, cash_offer, [scraped.get('description', 'N/A')], pdf_path, image_url=image_url)
                        with open(pdf_path, "rb") as pdf_file:
                                                        # Embedded Google Maps preview
    address_encoded = quote_plus(f"{street}, {city}, {state} {zip_code}")
                                                        # Show basic embedded map using a public Google Maps URL
    address_encoded = quote_plus(f"{street}, {city}, {state} {zip_code}")
    st.markdown(f"### 🗺️ Google Maps Preview")
    st.components.v1.iframe(f"https://maps.google.com/maps?q={address_encoded}&output=embed", width=600, height=450)
                                                                st.download_button(
        label='📄 Download Property Summary PDF',
        data=pdf_file,
        file_name=os.path.basename(pdf_path),
        mime='application/pdf'
    )

    if DEBUG_LOG:
        st.sidebar.markdown('### 🐞 Debug Log')
        for log in DEBUG_LOG:
            st.sidebar.code(log)
st.download_button(
                                label="📄 Download Property Summary PDF",
                                data=pdf_file,
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf"
                            )
                        break
                if not found:
                    st.error("Couldn't extract structured data from the listings found.")
            else:
                st.error("Couldn't find any public listings or property data.")

            google_data = search_property_google(f"{street}, {city}, {state} {zip_code}")
            if google_data and "organic_results" in google_data:
                links = google_data["organic_results"]
                st.markdown("🔍 Found public listings:")
                for item in links[:3]:
                    st.markdown(f"- [{item['title']}]({item['link']})")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Displayed public listing results from Google for: {street}, {city}, {state} {zip_code}"
                })
            else:
                st.error("Couldn't find any public listings or property data.")
    else:
        st.error("Please enter a valid U.S. property address.")

with st.expander("💬 Show Chat History"):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
