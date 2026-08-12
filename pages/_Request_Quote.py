import re
import streamlit as st
from datetime import date
from lib.db import get_client

st.set_page_config(page_title="Request a Quote — BSF Marketplace", page_icon="💬")

business_id = st.session_state.get("quote_business_id")
business_name = st.session_state.get("quote_business_name")

st.title("💬 Request a Quote")

if not business_id:
    st.info("Select a business from Find a Service first to request a quote.")
    if st.button("🔍 Go to Find a Service"):
        st.switch_page("pages/1_Find_a_Service.py")
    st.stop()

st.write(f"Requesting a quote from: **{business_name}**")

with st.form("request_quote", clear_on_submit=True):
    customer_name = st.text_input("Your name *")
    customer_whatsapp = st.text_input(
        "Your WhatsApp number *",
        placeholder="+27821234567",
        help="Format: +27 followed by 9 digits, no spaces (e.g. +27821234567). This is used to build your provider's WhatsApp link, so it must be exact.",
    )
    st.caption("⚠️ Must be in the format +27xxxxxxxxx — this is how the provider's WhatsApp link is generated.")
    customer_email = st.text_input("Email (optional)")
    service_required = st.text_input("Service required *", placeholder="e.g. Laptop repair")
    description = st.text_area(
        "Describe what you need *",
        placeholder="e.g. My laptop is not switching on and I need it diagnosed.",
    )
    preferred_date = st.date_input("Preferred date (optional)", value=None, min_value=date.today())
    budget = st.number_input("Budget (optional, R)", min_value=0.0, step=50.0, value=0.0)

    st.caption(
        "By submitting, your contact details and request will be shared with "
        "this business so they can respond with a quote."
    )
    consent = st.checkbox("I agree to the above *")

    submitted = st.form_submit_button("Send Request")

    if submitted:
        errors = []
        whatsapp_clean = customer_whatsapp.strip()
        if not customer_name.strip():
            errors.append("Your name is required.")
        if not whatsapp_clean:
            errors.append("Your WhatsApp number is required.")
        elif not re.match(r"^\+27\d{9}$", whatsapp_clean):
            errors.append("WhatsApp number must be in the format +27xxxxxxxxx (e.g. +27821234567).")
        if not service_required.strip():
            errors.append("Service required is required.")
        if not description.strip():
            errors.append("Please describe what you need.")
        if not consent:
            errors.append("You must agree to the consent notice.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                supabase = get_client()
                supabase.table("quote_requests").insert({
                    "business_id": business_id,
                    "customer_name": customer_name.strip(),
                    "customer_whatsapp": whatsapp_clean,
                    "customer_email": customer_email.strip() or None,
                    "service_required": service_required.strip(),
                    "description": description.strip(),
                    "preferred_date": preferred_date.isoformat() if preferred_date else None,
                    "budget": budget or None,
                    "status": "pending",
                }, returning="minimal").execute()
                st.success("Your quote request has been sent!")
                st.info(f"{business_name} will review your request and respond with a quote.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
