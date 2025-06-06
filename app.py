import streamlit as st
import os
from openai import OpenAI
from helpers.property_api import get_property_data

# Load API keys
api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
client = OpenAI(api_key=api_key)

# Jerry's prompt
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

user_input = st.text_input("Enter message or property address (format: street, city, state, zip):")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if "," in user_input and len(user_input.split(",")) == 4:
        street, city, state, zip_code = [x.strip() for x in user_input.split(",")]
        data = get_property_data(street, city, state, zip_code)

        if data and "data" in data:
            valuation = data["data"].get("valuation", {}).get("value")
            comps = data["data"].get("sales_history", [])
            if valuation:
                cash_offer = int(valuation * 0.6)
                subto_offer = valuation
                analysis = f"""
📍 **Address:** {street}, {city}, {state} {zip_code}  
💰 **Estimated Value (AVM):** ${valuation:,}  
💸 **60% ARV Cash Offer:** ${cash_offer:,}  
📑 **Creative Subto Offer:** Full price + seller equity payout terms  
🧾 **Last Sale/Comps:** {comps[0] if comps else 'N/A'}
"""
                st.markdown(analysis)
                st.session_state.chat_history.append({"role": "assistant", "content": analysis})
            else:
                st.warning("No valuation data available.")
        else:
            st.error("Couldn’t fetch property info.")
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.chat_history,
                temperature=0.6
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.markdown(f"**Jerry:** {reply}")
        except Exception as e:
            st.error(f"API Error: {str(e)}")

with st.expander("💬 Show Chat History"):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
