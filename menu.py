import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Finance Tools - Your Financial Companion", 
    layout="wide",
    page_icon="💰",
    initial_sidebar_state="collapsed"
)

# Initialize theme state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Create toggle button using Streamlit columns for positioning
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀ Light", 
                 help="Toggle dark/light mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ----------------------------
# Apply CSS based on theme state
# ----------------------------
if st.session_state.dark_mode:
    # Dark theme CSS
    st.markdown(""" 
    <style>
    /* Dark theme styles here ... (unchanged from your version) */
    </style>
    """, unsafe_allow_html=True)
else:
    # Light theme CSS
    st.markdown(""" 
    <style>
    /* Light theme styles here ... (unchanged from your version) */
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# Logo and Title
# ----------------------------
st.markdown("""
<div class="logo-container">
    <div class="logo">💰</div>
</div>
<h1 class="main-title">Finance Tools</h1>
<p class="subtitle">Your comprehensive financial companion for smart money management</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# Tools Data
# ----------------------------
tools = [
    {"name": "SIP Calculator", "desc": "Calculate your SIP returns...", 
     "link": "https://financialreach.streamlit.app/", "icon": "📈"},
    {"name": "Credit Score Estimator", "desc": "Get accurate credit score estimates...", 
     "link": "https://creditscores.streamlit.app/", "icon": "💳"},
    {"name": "Tax Calculator", "desc": "Calculate your income tax liability...", 
     "link": "https://taxreturncalc.streamlit.app/", "icon": "🧾"},
    {"name": "EMI Calculator", "desc": "Plan your loan repayments with precision...", 
     "link": "https://emicalculatorsj.streamlit.app/", "icon": "🏦"},
    {"name": "Expense Tracker", "desc": "Track daily expenses and analyze patterns...", 
     "link": "https://expensetrac.streamlit.app/", "icon": "💵"},
]

# ----------------------------
# Tools Grid
# ----------------------------
st.markdown('<div class="tools-grid">', unsafe_allow_html=True)

for tool in tools:
    st.markdown(
        f"""
        <div class="tool-card">
            <div>
                <div class="tool-icon">{tool["icon"]}</div>
                <h4 class="tool-title">{tool["name"]}</h4>
                <p class="tool-desc">{tool["desc"]}</p>
            </div>
            <a href="{tool["link"]}" target="_blank" class="tool-button">
                Launch Tool →
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# Info Section
# ----------------------------
st.markdown("""
<div class="info-section">
    ✨ <strong>All tools are free to use</strong> ✨<br>
    Each tool opens in a new tab on Streamlit Cloud for a seamless experience<br>
    🔒 Your data stays private and secure 🔒
</div>
""", unsafe_allow_html=True)
