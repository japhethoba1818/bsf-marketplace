import streamlit as st
from lib.db import get_client

st.set_page_config(page_title="Find a Service — BSF Marketplace", page_icon="🔍")

CATEGORIES = [
    "All Categories", "Technology", "Business Services", "Food & Catering",
    "Fashion & Clothing", "Beauty", "Transport", "Printing", "Graphic Design",
    "Photography & Media", "Construction & Repairs", "Cleaning",
    "Education & Tutoring", "Events", "Professional Services", "Retail", "Other",
]

st.title("🔍 Find a Service")
st.write("Search BSF member businesses and service providers.")

search_query = st.text_input("Search", placeholder="e.g. laptop repair, catering, tutoring")

col1, col2, col3 = st.columns(3)
with col1:
    category_filter = st.selectbox("Category", CATEGORIES)
with col2:
    location_filter = st.text_input("Location", placeholder="e.g. Johannesburg")
with col3:
    max_price = st.number_input("Max price (R)", min_value=0.0, step=50.0, value=0.0)

supabase = get_client()

try:
    query = supabase.table("businesses").select("*").eq("status", "approved")

    if category_filter != "All Categories":
        query = query.eq("category", category_filter)
    if location_filter.strip():
        query = query.ilike("location", f"%{location_filter.strip()}%")
    if max_price > 0:
        query = query.lte("starting_price", max_price)

    result = query.order("created_at", desc=True).execute()
    businesses = result.data
except Exception as e:
    st.error(f"Could not load businesses: {e}")
    businesses = []

if search_query.strip():
    q = search_query.strip().lower()
    businesses = [
        b for b in businesses
        if q in (b.get("business_name") or "").lower()
        or q in (b.get("services") or "").lower()
        or q in (b.get("description") or "").lower()
        or q in (b.get("category") or "").lower()
    ]

st.divider()

if not businesses:
    st.info("No businesses found matching your search. Try different filters.")
else:
    st.caption(f"{len(businesses)} result(s)")
    for b in businesses:
        with st.container(border=True):
            st.subheader(b["business_name"])
            st.caption(f"{b['category']} · {b.get('location', 'Location not set')}")
            if b.get("description"):
                st.write(b["description"])
            if b.get("services"):
                st.write(f"**Services:** {b['services']}")
            price_line = f"From R{b['starting_price']:.0f}" if b.get("starting_price") else "Price on request"
            hours_line = b.get("operating_hours") or "Hours not specified"
            st.write(f"**{price_line}** · {hours_line}")

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("View Profile", key=f"profile_{b['id']}"):
                    st.session_state["profile_business_id"] = b["id"]
                    st.switch_page("pages/_Business_Profile.py")
            with btn_col2:
                wa_number = b.get("whatsapp_number", "").replace(" ", "").replace("+", "")
                st.link_button("💬 WhatsApp", f"https://wa.me/{wa_number}")
            with btn_col3:
                if st.button("Request Quote", key=f"quote_{b['id']}"):
                    st.session_state["quote_business_id"] = b["id"]
                    st.session_state["quote_business_name"] = b["business_name"]
                    st.switch_page("pages/_Request_Quote.py")
