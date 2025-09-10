import streamlit as st
import streamlit.components.v1 as components

# Page configuration with enhanced settings
st.set_page_config(
    page_title="Finance Tools - Your Financial Companion", 
    layout="wide",
    page_icon="💰",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with dark/light mode toggle functionality
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* CSS Variables for Theme Colors */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --primary-gradient-light: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bg-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-bg: rgba(255, 255, 255, 0.95);
        --card-hover-bg: rgba(255, 255, 255, 1);
        --text-primary: #2c3e50;
        --text-secondary: #6c757d;
        --text-light: rgba(255, 255, 255, 0.9);
        --shadow-color: rgba(0, 0, 0, 0.1);
        --shadow-hover: rgba(102, 126, 234, 0.3);
        --border-color: rgba(255, 255, 255, 0.3);
        --info-bg: rgba(255, 255, 255, 0.15);
        --button-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Dark Theme Variables */
    [data-theme="dark"] {
        --primary-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        --bg-color: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        --card-bg: rgba(40, 44, 52, 0.95);
        --card-hover-bg: rgba(50, 54, 62, 1);
        --text-primary: #ffffff;
        --text-secondary: #b8bcc8;
        --text-light: rgba(255, 255, 255, 0.9);
        --shadow-color: rgba(0, 0, 0, 0.3);
        --shadow-hover: rgba(102, 126, 234, 0.4);
        --border-color: rgba(255, 255, 255, 0.1);
        --info-bg: rgba(40, 44, 52, 0.8);
        --button-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main app styling */
    .stApp {
        background: var(--bg-color);
        transition: all 0.3s ease;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Theme Toggle Button */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 50px;
        padding: 12px 16px;
        cursor: pointer;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px var(--shadow-color);
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .theme-toggle:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px var(--shadow-hover);
        background: var(--card-hover-bg);
    }

    .theme-toggle-icon {
        font-size: 1.5rem;
        transition: transform 0.3s ease;
    }

    .theme-toggle:hover .theme-toggle-icon {
        transform: rotate(180deg);
    }

    .theme-toggle-text {
        font-size: 0.9rem;
        font-weight: 500;
        margin-left: 5px;
    }

    /* Animated background overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        animation: backgroundFloat 8s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
        transition: all 0.3s ease;
    }

    [data-theme="dark"] .stApp::before {
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
    }

    @keyframes backgroundFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
    }

    /* Title styling - centered */
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 20px 0 10px 0;
        text-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }

    [data-theme="dark"] .main-title {
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .subtitle {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        color: var(--text-light);
        margin-bottom: 40px;
        font-weight: 400;
        position: relative;
        z-index: 1;
        transition: color 0.3s ease;
    }

    /* Logo container */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
    }

    .logo {
        width: 100px;
        height: 100px;
        background: var(--info-bg);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
        border: 2px solid var(--border-color);
        box-shadow: 0 8px 32px var(--shadow-color);
        font-size: 3rem;
        animation: logoFloat 3s ease-in-out infinite;
        transition: all 0.3s ease;
    }

    @keyframes logoFloat {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-10px) scale(1.05); }
    }

    /* Tool cards - theme adaptive */
    .tool-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 35px 25px;
        margin: 15px;
        text-align: center;
        box-shadow: 0 8px 32px var(--shadow-color);
        border: 1px solid var(--border-color);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .tool-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--button-gradient);
        background-size: 200% 100%;
        animation: gradientShift 3s ease infinite;
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    .tool-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 20px 60px var(--shadow-hover);
        background: var(--card-hover-bg);
    }

    .tool-icon {
        font-size: 4.5rem;
        margin-bottom: 20px;
        filter: drop-shadow(0 8px 16px var(--shadow-color));
        transition: transform 0.3s ease;
    }

    .tool-card:hover .tool-icon {
        transform: scale(1.1) rotate(5deg);
    }

    .tool-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 15px;
        line-height: 1.3;
        transition: color 0.3s ease;
    }

    .tool-desc {
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 25px;
        flex-grow: 1;
        font-weight: 400;
        transition: color 0.3s ease;
    }

    .tool-button {
        display: inline-block;
        padding: 15px 35px;
        background: var(--button-gradient);
        color: white;
        text-decoration: none;
        border-radius: 50px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }

    .tool-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }

    .tool-button:hover::before {
        left: 100%;
    }

    .tool-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
        text-decoration: none;
        color: white;
    }

    /* Grid layout for tools */
    .tools-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 20px;
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }

    /* Info section styling */
    .info-section {
        background: var(--info-bg);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        margin: 40px auto;
        text-align: center;
        border: 1px solid var(--border-color);
        color: var(--text-light);
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        max-width: 800px;
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.8rem;
        }

        .tools-grid {
            grid-template-columns: 1fr;
            padding: 10px;
        }

        .tool-card {
            margin: 10px 0;
            padding: 25px 20px;
            min-height: 280px;
        }

        .logo {
            width: 80px;
            height: 80px;
            font-size: 2.5rem;
        }

        .theme-toggle {
            top: 15px;
            right: 15px;
            padding: 10px 12px;
        }

        .theme-toggle-text {
            display: none;
        }
    }

    @media (max-width: 480px) {
        .main-title {
            font-size: 2.2rem;
        }

        .tool-icon {
            font-size: 3.5rem;
        }

        .tool-title {
            font-size: 1.4rem;
        }

        .theme-toggle {
            top: 10px;
            right: 10px;
            padding: 8px 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for theme toggle functionality
theme_toggle_js = """
<script>
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', newTheme);

    // Update toggle button
    const toggleBtn = document.getElementById('themeToggle');
    const toggleIcon = document.getElementById('toggleIcon');
    const toggleText = document.getElementById('toggleText');

    if (newTheme === 'dark') {
        toggleIcon.textContent = '🌙';
        toggleText.textContent = 'Dark';
    } else {
        toggleIcon.textContent = '☀';
        toggleText.textContent = 'Light';
    }

    // Try to store preference (may not work in Streamlit sandbox)
    try {
        localStorage.setItem('theme', newTheme);
    } catch (e) {
        console.log('LocalStorage not available');
    }
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
    let savedTheme = 'light';

    // Try to get saved theme
    try {
        savedTheme = localStorage.getItem('theme') || 'light';
    } catch (e) {
        console.log('LocalStorage not available, using default theme');
    }

    const html = document.documentElement;
    html.setAttribute('data-theme', savedTheme);

    // Update toggle button
    const toggleIcon = document.getElementById('toggleIcon');
    const toggleText = document.getElementById('toggleText');

    if (savedTheme === 'dark') {
        toggleIcon.textContent = '🌙';
        toggleText.textContent = 'Dark';
    } else {
        toggleIcon.textContent = '☀';
        toggleText.textContent = 'Light';
    }
});

// Re-run initialization when Streamlit reruns
setTimeout(function() {
    let savedTheme = 'light';
    try {
        savedTheme = localStorage.getItem('theme') || 'light';
    } catch (e) {
        console.log('LocalStorage not available');
    }

    const html = document.documentElement;
    html.setAttribute('data-theme', savedTheme);

    const toggleIcon = document.getElementById('toggleIcon');
    const toggleText = document.getElementById('toggleText');

    if (toggleIcon && toggleText) {
        if (savedTheme === 'dark') {
            toggleIcon.textContent = '🌙';
            toggleText.textContent = 'Dark';
        } else {
            toggleIcon.textContent = '☀';
            toggleText.textContent = 'Light';
        }
    }
}, 100);
</script>
"""

# Inject the JavaScript
components.html(theme_toggle_js, height=0)

# Theme Toggle Button
st.markdown("""
<div class="theme-toggle" id="themeToggle" onclick="toggleTheme()">
    <span class="theme-toggle-icon" id="toggleIcon">☀</span>
    <span class="theme-toggle-text" id="toggleText">Light</span>
</div>
""", unsafe_allow_html=True)

# Logo and centered title
st.markdown("""
<div class="logo-container">
    <div class="logo">💰</div>
</div>
<h1 class="main-title">Finance Tools</h1>
<p class="subtitle">Your comprehensive financial companion for smart money management</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Enhanced tools data with better descriptions
tools = [
    {
        "name": "SIP Calculator",
        "desc": "Calculate your Systematic Investment Plan returns with detailed projections and wealth growth analysis for long-term financial planning.",
        "link": "https://financialreach.streamlit.app/",
        "icon": "📈"
    },
    {
        "name": "Credit Score Estimator", 
        "desc": "Get accurate credit score estimates using advanced CIBIL-like algorithms and receive personalized tips to improve your creditworthiness.",
        "link": "https://creditscores.streamlit.app/",
        "icon": "💳"
    },
    {
        "name": "Tax Calculator",
        "desc": "Calculate your income tax liability under India's new tax regime with comprehensive breakdowns, savings analysis, and tax planning insights.",
        "link": "https://taxreturncalc.streamlit.app/",
        "icon": "🧾"
    },
    {
        "name": "EMI Calculator",
        "desc": "Plan your loan repayments with precision. Calculate EMIs for home loans, personal loans, and vehicle loans with detailed amortization schedules.",
        "link": "https://emicalculatorsj.streamlit.app/",
        "icon": "🏦"
    },
    {
        "name": "Expense Tracker",
        "desc": "Take complete control of your finances by tracking daily expenses, setting smart budgets, and analyzing detailed spending patterns.",
        "link": "https://expensetrac.streamlit.app/",
        "icon": "💵"
    }
]

# Create tools grid with enhanced cards
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

# Enhanced info section
st.markdown("""
<div class="info-section">
    ✨ <strong>All tools are free to use</strong> ✨<br>
    Each tool opens in a new tab on Streamlit Cloud for seamless experience<br>
    🔒 Your data stays private and secure 🔒
</div>
""", unsafe_allow_html=True)
