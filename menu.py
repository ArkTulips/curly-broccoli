import streamlit as st

# Page config
st.set_page_config(
    page_title="Finance Tools - Your Financial Companion",
    layout="wide",
    page_icon="💰",
    initial_sidebar_state="expanded",
)

# Initialize theme state in session
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar toggle for dark/light mode
with st.sidebar:
    st.markdown("## Theme Settings")
    dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode

# Define CSS for light and dark themes
light_theme_css = """
<style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #000000;
    }
    .tool-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1) !important;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        text-align: center;
    }
    h4 {
        color: #000000 !important;
    }
    p {
        color: #555555 !important;
    }
    a {
        color: #ffffff !important;
        background-color: #4CAF50;
        padding: 10px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
</style>
"""

dark_theme_css = """
<style>
    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
    }
    .tool-card {
        background-color: #2c3e50 !important;
        color: #ffffff !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.5) !important;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        text-align: center;
    }
    h4 {
        color: #ffffff !important;
    }
    p {
        color: #bbbbbb !important;
    }
    a {
        color: #ffffff !important;
        background-color: #4CAF50;
        padding: 10px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
</style>
"""

# Apply theme CSS
if st.session_state.dark_mode:
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)

# Main title centered
st.markdown(
    """
    <h1 style="text-align:center; font-family:sans-serif; font-size:3rem; margin-bottom:1rem;">
    Finance Tools
    </h1>
    <p style="text-align:center; font-family:sans-serif; font-size:1.2rem; margin-top:0; color:gray;">
    Your comprehensive financial companion for smart money management
    </p>
    """,
    unsafe_allow_html=True,
)

st.write("Welcome! Select a tool below to get started:")
st.markdown("---")

# List of tools
tools = [
    {
        "name": "SIP Calculator",
        "desc": "Calculate SIP returns and profit percentage.",
        "link": "https://financialreach.streamlit.app/",
        "icon": "📈",
    },
    {
        "name": "Credit Score Estimator",
        "desc": "Estimate your credit score based on CIBIL-like logic.",
        "link": "https://creditscores.streamlit.app/",
        "icon": "💳",
    },
    {
        "name": "Tax Calculator",
        "desc": "Calculate your income tax under the new regime.",
        "link": "https://taxreturncalc.streamlit.app/",
        "icon": "🧾",
    },
    {
        "name": "EMI Calculator",
        "desc": "Calculate your monthly loan EMI.",
        "link": "https://emicalculatorsj.streamlit.app/",
        "icon": "🏦",
    },
    {
        "name": "Expense Tracker",
        "desc": "Track your monthly and overall expenses.",
        "link": "https://expensetrac.streamlit.app/",
        "icon": "💵",
    },
]

# Display tools in 3 columns
cols = st.columns(3)
for i, tool in enumerate(tools):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="tool-card">
                <div style="font-size:100px; margin-bottom:10px;">{tool['icon']}</div>
                <h4>{tool['name']}</h4>
                <p style="font-size:20px;">{tool['desc']}</p>
                <a href="{tool['link']}" target="_blank" rel="noopener noreferrer">Open Tool ➡️</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.info("Each tool will open in a new tab on Streamlit Cloud.")
