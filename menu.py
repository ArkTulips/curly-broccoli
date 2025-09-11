import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Capital Compass - Your Ultimate Financial Companion", 
    layout="wide",
    page_icon="",
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
    # Professional Dark theme CSS with consistent tool cards
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Dark theme styling */
        .stApp {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            font-family: 'Inter', sans-serif;
        }
        
        /* Main title styling */
        .main-title {
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            text-align: center;
            color: #ffffff;
            margin: 40px 0 20px 0;
            letter-spacing: -0.02em;
        }
        
        .subtitle {
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            color: #e2e8f0;
            margin-bottom: 20px;
            font-weight: 500;
        }
        
        .tagline {
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #cbd5e0;
            margin-bottom: 60px;
            font-weight: 400;
            font-style: italic;
        }
        
        /* Professional tool cards - SAME AS LIGHT THEME */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .tool-card {
            background: #2d3748;
            border: 1px solid #4a5568;
            border-radius: 12px;
            padding: 24px;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.2s ease;
            min-height: 160px;
            display: flex;
            flex-direction: column;
        }
        
        .tool-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            transform: translateY(-2px);
            border-color: #718096;
        }
        
        .tool-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .tool-desc {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #cbd5e0;
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
            background: #2d3748;
            border: 1px solid #4a5568;
            border-radius: 12px;
            padding: 32px;
            margin: 48px auto;
            max-width: 1000px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .features-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            text-align: center;
            color: #ffffff;
            margin-bottom: 28px;
        }
        
        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        
        .feature-item {
            background: #374151;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4F46E5;
        }
        
        .feature-title {
            font-weight: 600;
            color: #ffffff;
            font-size: 1rem;
            margin-bottom: 8px;
        }
        
        .feature-desc {
            color: #d1d5db;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .info-section {
            background: #2d3748;
            border: 1px solid #4a5568;
            border-radius: 12px;
            padding: 28px;
            margin: 48px auto;
            text-align: center;
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
            max-width: 900px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
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
    
else:
    # Professional Light theme CSS (unchanged)
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

# Enhanced info section without emojis
st.markdown("""
<div class="info-section">
    <strong>Completely Free Forever</strong><br>
    <strong>Zero Data Storage • No Registration Required • Instant Results</strong><br><br>
    <em>Powered by cutting-edge fintech algorithms trusted by leading financial institutions</em>
</div>
""", unsafe_allow_html=True)
