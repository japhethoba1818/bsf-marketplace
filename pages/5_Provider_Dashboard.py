import streamlit as st
from lib.db import get_client
from lib.auth import get_current_user

st.set_page_config(page_title="Provider Dashboard — BSF Marketplace", page_icon="📊")

st.title("📊 Provider Dashboard")

user = get_current_user()
if not user:
    st.warning("Please sign in to view your business dashboard.")
    if st.button("🔐 Go to Sign In"):
        st.switch_page("pages/6_Sign_In.py")
    st.stop()

supabase = get_client()

try:
    result = (
        supabase.table("businesses")
        .select("*")
        .eq("owner_user_id", user.id)
        .execute()
    )
    businesses = result.data
except Exception as e:
    st.error(f"Could not load your businesses: {e}")
    businesses = []

if not businesses:
    st.info("You haven't registered a business yet.")
    if st.button("🏪 Register My Business"):
        st.switch_page("pages/2_Register_My_Business.py")
    st.stop()

if len(businesses) == 1:
    business = businesses[0]
else:
    names = {b["business_name"]: b for b in businesses}
    chosen = st.selectbox("Select your business", list(names.keys()))
    business = names[chosen]

st.success(f"Managing: {business['business_name']}")
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
                                    {"status": "quote_sent"}
                                ).eq("id", req["id"]).execute()

                                import urllib.parse
                                wa_number = req["customer_whatsapp"].replace(" ", "").replace("+", "")
                                msg_lines = [
                                    f"Hi {req['customer_name']}, here's your quote from {business['business_name']}:",
                                    f"Amount: R{amount:.0f}",
                                ]
                                if completion.strip():
                                    msg_lines.append(f"Estimated completion: {completion.strip()}")
                                if message.strip():
                                    msg_lines.append(message.strip())
                                wa_message = urllib.parse.quote("\n".join(msg_lines))
                                wa_link = f"https://wa.me/{wa_number}?text={wa_message}"

                                st.session_state[f"wa_link_{req['id']}"] = wa_link
                                st.rerun()
                            except Exception as e:
                                st.error(f"Could not send quote: {e}")
            else:
                st.caption(f"Already responded — status: {req['status']}")

            wa_link_key = f"wa_link_{req['id']}"
            if wa_link_key in st.session_state:
                st.success("Quote saved! Send it to the customer:")
                st.link_button("💬 Send Quote via WhatsApp", st.session_state[wa_link_key])
