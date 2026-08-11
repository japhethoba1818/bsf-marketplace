import streamlit as st

st.set_page_config(page_title="Request a Quote — BSF Marketplace", page_icon="💬")
st.title("💬 Request a Quote")

business_name = st.session_state.get("quote_business_name")
if business_name:
    st.write(f"Requesting a quote from: **{business_name}**")
else:
    st.write("Select a business from Find a Service first.")

st.info("Coming in Phase 8: full quote request form.")
