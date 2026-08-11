import streamlit as st
from lib.db import get_client

st.set_page_config(page_title="Register My Business — BSF Marketplace", page_icon="🏪")

CATEGORIES = [
    "Technology", "Business Services", "Food & Catering", "Fashion & Clothing",
    "Beauty", "Transport", "Printing", "Graphic Design", "Photography & Media",
    "Construction & Repairs", "Cleaning", "Education & Tutoring", "Events",
    "Professional Services", "Retail", "Other",
]

st.title("🏪 Register My Business")
st.write("List your business or service in the BSF Marketplace.")

with st.form("register_business", clear_on_submit=True):
    business_name = st.text_input("Business name *")
    owner_name = st.text_input("Owner / member name *")
    whatsapp_number = st.text_input("WhatsApp number *", placeholder="e.g. 0821234567")
    email = st.text_input("Email (optional)")
    branch = st.text_input("BSF branch")
    location = st.text_input("Location *", placeholder="e.g. Johannesburg")
    category = st.selectbox("Category *", CATEGORIES)
    services = st.text_area("Services offered *", placeholder="e.g. Laptop repairs, screen replacements")
    description = st.text_area("Description")
    starting_price = st.number_input("Starting price (R)", min_value=0.0, step=10.0)
    operating_hours = st.text_input("Operating hours", placeholder="e.g. Mon-Fri 9am-5pm")
    website = st.text_input("Website / social media link (optional)")

    st.caption(
        "By submitting, you agree that this business information (excluding "
        "your email) will be shown publicly in the marketplace so other BSF "
        "members can find and contact you. Your listing will be reviewed "
        "before it goes live."
    )
    consent = st.checkbox("I agree to the above *")

    submitted = st.form_submit_button("Submit Business")

    if submitted:
        errors = []
        if not business_name.strip():
            errors.append("Business name is required.")
        if not owner_name.strip():
            errors.append("Owner/member name is required.")
        if not whatsapp_number.strip():
            errors.append("WhatsApp number is required.")
        if not location.strip():
            errors.append("Location is required.")
        if not services.strip():
            errors.append("Services offered is required.")
        if not consent:
            errors.append("You must agree to the consent notice.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                supabase = get_client()
                supabase.table("businesses").insert({
                    "business_name": business_name.strip(),
                    "owner_name": owner_name.strip(),
                    "whatsapp_number": whatsapp_number.strip(),
                    "email": email.strip() or None,
                    "branch": branch.strip() or None,
                    "location": location.strip(),
                    "category": category,
                    "services": services.strip(),
                    "description": description.strip() or None,
                    "starting_price": starting_price or None,
                    "operating_hours": operating_hours.strip() or None,
                    "website": website.strip() or None,
                    "status": "pending",
                }, returning="minimal").execute()
                st.success("Your business has been submitted successfully.")
                st.info("It will appear in the marketplace once reviewed and approved.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
