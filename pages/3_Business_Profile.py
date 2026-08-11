import streamlit as st
from lib.db import get_client

st.set_page_config(page_title="Business Profile — BSF Marketplace", page_icon="🏪")

business_id = st.session_state.get("profile_business_id")

if not business_id:
    st.title("🏪 Business Profile")
    st.info("Select a business from Find a Service to view its profile.")
    if st.button("🔍 Go to Find a Service"):
        st.switch_page("pages/1_Find_a_Service.py")
    st.stop()

supabase = get_client()

try:
    result = (
        supabase.table("businesses")
        .select("*")
        .eq("id", business_id)
        .eq("status", "approved")
        .execute()
    )
    business = result.data[0] if result.data else None
except Exception as e:
    st.error(f"Could not load business: {e}")
    business = None

if not business:
    st.title("🏪 Business Profile")
    st.warning("This business could not be found or is not currently listed.")
    if st.button("🔍 Go to Find a Service"):
        st.switch_page("pages/1_Find_a_Service.py")
    st.stop()

st.title(business["business_name"])
st.caption(f"{business['category']} · {business.get('location', 'Location not set')}")

if business.get("photo_urls"):
    photo_cols = st.columns(len(business["photo_urls"]))
    for col, url in zip(photo_cols, business["photo_urls"]):
        with col:
            st.image(url, use_container_width=True)

if business.get("description"):
    st.write(business["description"])

st.divider()

if business.get("services"):
    st.subheader("Services")
    st.write(business["services"])

col1, col2 = st.columns(2)
with col1:
    price_line = (
        f"From R{business['starting_price']:.0f}"
        if business.get("starting_price") else "Price on request"
    )
    st.metric("Starting Price", price_line)
with col2:
    st.metric("Operating Hours", business.get("operating_hours") or "Not specified")

if business.get("branch"):
    st.write(f"**BSF Branch:** {business['branch']}")
if business.get("website"):
    st.write(f"**Website / Social:** {business['website']}")

st.divider()

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    wa_number = (business.get("whatsapp_number") or "").replace(" ", "").replace("+", "")
    st.link_button("💬 Contact via WhatsApp", f"https://wa.me/{wa_number}")
with btn_col2:
    if st.button("📩 Request Quote"):
        st.session_state["quote_business_id"] = business["id"]
        st.session_state["quote_business_name"] = business["business_name"]
        st.switch_page("pages/4_Request_Quote.py")
