import streamlit as st
import streamlit.components.v1 as components

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Finance Tools", layout="centered")

# ----------------------------
# SESSION STATE FOR THEME
# ----------------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# ----------------------------
# THEME TOGGLE BUTTON + SCRIPT
# ----------------------------
components.html(f"""
<div class="theme-toggle" id="themeToggle" onclick="toggleTheme()" 
     style="cursor:pointer; font-size:20px; display:flex; align-items:center; gap:8px;">
    <span id="toggleIcon">{'☀' if st.session_state["theme"] == 'light' else '🌙'}</span>
    <span id="toggleText">{st.session_state["theme"].capitalize()}</span>
</div>

<script>
function toggleTheme() {{
    const html = parent.document.documentElement; 
    const currentTheme = html.getAttribute('data-theme') || '{st.session_state["theme"]}';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);

    const icon = parent.document.getElementById('toggleIcon');
    const text = parent.document.getElementById('toggleText');
    if (newTheme === 'dark') {{
        icon.textContent = '🌙';
        text.textContent = 'Dark';
    }} else {{
        icon.textContent = '☀';
        text.textContent = 'Light';
    }}

    // Update Streamlit state via localStorage
    localStorage.setItem('theme', newTheme);
}}

// Initialize theme on load
document.addEventListener("DOMContentLoaded", function() {{
    let savedTheme = localStorage.getItem("theme") || "{st.session_state["theme"]}";
    parent.document.documentElement.setAttribute('data-theme', savedTheme);

    const icon = parent.document.getElementById('toggleIcon');
    const text = parent.document.getElementById('toggleText');
    if (savedTheme === 'dark') {{
        icon.textContent = '🌙';
        text.textContent = 'Dark';
    }} else {{
        icon.textContent = '☀';
        text.textContent = 'Light';
    }}
}});
</script>
""", height=50)

# ----------------------------
# DASHBOARD CONTENT
# ----------------------------
st.title("💰 Finance Tools Dashboard")
st.write("Welcome! Use the links below to navigate to your preferred financial tool.")

st.markdown("---")

tools = [
    ("📈", "SIP Calculator", "Calculate SIP returns and profit percentage.", "https://financialreach.streamlit.app/"),
    ("💳", "Credit Score Estimator", "Estimate your credit score based on CIBIL-like logic.", "https://creditscores.streamlit.app/"),
    ("🧾", "Tax Calculator", "Calculate your income tax under the new regime.", "https://yourname-tax.streamlit.app"),
    ("🏦", "EMI Calculator", "Calculate your loan EMI easily.", "https://emicalculatorsj.streamlit.app/"),
    ("📊", "Expense Tracker", "Track and analyze your monthly expenses.", "https://expensetrac.streamlit.app/")
]

for icon, title, desc, link in tools:
    st.markdown(f"""
    <div style="padding:15px; border-radius:12px; border:1px solid #ddd; margin-bottom:15px;">
        <h3 style="font-size:24px;">{icon} {title}</h3>
        <p style="font-size:16px;">{desc}</p>
        <a href="{link}" target="_blank" style="text-decoration:none; 
            background:#4CAF50; color:white; padding:8px 15px; 
            border-radius:8px; font-size:16px;">Open Tool</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("Each tool opens in a new tab on Streamlit Cloud.")
