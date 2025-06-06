import streamlit as st
import os
from openai import OpenAI

# Load API key from environment or Streamlit secrets
api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
client = OpenAI(api_key=api_key)

# Jerry's system prompt
jerry_personality = """
Your name is Jerry, an expert deal analyzer trained in real estate investment, MLS property audits, and creative finance.

Your job is to:
1. Ask for the property address, asking price, estimated repairs, and condition.
2. Determine if the property is listed on the MLS.
3. Pull or estimate comps and determine ARV.
4. Estimate profit margins.
5. Generate 2 offers:
   - 60% ARV cash offer
   - Creative Subto offer with full price and seller equity payout

Be professional, confident, and investment-focused. Always offer to forward the analysis to the acquisition team if the seller is open to selling.
"""

st.set_page_config(page_title="Jerry - Real Estate Deal Analyzer", page_icon="🏠")
st.title("🏠 Jerry - Real Estate Deal Analyzer (Subto + Cash Offer Bot)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": jerry_personality}]

user_input = st.text_input("You (Seller/Agent):", key="input")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

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
        st.error(f"Error: {str(e)}")

with st.expander("📋 Show Chat History"):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
