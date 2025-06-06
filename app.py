
import streamlit as st
from helpers.web_search import search_property_google, suggest_addresses
from helpers.summary_export import create_pdf_report
from urllib.parse import quote_plus

st.set_page_config(page_title="Agent Jerry", layout="centered")

# Sidebar toggle for debug/test mode
debug = st.sidebar.toggle("Debug Mode")

st.title("🏠 Agent Jerry - Smart Property Deal Finder")

# Address input with autocomplete suggestions
user_input = st.text_input("Enter a property address:")
suggestions = suggest_addresses(user_input) if user_input else []

if suggestions:
    st.markdown("**Suggestions:**")
    for s in suggestions:
        if st.button(s):
            user_input = s

if user_input:
    with st.spinner("🔍 Searching top real estate listings..."):
        search_results = search_property_google(user_input)

    if not search_results:
        st.error("❌ No property listings found. Try a different address or be more specific.")
    else:
        st.success(f"✅ Found {len(search_results)} listing(s)")
        for result in search_results[:3]:  # Show top 3
            st.markdown(f"- [{result['title']}]({result['link']})")

        # Summary Section
        summary_text = "\n\n".join(
            [f"🏠 **{user_input}**\n**Listing:** {res['title']}\n[View Listing]({res['link']})"
             for res in search_results[:3]]
        )

        if st.button("📝 Generate Property Summary PDF"):
            pdf_path = create_pdf_report(user_input, search_results)
            st.success("📄 Report ready!")
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name="Property_Summary.pdf")

        if debug:
            st.subheader("🔧 Raw Search Data")
            st.json(search_results)
