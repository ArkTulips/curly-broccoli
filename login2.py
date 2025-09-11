import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Capital Compass - Your Ultimate Financial Companion",
    layout="wide",
    page_icon="💰",
    initial_sidebar_state="collapsed"
)

# Initialize theme state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Custom CSS
def load_custom_css():
    st.markdown("""
        <style>
        /* Reduce top padding */
        .block-container {
            padding-top: 1rem !important;
        }

        /* Global styles */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
        }

        /* Navbar styles */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: var(--card-bg);
            border-radius: 12px;
            margin-bottom: 2rem;
        }

        .nav-links a {
            margin: 0 1rem;
            text-decoration: none;
            color: var(--text-color);
            font-weight: 500;
        }

        .nav-links a:hover {
            color: var(--accent-color);
        }

        /* Hero section */
        .hero {
            text-align: center;
            padding: 3rem 1rem;
            border-radius: 16px;
            background: var(--card-bg);
            margin-bottom: 3rem;
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--secondary-text);
        }

        /* Card styles */
        .tool-card {
            background-color: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.2s ease-in-out;
        }

        .tool-card:hover {
            transform: translateY(-5px);
        }

        .tool-card h3 {
            margin-top: 0;
        }

        .tool-card a {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.5rem 1rem;
            background-color: var(--accent-color);
            color: white;
            border-radius: 8px;
            text-decoration: none;
        }

        .tool-card a:hover {
            background-color: var(--accent-hover);
        }

        /* Light & Dark themes */
        .light-theme {
            --bg-color: #f5f7fa;
            --text-color: #1a1a1a;
            --secondary-text: #555;
            --card-bg: #ffffff;
            --accent-color: #007bff;
            --accent-hover: #0056b3;
        }

        .dark-theme {
            --bg-color: #121212;
            --text-color: #f5f5f5;
            --secondary-text: #bbb;
            --card-bg: #1e1e1e;
            --accent-color: #0d6efd;
            --accent-hover: #0b5ed7;
        }
        </style>
    """, unsafe_allow_html=True)

# Apply theme
theme_class = "dark-theme" if st.session_state.dark_mode else "light-theme"
st.markdown(f'<div class="{theme_class}">', unsafe_allow_html=True)

load_custom_css()

# Navbar
st.markdown("""
<div class="navbar">
    <div class="logo">
        <h2>💰 Capital Compass</h2>
    </div>
    <div class="nav-links">
        <a href="#sip">SIP Calculator</a>
        <a href="#loan">Loan Planner</a>
        <a href="#retirement">Retirement Planner</a>
        <a href="#credit">Credit Score Tool</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>Capital Compass</h1>
    <p>Your all-in-one financial companion – plan, calculate, and achieve your financial goals.</p>
</div>
""", unsafe_allow_html=True)

# Dark Mode Toggle
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Tools Section
st.subheader("📊 Financial Tools")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div id="sip" class="tool-card">
        <h3>📈 SIP Calculator</h3>
        <p>Plan your investments and estimate future returns with our powerful SIP calculator.</p>
        <a href="https://sip-calculator.streamlit.app" target="_blank">Open Tool</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="loan" class="tool-card">
        <h3>🏦 Loan Planner</h3>
        <p>Calculate EMIs, repayment schedules, and manage your loan effectively.</p>
        <a href="https://loan-planner.streamlit.app" target="_blank">Open Tool</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div id="retirement" class="tool-card">
        <h3>👴 Retirement Planner</h3>
        <p>Secure your future with personalized retirement planning tools and projections.</p>
        <a href="https://retirement-planner.streamlit.app" target="_blank">Open Tool</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="credit" class="tool-card">
        <h3>💳 Credit Score Tool</h3>
        <p>Predict and analyze your credit score based on financial habits and profiles.</p>
        <a href="https://credit-score-tool.streamlit.app" target="_blank">Open Tool</a>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<hr>
<p style='text-align: center; color: gray;'>
    © 2025 Capital Compass. All rights reserved.
</p>
""", unsafe_allow_html=True)

# Close theme wrapper
st.markdown("</div>", unsafe_allow_html=True)
