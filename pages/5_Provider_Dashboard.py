import streamlit as st
from lib.db import get_client

st.set_page_config(page_title="Provider Dashboard — BSF Marketplace", page_icon="📊")

st.title("📊 Provider Dashboard")
st.write("Look up your business to view and respond to quote requests.")

supabase = get_client()

lookup_whatsapp = st.text_input(
    "Enter the WhatsApp number you registered with",
    placeholder="e.g. 0821234567",
)

if not lookup_whatsapp.strip():
    st.info("Enter your WhatsApp number above to access your dashboard.")
    st.stop()

try:
    result = (
        supabase.table("businesses")
        .select("*")
        .eq("whatsapp_number", lookup_whatsapp.strip())
        .execute()
    )
    businesses = result.data
except Exception as e:
    st.error(f"Could not look up business: {e}")
    businesses = []

if not businesses:
    st.warning("No business found with that WhatsApp number.")
    st.stop()

business = businesses[0]
st.success(f"Welcome, {business['business_name']}")
st.caption(f"Status: {business['status']}")

st.divider()
st.subheader("New Quote Requests")

try:
    req_result = (
        supabase.table("quote_requests")
        .select("*")
        .eq("business_id", business["id"])
        .order("created_at", desc=True)
        .execute()
    )
    requests = req_result.data
except Exception as e:
    st.error(f"Could not load quote requests: {e}")
    requests = []

if not requests:
    st.info("No quote requests yet.")
else:
    for req in requests:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Customer:** {req['customer_name']}")
                st.write(f"**Service:** {req['service_required']}")
                st.write(f"**Request:** {req['description']}")
                if req.get("preferred_date"):
                    st.write(f"**Preferred date:** {req['preferred_date']}")
                if req.get("budget"):
                    st.write(f"**Budget:** R{req['budget']:.0f}")
                st.caption(f"Contact: {req['customer_whatsapp']}")
            with col2:
                st.write(f"**Status:** {req['status']}")

            if req["status"] == "pending":
                with st.form(f"quote_form_{req['id']}"):
                    st.write("Respond with a quote:")
                    amount = st.number_input("Quote amount (R)", min_value=0.0, step=50.0, key=f"amt_{req['id']}")
                    completion = st.text_input("Estimated completion", placeholder="e.g. 1 day", key=f"comp_{req['id']}")
                    message = st.text_area("Additional message (optional)", key=f"msg_{req['id']}")
                    send_quote = st.form_submit_button("Send Quote")

                    if send_quote:
                        if amount <= 0:
                            st.error("Please enter a quote amount.")
                        else:
                            try:
                                supabase.table("quotes").insert({
                                    "quote_request_id": req["id"],
                                    "business_id": business["id"],
                                    "amount": amount,
                                    "estimated_completion": completion.strip() or None,
                                    "message": message.strip() or None,
                                    "status": "sent",
                                }, returning="minimal").execute()
                                supabase.table("quote_requests").update(
                                    {"status": "quoted"}
                                ).eq("id", req["id"]).execute()
                                st.success("Quote sent!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Could not send quote: {e}")
            else:
                st.caption(f"Already responded — status: {req['status']}")
