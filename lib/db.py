import os
import streamlit as st
from supabase import create_client, Client


def _get_secret(key: str) -> str:
    # Local/Codespaces: reads from .streamlit/secrets.toml
    # Render (or any host without secrets.toml): falls back to env vars
    try:
        return st.secrets[key]
    except Exception:
        value = os.environ.get(key)
        if not value:
            raise RuntimeError(
                f"Missing required secret: {key}. "
                f"Set it in .streamlit/secrets.toml locally or as an "
                f"environment variable in your hosting platform."
            )
        return value


@st.cache_resource
def get_client() -> Client:
    url = _get_secret("SUPABASE_URL")
    key = _get_secret("SUPABASE_KEY")
    return create_client(url, key)
