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

# Apply CSS based on theme state
if st.session_state.dark_mode:
    # Dark theme CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Dark theme styling */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
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
                radial-gradient(circle at 25% 25%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
            animation: backgroundFloat 8s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes backgroundFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(2deg); }
        }

        /* Title styling */
        .main-title {
            font-family: 'Poppins', sans-serif;
            font-size: 4rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 20px 0 10px 0;
            text-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
            position: relative;
            z-index: 1;
        }

        .subtitle {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 40px;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }

        /* Logo styling */
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
            background: rgba(40, 44, 52, 0.8);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            font-size: 3rem;
            animation: logoFloat 3s ease-in-out infinite;
        }

        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.05); }
        }

        /* Tool cards - dark theme */
        .tool-card {
            background: rgba(40, 44, 52, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 35px 25px;
            margin: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-size: 200% 100%;
            animation: gradientShift 3s ease infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .tool-card:hover {
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
            background: rgba(50, 54, 62, 1);
        }

        .tool-icon {
            font-size: 4.5rem;
            margin-bottom: 20px;
            filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.3));
            transition: transform 0.3s ease;
        }

        .tool-card:hover .tool-icon {
            transform: scale(1.1) rotate(5deg);
        }

        .tool-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.6rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 15px;
            line-height: 1.3;
        }

        .tool-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            color: #b8bcc8;
            line-height: 1.6;
            margin-bottom: 25px;
            flex-grow: 1;
            font-weight: 400;
        }

        .tool-button {
            display: inline-block;
            padding: 15px 35px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

        .tool-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
            text-decoration: none;
            color: white;
        }

        /* Grid layout */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Info section */
        .info-section {
            background: rgba(40, 44, 52, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 25px;
            margin: 40px auto;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.9);
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            max-width: 800px;
            position: relative;
            z-index: 1;
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
        }
    </style>
    """, unsafe_allow_html=True)

else:
    # Light theme CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Light theme styling */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: black;
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
        }

        @keyframes backgroundFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(2deg); }
        }

        /* Title styling */
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
        }

        .subtitle {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 40px;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }

        /* Logo styling */
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
            background: rgba(255, 255, 255, 0.15);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(255, 255, 255, 0.2);
            font-size: 3rem;
            animation: logoFloat 3s ease-in-out infinite;
        }

        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.05); }
        }

        /* Tool cards - light theme */
        .tool-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 35px 25px;
            margin: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-size: 200% 100%;
            animation: gradientShift 3s ease infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .tool-card:hover {
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
            background: rgba(255, 255, 255, 1);
        }

        .tool-icon {
            font-size: 4.5rem;
            margin-bottom: 20px;
            filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.15));
            transition: transform 0.3s ease;
        }

        .tool-card:hover .tool-icon {
            transform: scale(1.1) rotate(5deg);
        }

        .tool-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.6rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.3;
        }

        .tool-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            color: #6c757d;
            line-height: 1.6;
            margin-bottom: 25px;
            flex-grow: 1;
            font-weight: 400;
        }

        .tool-button {
            display: inline-block;
            padding: 15px 35px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

        .tool-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
            text-decoration: none;
            color: white;
        }

        /* Grid layout */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Info section */
        .info-section {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 25px;
            margin: 40px auto;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 0.9);
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            max-width: 800px;
            position: relative;
            z-index: 1;
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
        }
    </style>
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
