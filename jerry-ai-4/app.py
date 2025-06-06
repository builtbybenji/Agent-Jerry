
import streamlit as st
import os
import re
from urllib.parse import quote_plus
from helpers.web_search import search_property_google
from helpers.summary_export import create_pdf_report
from helpers.scraper import scrape_listing_page

st.set_page_config(page_title="Jerry - Real Estate Deal AI", page_icon="🏠")
st.title("Jerry – Real Estate Deal Analyzer")
TEST_MODE = st.sidebar.toggle('Enable Test Mode', value=True)
DEBUG_LOG = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": "You are Jerry, a smart AI that helps analyze real estate deals and summarize offers."}]

def parse_address(raw_input):
    raw = raw_input.strip()
    if "," in raw and len(raw.split(",")) == 4:
        return [x.strip() for x in raw.split(",")]
    pattern = r"(\d+\s[\w\s]+),?\s*([\w\s]+),?\s*([A-Z]{2}),?\s*(\d{5})"
    match = re.search(pattern, raw)
    if match:
        return [match.group(1), match.group(2), match.group(3), match.group(4)]
    return None

user_input = st.text_input("Enter property info (full or casual address):")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    parsed = parse_address(user_input)

    if parsed:
        street, city, state, zip_code = parsed
        full_address = f"{street}, {city}, {state} {zip_code}"

        if "data" in data["data"].get("valuation"):
            valuation = data["data"]["valuation"]["value"]
            comps = data["data"].get("sales_history", [])
            cash_offer = int(valuation * 0.6)

            summary = (
                f"**Address**: {full_address}\n"
                f"**Estimated Value (AVM)**: ${valuation:,}\n"
                f"**60% ARV Cash Offer**: ${cash_offer:,}\n"
                f"**Creative Subto Offer**: Full price + seller equity terms\n"
                f"**Last Sale/Comps**: {comps[0] if comps else 'N/A'}"
            )
            st.markdown(summary)
            st.session_state.chat_history.append({"role": "assistant", "content": summary})
            pdf_path = f"/tmp/{street.replace(' ', '_')}_{zip_code}_summary.pdf"
            create_pdf_report(full_address, valuation, cash_offer, comps, pdf_path)
        else:
            DEBUG_LOG.append("Primary API failed. Falling back to Google scraping.")
            st.warning("API data unavailable. Scraping public listings...")
            google_data = search_property_google(full_address)
            if google_"organic_results" in google_data:
                for result in google_data["organic_results"][:3]:
                    url = result["link"]
                    image_url = result.get("thumbnail")
                    scraped = scrape_listing_page(url) if not TEST_MODE else {
                        'price': '$450,000', 'beds': '3', 'baths': '2', 'sqft': '1800',
                        'description': 'Test mode: Beautiful 3 bed, 2 bath home.'
                    }
                    if scraped and scraped.get("price"):
                        price_val = int(scraped["price"].replace("$", "").replace(",", ""))
                        cash_offer = int(price_val * 0.6)
                        description = scraped.get("description") or "N/A"
                        description_short = description[:300] if isinstance(description, str) else "N/A"

                        markdown_text = (
                            f"**Source**: [{result['title']}]({url})\n\n"
                            f"**Address**: {full_address}\n"
                            f"**Listed Price**: {scraped['price']}\n"
                            f"**Beds**: {scraped.get('beds', 'N/A')}\n"
                            f"**Baths**: {scraped.get('baths', 'N/A')}\n"
                            f"**Sqft**: {scraped.get('sqft', 'N/A')}\n"
                            f"**Description**: {description_short}...\n\n"
                            f"**60% ARV Cash Offer**: ${cash_offer:,}\n"
                            "**Creative Subto Offer**: Full price + seller equity terms"
                        )
                        st.markdown(markdown_text)
                        pdf_path = f"/tmp/{street.replace(' ', '_')}_{zip_code}_scraped_summary.pdf"
                        create_pdf_report(full_address, price_val, cash_offer, [description], pdf_path, image_url=image_url)
                        break
            else:
                st.error("No property data found from public sources.")
    else:
        st.error("Please enter a valid U.S. property address.")

    if 'pdf_path' in locals() and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Property Summary PDF",
                data=pdf_file,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
        address_encoded = quote_plus(full_address)
        st.components.v1.html(
            f'<iframe width="100%" height="350" src="https://maps.google.com/maps?q={address_encoded}&output=embed"></iframe>',
            height=350
        )

    if DEBUG_LOG:
        st.sidebar.markdown("Debug Log")
        for log in DEBUG_LOG:
            st.sidebar.code(log)

with st.expander("Chat History"):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
