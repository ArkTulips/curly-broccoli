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

# Create toggle button using Streamlit columns for positioning
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light", 
                 help="Toggle dark/light mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Apply CSS based on theme state
if st.session_state.dark_mode:
    # Dark theme CSS (keeping original dark theme)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Dark theme styling */
        .stApp {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
        }
        
        /* Main title styling */
        .main-title {
            font-family: 'Poppins', sans-serif;
            font-size: 4.5rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(135deg, #ffffff 0%, #4ade80 20%, #3b82f6 40%, #8b5cf6 60%, #ec4899 80%, #ffffff 100%);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 25px 0 15px 0;
            text-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
            position: relative;
            z-index: 1;
        }
        
        .subtitle {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 30px;
            font-weight: 500;
            position: relative;
            z-index: 1;
            letter-spacing: 0.5px;
        }
        
        .tagline {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.85);
            margin-bottom: 50px;
            font-weight: 400;
            position: relative;
            z-index: 1;
            font-style: italic;
        }
        
        /* Tool cards - dark theme */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(2, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto;
            padding: 25px;
        }
        
        .tool-card {
            background: rgba(40, 44, 52, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px 30px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.6);
        }
        
        .tool-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 15px;
        }
        
        .tool-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            color: #c1c7d0;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        
        .tool-button {
            display: inline-block;
            padding: 12px 24px;
            background: #4F46E5;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .tool-button:hover {
            background: #3B37DB;
            text-decoration: none;
            color: white;
        }
        
        /* Info sections */
        .features-section {
            background: rgba(40, 44, 52, 0.85);
            backdrop-filter: blur(25px);
            border-radius: 15px;
            padding: 30px;
            margin: 40px auto;
            max-width: 1000px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .features-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.8rem;
            font-weight: 600;
            text-align: center;
            color: #ffffff;
            margin-bottom: 25px;
        }
        
        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .feature-item {
            background: rgba(60, 64, 72, 0.6);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #4F46E5;
        }
        
        .feature-title {
            font-weight: 600;
            color: #ffffff;
            font-size: 1.1rem;
            margin-bottom: 8px;
        }
        
        .feature-desc {
            color: rgba(255, 255, 255, 0.85);
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        .info-section {
            background: rgba(40, 44, 52, 0.85);
            backdrop-filter: blur(25px);
            border-radius: 15px;
            padding: 25px;
            margin: 40px auto;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.95);
            font-family: 'Poppins', sans-serif;
            max-width: 900px;
        }
        
        /* Responsive design */
        @media (max-width: 1024px) {
            .tools-grid {
                grid-template-columns: repeat(2, 1fr);
                grid-template-rows: repeat(3, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .main-title {
                font-size: 3.2rem;
            }
            .tools-grid {
                grid-template-columns: 1fr;
                padding: 15px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
else:
    # Professional Light theme CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Professional light theme styling */
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
            color: #1a202c;
            font-family: 'Inter', sans-serif;
        }
        
        /* Main title styling */
        .main-title {
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            text-align: center;
            color: #1a365d;
            margin: 40px 0 20px 0;
            letter-spacing: -0.02em;
        }
        
        .subtitle {
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            color: #4a5568;
            margin-bottom: 20px;
            font-weight: 500;
        }
        
        .tagline {
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #718096;
            margin-bottom: 60px;
            font-weight: 400;
            font-style: italic;
        }
        
        /* Professional tool cards */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .tool-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
            min-height: 160px;
            display: flex;
            flex-direction: column;
        }
        
        .tool-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
            border-color: #cbd5e0;
        }
        
        .tool-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .tool-desc {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #718096;
            line-height: 1.5;
            margin-bottom: 16px;
            flex-grow: 1;
        }
        
        .tool-button {
            display: inline-block;
            padding: 8px 16px;
            background: #4F46E5;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.2s ease;
            align-self: flex-start;
        }
        
        .tool-button:hover {
            background: #3B37DB;
            text-decoration: none;
            color: white;
        }
        
        /* Professional info sections */
        .features-section {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 32px;
            margin: 48px auto;
            max-width: 1000px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .features-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            text-align: center;
            color: #2d3748;
            margin-bottom: 28px;
        }
        
        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        
        .feature-item {
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4F46E5;
        }
        
        .feature-title {
            font-weight: 600;
            color: #2d3748;
            font-size: 1rem;
            margin-bottom: 8px;
        }
        
        .feature-desc {
            color: #4a5568;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .info-section {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 28px;
            margin: 48px auto;
            text-align: center;
            color: #4a5568;
            font-family: 'Inter', sans-serif;
            max-width: 900px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        /* Responsive design */
        @media (max-width: 1024px) {
            .tools-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .main-title {
                font-size: 2.5rem;
            }
            .tools-grid {
                grid-template-columns: 1fr;
            }
            .tool-card {
                min-height: 140px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
# Header section without emojis
st.markdown("""
<h1 class="main-title">Capital Compass</h1>
<p class="subtitle"><strong>All your financial solutions in one place</strong></p>
<p class="tagline">"Where Smart Money Decisions Begin"</p>
""", unsafe_allow_html=True)



# Simplified tools data without emojis
tools = [
    {
        "name": "SIP Calculator",
        "desc": "Master Systematic Investment Planning with advanced projections and wealth growth analysis for mutual funds and equity investments.",
        "link": "https://financialreach.streamlit.app/"
    },
    {
        "name": "Credit Score Estimator", 
        "desc": "AI-Powered Credit Analysis using CIBIL-compatible algorithms with accurate score estimates and improvement strategies.",
        "link": "https://creditscores.streamlit.app/"
    },
    {
        "name": "Tax Calculator",
        "desc": "Smart Tax Optimization for India's tax regime with liability calculations and deduction comparisons.",
        "link": "https://taxreturncalc.streamlit.app/"
    },
    {
        "name": "EMI Calculator",
        "desc": "Complete Loan Planning Suite with EMI calculations, amortization schedules, and prepayment analysis.",
        "link": "https://emicalculatorsj.streamlit.app/"
    },
    {
        "name": "Expense Tracker",
        "desc": "Intelligent Expense Management with AI-powered categorization and smart budgeting insights.",
        "link": "https://expensetrac.streamlit.app/"
    },
    {
        "name": "Retirement Planner",
        "desc": "Strategic Retirement Planning with inflation-adjusted calculations and corpus estimation tools.",
        "link": "https://retirementtrack.streamlit.app/"
    }
]

# Create simple tools grid
st.markdown('<div class="tools-grid">', unsafe_allow_html=True)
for tool in tools:
    st.markdown(
        f"""
        <div class="tool-card">
            <h4 class="tool-title">{tool["name"]}</h4>
            <p class="tool-desc">{tool["desc"]}</p>
            <a href="{tool["link"]}" target="_blank" class="tool-button">
                Launch Tool
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Enhanced description section without emojis
st.markdown("""
<div class="features-section">
    <h2 class="features-title">What Makes Capital Compass Unique?</h2>
    <div class="features-list">        
        <div class="feature-item">
            <div class="feature-title"><strong>Lightning Fast</strong></div>
            <div class="feature-desc">Get instant results with our optimized calculation engine - no waiting, no delays</div>
        </div>
        <div class="feature-item">
            <div class="feature-title"><strong>Mobile-First Design</strong></div>
            <div class="feature-desc">Perfect experience across all devices with responsive, touch-friendly interfaces</div>
        </div>
        <div class="feature-item">
            <div class="feature-title"><strong>Personalized Insights</strong></div>
            <div class="feature-desc">Smart recommendations based on your financial profile and Indian market conditions</div>
        </div>
        <div class="feature-item">
            <div class="feature-title"><strong>Interactive Visualizations</strong></div>
            <div class="feature-desc">Beautiful charts and graphs that make complex financial data easy to understand</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Enhanced info section without emojis
st.markdown("""
<div class="info-section">
    <strong>Completely Free Forever</strong><br>
    <strong>Zero Data Storage • No Registration Required • Instant Results</strong><br><br>
    <em>Powered by cutting-edge fintech algorithms trusted by leading financial institutions</em>
</div>
""", unsafe_allow_html=True)
