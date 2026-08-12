import streamlit as st
from lib.auth import sign_up, sign_in, sign_out, get_current_user

st.set_page_config(page_title="Sign In — BSF Marketplace", page_icon="🔐")

st.title("🔐 Business Owner Sign In")

user = get_current_user()
if user:
    st.success(f"Signed in as {user.email}")
    if st.button("Sign Out"):
        sign_out()
        st.rerun()
    st.stop()

tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

with tab_login:
    with st.form("login_form"):
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Log In")
        if login_submitted:
            try:
                sign_in(login_email.strip(), login_password)
                st.success("Logged in!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")

with tab_signup:
    with st.form("signup_form"):
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
        signup_submitted = st.form_submit_button("Sign Up")
        if signup_submitted:
            if len(signup_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                try:
                    result = sign_up(signup_email.strip(), signup_password)
                    if result.session:
                        st.success("Account created! You're now logged in.")
                        st.rerun()
                    else:
                        st.success("Account created! Please log in using the Log In tab.")
                except Exception as e:
                    st.error(f"Sign up failed: {e}")
