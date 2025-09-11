import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration
st.set_page_config(
    page_title=" Advanced CIBIL Score Estimator", 
    layout="wide",
    page_icon=""
)

# Initialize session state for credit score data
if 'calculated_score' not in st.session_state:
    st.session_state.calculated_score = None
if 'score_category' not in st.session_state:
    st.session_state.score_category = None
if 'score_recommendations' not in st.session_state:
    st.session_state.score_recommendations = []

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

# Professional Images Integration
hero_image_url = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
dashboard_image_url = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
analytics_image_url = "https://plus.unsplash.com/premium_photo-1682310156923-3f4a463610f0?q=80&w=912&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
calculator_image_url = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"

# Custom CSS for enhanced styling including credit score dashboard
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Credit Score Dashboard Styling */
    .credit-score-dashboard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 20px auto;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 320px;
        position: relative;
        overflow: hidden;
    }
    
    .credit-score-dashboard::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .dashboard-content {
        position: relative;
        z-index: 1;
    }
    
    .dashboard-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 12px;
        opacity: 0.9;
    }
    
    .dashboard-score {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 8px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-category {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 16px;
        padding: 4px 12px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        display: inline-block;
    }
    
    .dashboard-recommendations {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 16px;
        margin-top: 16px;
        text-align: left;
    }
    
    .recommendation-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 8px;
        color: #fff;
    }
    
    .recommendation-item {
        font-size: 0.8rem;
        line-height: 1.4;
        margin-bottom: 6px;
        padding-left: 12px;
        position: relative;
        opacity: 0.95;
    }
    
    .recommendation-item::before {
        content: '💡';
        position: absolute;
        left: 0;
        top: 0;
    }
    
    .dashboard-placeholder {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 20px auto;
        text-align: center;
        color: #4a5568;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 2px dashed #a0aec0;
        max-width: 320px;
    }
    
    .placeholder-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
        opacity: 0.6;
    }
    
    .placeholder-text {
        font-size: 1rem;
        font-weight: 500;
        line-height: 1.4;
    }
    
    /* Theme-specific styling */
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
        margin-bottom: 40px;
        font-weight: 400;
        font-style: italic;
    }
    
    /* Hero section styling */
    .hero-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 40px auto 60px auto;
        max-width: 1200px;
        padding: 40px 20px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        gap: 40px;
    }
    
    .hero-content {
        flex: 1;
        max-width: 500px;
    }
    
    .hero-image {
        flex: 1;
        max-width: 500px;
    }
    
    .hero-image img {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .hero-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 20px;
        line-height: 1.3;
    }
    
    .hero-desc {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #4a5568;
        margin-bottom: 25px;
    }
    
    .badge-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    .badge {
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        color: white;
    }
    
    .badge-primary { background: #4F46E5; }
    .badge-success { background: #10B981; }
    .badge-warning { background: #F59E0B; }
    
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
        .hero-section {
            flex-direction: column;
            text-align: center;
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
        .credit-score-dashboard {
            max-width: 280px;
        }
    }
</style>
""", unsafe_allow_html=True)

def calculate_enhanced_cibil_score(payment_history, credit_utilization, credit_history_years, 
                                 credit_mix, recent_inquiries, total_accounts, outstanding_debt,
                                 total_credit_limit, income_range, employment_type, late_payments,
                                 settled_accounts):
    """
    Enhanced CIBIL score calculation with additional factors
    """
    # Base weights (adjusted based on research)
    weights = {
        "payment_history": 0.35,
        "credit_utilization": 0.30,
        "credit_history": 0.15,
        "credit_mix": 0.10,
        "recent_inquiries": 0.10
    }
    
    # Payment history score (35%)
    ph_score = payment_history * weights["payment_history"]
    
    # Adjust for late payments
    late_payment_penalty = min(late_payments * 5, 20)
    ph_score = max(0, ph_score - (late_payment_penalty * weights["payment_history"] / 100))
    
    # Adjust for settled accounts
    settled_penalty = settled_accounts * 10
    ph_score = max(0, ph_score - (settled_penalty * weights["payment_history"] / 100))
    
    # Credit utilization score (30%)
    cu_score = (100 - credit_utilization) * weights["credit_utilization"]
    
    # Bonus for very low utilization
    if credit_utilization < 10:
        cu_score *= 1.1
    elif credit_utilization > 70:
        cu_score *= 0.8
    
    # Credit history score (15%)
    ch_score = min(credit_history_years * 7, 100) * weights["credit_history"]
    
    # Bonus for very long history
    if credit_history_years > 10:
        ch_score *= 1.1
    
    # Credit mix score (10%)
    cm_score = credit_mix * weights["credit_mix"]
    
    # Adjust for number of accounts
    if total_accounts < 3:
        cm_score *= 0.8
    elif total_accounts > 10:
        cm_score *= 0.9
    
    # Recent inquiries score (10%)
    ri_score = max(100 - (recent_inquiries * 20), 0) * weights["recent_inquiries"]
    
    # Additional factors adjustments
    # Income stability bonus
    income_bonus = 0
    if employment_type == "Salaried" and income_range == "Above 10 Lakhs":
        income_bonus = 5
    elif employment_type == "Self-employed" and income_range == "Above 10 Lakhs":
        income_bonus = 3
    elif income_range in ["5-10 Lakhs", "3-5 Lakhs"]:
        income_bonus = 2
    
    # Outstanding debt impact
    debt_impact = 0
    if outstanding_debt > 80:
        debt_impact = -10
    elif outstanding_debt > 50:
        debt_impact = -5
    elif outstanding_debt < 20:
        debt_impact = 2
    
    # Calculate total percentage
    total_percentage = ph_score + cu_score + ch_score + cm_score + ri_score + income_bonus + debt_impact
    
    # Convert to CIBIL score range (300-900)
    final_score = int(300 + (total_percentage / 100) * 600)
    
    # Ensure score is within bounds
    final_score = max(300, min(900, final_score))
    
    return final_score, {
        'payment_history': ph_score,
        'credit_utilization': cu_score,
        'credit_history': ch_score,
        'credit_mix': cm_score,
        'recent_inquiries': ri_score,
        'income_bonus': income_bonus,
        'debt_impact': debt_impact
    }

def get_score_category(score):
    """Get score category and color"""
    if score >= 750:
        return "Excellent", "excellent", "🌟"
    elif score >= 700:
        return "Good", "good", "✅"
    elif score >= 650:
        return "Fair", "fair", "⚠️"
    else:
        return "Poor", "poor", "❌"

def get_top_recommendations(score, credit_utilization, recent_inquiries, late_payments):
    """Get top 2 personalized recommendations"""
    recommendations = []
    
    # Priority-based recommendations
    if late_payments > 0:
        recommendations.append("Set up auto-pay for all bills to ensure 100% on-time payments")
    
    if credit_utilization > 30:
        recommendations.append(f"Reduce credit card usage to below 30% (currently {credit_utilization}%)")
    
    if recent_inquiries > 3:
        recommendations.append("Avoid applying for new credit for the next 6 months")
    
    # Default recommendations if none of the above apply
    if len(recommendations) == 0:
        if score < 750:
            recommendations.append("Maintain consistent payment history across all accounts")
            recommendations.append("Keep credit utilization below 10% for optimal score")
        else:
            recommendations.append("Excellent score! Monitor quarterly for any changes")
            recommendations.append("Consider becoming an authorized user on family accounts")
    
    # Return top 2 recommendations
    return recommendations[:2]

# Credit Score Dashboard Component
def display_credit_score_dashboard():
    if st.session_state.calculated_score is not None:
        score = st.session_state.calculated_score
        category = st.session_state.score_category
        recommendations = st.session_state.score_recommendations
        
        # Get emoji for category
        if score >= 750:
            emoji = "🌟"
        elif score >= 700:
            emoji = "✅"
        elif score >= 650:
            emoji = "⚠️"
        else:
            emoji = "❌"
        
        dashboard_html = f"""
        <div class="credit-score-dashboard">
            <div class="dashboard-content">
                <div class="dashboard-title">Your Credit Score</div>
                <div class="dashboard-score">{score}</div>
                <div class="dashboard-category">{emoji} {category}</div>
                <div class="dashboard-recommendations">
                    <div class="recommendation-title">Quick Improvements:</div>
                    {"".join([f'<div class="recommendation-item">{rec}</div>' for rec in recommendations[:2]])}
                </div>
            </div>
        </div>
        """
        st.markdown(dashboard_html, unsafe_allow_html=True)
    else:
        placeholder_html = """
        <div class="dashboard-placeholder">
            <div class="placeholder-icon">📊</div>
            <div class="placeholder-text">
                Calculate your credit score to see personalized insights here
            </div>
        </div>
        """
        st.markdown(placeholder_html, unsafe_allow_html=True)

# Header section
st.markdown("""
<h1 class="main-title">Capital Compass</h1>
<p class="subtitle"><strong>All your financial solutions in one place</strong></p>
<p class="tagline">"Where Smart Money Decisions Begin"</p>
""", unsafe_allow_html=True)

# Hero section with professional image
st.markdown(f"""
<div class="hero-section">
    <div class="hero-content">
        <h2 class="hero-title">Professional Financial Management Made Simple</h2>
        <p class="hero-desc">
            Experience the power of comprehensive financial planning with our suite of professional-grade calculators and tools. 
            Designed for accuracy, built for professionals, trusted by thousands.
        </p>
        <div class="badge-container">
            <span class="badge badge-primary">Enterprise Ready</span>
            <span class="badge badge-success">Bank-Grade Security</span>
            <span class="badge badge-warning">Real-time Analytics</span>
        </div>
    </div>
    <div class="hero-image">
        <img src="{hero_image_url}" alt="Professional Financial Dashboard" />
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced description section
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

# Credit Score Dashboard (placed above tools)
st.markdown("## 📊 Your Financial Dashboard")
display_credit_score_dashboard()

st.markdown("## 🔧 Financial Tools")

# Tools section with updated layout
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
    },
    {
        "name": "Stock Market checker",
        "desc": "Check realtime stock prices of your favourite stocks",
        "link": "https://demo-stockpeers.streamlit.app/?ref=streamlit-io-gallery-favorites&stocks=AAPL%2CMSFT%2CGOOGL%2CNVDA%2CAMZN%2CTSLA%2CMETA"
    }
]

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

# Quick Credit Score Calculator Section
st.markdown("---")
st.markdown("## 🎯 Quick Credit Score Calculator")

with st.expander("Calculate Your Credit Score Now", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Basic Information")
        payment_history = st.slider("Payment History (%)", 0, 100, 90, 
                                   help="Percentage of payments made on time")
        credit_utilization = st.slider("Credit Utilization (%)", 0, 100, 30, 
                                     help="Percentage of credit limit used")
        credit_history_years = st.slider("Credit History (Years)", 0, 25, 5,
                                        help="Age of your oldest credit account")
        credit_mix = st.slider("Credit Mix Score", 0, 100, 70,
                              help="Diversity of credit types")
    
    with col2:
        st.markdown("### Additional Details")
        recent_inquiries = st.slider("Recent Credit Inquiries", 0, 15, 1,
                                    help="Number of inquiries in last 12 months")
        total_accounts = st.number_input("Total Credit Accounts", min_value=0, max_value=20, value=3)
        outstanding_debt = st.slider("Outstanding Debt (%)", 0, 100, 25)
        total_credit_limit = st.number_input("Total Credit Limit (₹)", min_value=10000, 
                                           max_value=5000000, value=200000, step=10000)
        late_payments = st.number_input("Late Payments (Last 2 Years)", min_value=0, max_value=20, value=0)
        settled_accounts = st.number_input("Settled Accounts", min_value=0, max_value=10, value=0)
        
        employment_type = st.selectbox("Employment Type", 
                                     ["Salaried", "Self-employed", "Business Owner", "Retired", "Student"])
        income_range = st.selectbox("Annual Income Range",
                                  ["Below 3 Lakhs", "3-5 Lakhs", "5-10 Lakhs", "Above 10 Lakhs"])
    
    if st.button("🧮 Calculate My Credit Score", type="primary", use_container_width=True):
        # Calculate the score
        score, components = calculate_enhanced_cibil_score(
            payment_history, credit_utilization, credit_history_years,
            credit_mix, recent_inquiries, total_accounts, outstanding_debt,
            total_credit_limit, income_range, employment_type, late_payments,
            settled_accounts
        )
        
        category, css_class, emoji = get_score_category(score)
        recommendations = get_top_recommendations(score, credit_utilization, recent_inquiries, late_payments)
        
        # Store in session state
        st.session_state.calculated_score = score
        st.session_state.score_category = category
        st.session_state.score_recommendations = recommendations
        
        # Display result
        st.success(f"🎉 Your CIBIL Score: **{score}** ({category})")
        st.info("Your dashboard above has been updated with personalized recommendations!")
        st.rerun()

# Enhanced info section
st.markdown("""
<div class="info-section">
    <strong>Completely Free Forever</strong><br>
    <em>Powered by cutting-edge fintech algorithms trusted by leading financial institutions</em>
</div>
""", unsafe_allow_html=True)
