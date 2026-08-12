import streamlit as st
from lib.db import get_client

def get_current_user():
    return st.session_state.get("auth_user")

def sign_up(email: str, password: str):
    supabase = get_client()
    result = supabase.auth.sign_up({"email": email, "password": password})
    if result.user and result.session:
        st.session_state["auth_user"] = result.user
        st.session_state["auth_session"] = result.session
    return result

def sign_in(email: str, password: str):
    supabase = get_client()
    result = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if result.user:
        st.session_state["auth_user"] = result.user
        st.session_state["auth_session"] = result.session
    return result

def sign_out():
    supabase = get_client()
    supabase.auth.sign_out()
    st.session_state.pop("auth_user", None)
    st.session_state.pop("auth_session", None)
