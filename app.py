import streamlit as st

st.set_page_config(
    page_title="BSF Marketplace",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .main > div { padding-top: 2rem; }
    .hero-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0; text-align: center; }
    .hero-slogan {
        font-size: 1.3rem; font-weight: 800; letter-spacing: 1px;
        color: #1E88E5; text-align: center; margin: 0.3rem 0 0.2rem 0;
        text-transform: uppercase;
    }
    .hero-tagline { font-size: 1.05rem; color: #444; font-weight: 600; text-align: center; margin: 0; }
    .hero-quote {
        font-size: 0.95rem; color: #666; font-style: italic; text-align: center;
        margin: 0.8rem 0 1.2rem 0;
    }
    .hero-desc { font-size: 1rem; color: #444; margin: 0.5rem 0 2rem 0; line-height: 1.5; text-align: center; }
    div.stButton > button {
        width: 100%;
        padding: 0.75rem;
        font-weight: 600;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

logo_col = st.columns([1, 2, 1])[1]
with logo_col:
    st.image("assets/bsf-logo.jpeg", use_container_width=True)

st.markdown('<p class="hero-title">BSF Marketplace</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-slogan">Now or Never</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-tagline">Find. Connect. Support.</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-quote">"Bokamoso bja ekonomi ya rena ke boipereki."</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-desc">A marketplace connecting BSF members with businesses '
    "and service providers within the BSF community.</p>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Find a Service"):
        st.switch_page("pages/1_Find_a_Service.py")

with col2:
    if st.button("🏪 Register My Business"):
        st.switch_page("pages/2_Register_My_Business.py")

with col3:
    if st.button("💬 Request a Quote"):
        st.switch_page("pages/1_Find_a_Service.py")

st.write("")
if st.button("📊 Provider Dashboard", use_container_width=True):
    st.switch_page("pages/5_Provider_Dashboard.py")

st.divider()
st.caption(
    "By using this platform, you agree that basic contact and business "
    "information you submit may be shown to other BSF members to enable "
    "connections. We only display what's needed to make contact — see our "
    "privacy notice on the registration and quote forms."
)
