import streamlit as st
from lib.db import get_client
from lib.auth import get_current_user

st.set_page_config(page_title="Register My Business — BSF Marketplace", page_icon="🏪")

user = get_current_user()
if not user:
    st.title("🏪 Register My Business")
    st.warning("Please sign in first to register a business.")
    if st.button("🔐 Go to Sign In"):
        st.switch_page("pages/6_Sign_In.py")
    st.stop()

CATEGORIES = [
    "Technology", "Business Services", "Food & Catering", "Fashion & Clothing",
    "Beauty", "Transport", "Printing", "Graphic Design", "Photography & Media",
    "Construction & Repairs", "Cleaning", "Education & Tutoring", "Events",
    "Professional Services", "Retail", "Other",
]

ZCCSF_BRANCHES = ["AP", "CJC", "DFC", "SWC", "WITS", "N/A", "Other"]

st.title("🏪 Register My Business")
st.write("List your business or service in the BSF Marketplace.")

with st.form("register_business", clear_on_submit=True):
    business_name = st.text_input("Business name *")
    owner_name = st.text_input("Owner / member name *")
    whatsapp_number = st.text_input("WhatsApp number *", placeholder="e.g. 0821234567")
    email = st.text_input("Email (optional)")
    branch_choice = st.selectbox("ZCCSF Branch", ZCCSF_BRANCHES)
    branch_other = ""
    if branch_choice == "Other":
        branch_other = st.text_input("Please specify your ZCCSF Branch")
    location = st.text_input("Location *", placeholder="e.g. Johannesburg")
    category = st.selectbox("Category *", CATEGORIES)
    services = st.text_area("Services offered *", placeholder="e.g. Laptop repairs, screen replacements")
    description = st.text_area("Description")
    starting_price = st.number_input("Starting price (R)", min_value=0.0, step=10.0)
    operating_hours = st.text_input("Operating hours", placeholder="e.g. Mon-Fri 9am-5pm")
    website = st.text_input("Website / social media link (optional)")
    photos = st.file_uploader(
        "Photos (optional, up to 4)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

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
        if branch_choice == "Other" and not branch_other.strip():
            errors.append("Please specify your ZCCSF Branch.")
        if not location.strip():
            errors.append("Location is required.")
        if not services.strip():
            errors.append("Services offered is required.")
        if not consent:
            errors.append("You must agree to the consent notice.")
        if photos and len(photos) > 4:
            errors.append("Please upload a maximum of 4 photos.")
        if photos:
            for p in photos:
                if p.size > 5 * 1024 * 1024:
                    errors.append(f"{p.name} is too large (max 5MB per photo).")

        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                supabase = get_client()

                branch_value = branch_other.strip() if branch_choice == "Other" else branch_choice

                photo_urls = []
                if photos:
                    import uuid
                    for photo in photos[:4]:
                        ext = photo.name.split(".")[-1]
                        file_path = f"{uuid.uuid4()}.{ext}"
                        supabase.storage.from_("business-photos").upload(
                            file_path, photo.getvalue(),
                            {"content-type": photo.type},
                        )
                        public_url = supabase.storage.from_("business-photos").get_public_url(file_path)
                        photo_urls.append(public_url)

                supabase.table("businesses").insert({
                    "owner_user_id": user.id,
                    "business_name": business_name.strip(),
                    "owner_name": owner_name.strip(),
                    "whatsapp_number": whatsapp_number.strip(),
                    "email": email.strip() or None,
                    "branch": branch_value or None,
                    "location": location.strip(),
                    "category": category,
                    "services": services.strip(),
                    "description": description.strip() or None,
                    "starting_price": starting_price or None,
                    "operating_hours": operating_hours.strip() or None,
                    "website": website.strip() or None,
                    "photo_urls": photo_urls or None,
                    "status": "pending",
                }, returning="minimal").execute()
                st.success("Your business has been submitted successfully.")
                st.info("It will appear in the marketplace once reviewed and approved.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
