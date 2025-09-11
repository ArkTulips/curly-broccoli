import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os
from datetime import datetime
import hashlib

# Set page configuration
st.set_page_config(
    page_title="Capital Compass - Financial Management Platform", 
    layout="wide",
    page_icon="💰"
)

# File paths for data storage
USERS_FILE = "users_data.json"
USER_PROFILES_FILE = "user_profiles.json"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'profile_completed' not in st.session_state:
    st.session_state.profile_completed = False
if 'calculated_score' not in st.session_state:
    st.session_state.calculated_score = None
if 'score_category' not in st.session_state:
    st.session_state.score_category = None
if 'score_recommendations' not in st.session_state:
    st.session_state.score_recommendations = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_user_profiles():
    """Load user profiles from JSON file"""
    if os.path.exists(USER_PROFILES_FILE):
        try:
            with open(USER_PROFILES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_profiles(profiles):
    """Save user profiles to JSON file"""
    with open(USER_PROFILES_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

def register_user(email, password, full_name):
    """Register a new user"""
    users = load_users()
    if email in users:
        return False, "Email already exists"
    
    users[email] = {
        'password': hash_password(password),
        'full_name': full_name,
        'created_at': datetime.now().isoformat(),
        'last_login': None
    }
    save_users(users)
    return True, "Registration successful"

def authenticate_user(email, password):
    """Authenticate user login"""
    users = load_users()
    if email not in users:
        return False, "Email not found"
    
    if verify_password(password, users[email]['password']):
        users[email]['last_login'] = datetime.now().isoformat()
        save_users(users)
        return True, "Login successful"
    return False, "Invalid password"

def get_user_profile(email):
    """Get user profile data"""
    profiles = load_user_profiles()
    return profiles.get(email, None)

def save_user_profile(email, profile_data):
    """Save user profile data"""
    profiles = load_user_profiles()
    profiles[email] = profile_data
    save_user_profiles(profiles)

# Professional Login Page CSS with attractive images
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Inter', sans-serif;
    }
    
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 900px;
        width: 100%;
        margin: 20px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        align-items: center;
    }
    
    .login-left {
        text-align: center;
    }
    
    .login-right {
        padding: 20px;
    }
    
    .login-image {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }
    
    .login-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .login-subtitle {
        font-size: 1.1rem;
        color: #718096;
        margin-bottom: 30px;
        text-align: center;
        line-height: 1.5;
    }
    
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 8px;
        display: block;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .login-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    
    .login-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
    }
    
    .profile-setup {
        background: #f8fafc;
        min-height: 100vh;
        padding: 40px 20px;
        font-family: 'Inter', sans-serif;
    }
    
    .profile-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .profile-title {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #4a5568;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .welcome-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .main-dashboard {
        font-family: 'Inter', sans-serif;
    }
    
    .user-info-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logout-btn {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 0.9rem !important;
    }
    
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
    
    @media (max-width: 768px) {
        .login-card {
            grid-template-columns: 1fr;
            gap: 20px;
            padding: 30px;
        }
        
        .login-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def show_login_page():
    """Display the login/registration page"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Left side with image
    st.markdown("""
    <div class="login-left">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8ZGVmcz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY3ZWVhO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM3NjRiYTI7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogIDwvZGVmcz4KICA8cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0idXJsKCNncmFkaWVudCkiLz4KICA8dGV4dCB4PSIyMDAiIHk9IjE1MCIgZm9udC1mYW1pbHk9IkludGVyLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjI0IiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkNhcGl0YWwgQ29tcGFzczwvdGV4dD4KICA8dGV4dCB4PSIyMDAiIHk9IjE4MCIgZm9udC1mYW1pbHk9IkludGVyLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2IiBmaWxsPSJyZ2JhKDI1NSwyNTUsMjU1LDAuOCkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPlByb2Zlc3Npb25hbCBGaW5hbmNpYWwgTWFuYWdlbWVudDwvdGV4dD4KPC9zdmc+" class="login-image" alt="Capital Compass Platform">
        <h3 style="color: #4a5568; margin: 0;">Secure Financial Platform</h3>
        <p style="color: #718096; margin: 10px 0;">Access your personalized financial tools and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Right side with login form
    st.markdown('<div class="login-right">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown('<h2 class="login-title">Welcome Back</h2>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Sign in to access your financial dashboard</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if email and password:
                    success, message = authenticate_user(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_user = email
                        # Load user profile
                        profile = get_user_profile(email)
                        if profile:
                            st.session_state.user_profile = profile
                            st.session_state.profile_completed = True
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.markdown('<h2 class="login-title">Create Account</h2>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Join Capital Compass for personalized financial management</p>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            reg_email = st.text_input("Email Address", placeholder="Enter your email")
            reg_password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if full_name and reg_email and reg_password and confirm_password:
                    if reg_password == confirm_password:
                        success, message = register_user(reg_email, reg_password, full_name)
                        if success:
                            st.success("Registration successful! Please login with your credentials.")
                        else:
                            st.error(message)
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_profile_setup():
    """Display profile setup page"""
    users = load_users()
    user_data = users.get(st.session_state.current_user, {})
    
    st.markdown('<div class="profile-setup">', unsafe_allow_html=True)
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="welcome-header">
        <h2 style="margin: 0;">Welcome, {user_data.get('full_name', 'User')}!</h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">Let's set up your financial profile to provide personalized insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("profile_setup_form"):
        st.markdown('<h3 class="section-title">Personal Information</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            phone = st.text_input("Phone Number", placeholder="Enter your phone number")
            city = st.text_input("City", placeholder="Enter your city")
            
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
            occupation = st.text_input("Occupation", placeholder="Enter your occupation")
            state = st.text_input("State", placeholder="Enter your state")
        
        st.markdown('<h3 class="section-title">Employment & Income Information</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            employment_type = st.selectbox("Employment Type", 
                                         ["Salaried", "Self-employed", "Business Owner", "Retired", "Student"])
            income_range = st.selectbox("Annual Income Range",
                                      ["Below 3 Lakhs", "3-5 Lakhs", "5-10 Lakhs", "Above 10 Lakhs"])
            
        with col2:
            work_experience = st.slider("Work Experience (Years)", 0, 40, 5)
            monthly_salary = st.number_input("Monthly Salary (₹)", min_value=0, value=50000, step=5000)
        
        st.markdown('<h3 class="section-title">Credit & Financial Information</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            payment_history = st.slider("Payment History (%)", 0, 100, 90, 
                                       help="Percentage of payments made on time")
            credit_utilization = st.slider("Credit Utilization (%)", 0, 100, 30,
                                         help="Percentage of credit limit used")
            credit_history_years = st.slider("Credit History (Years)", 0, 25, 5,
                                           help="Age of your oldest credit account")
            credit_mix = st.slider("Credit Mix Score", 0, 100, 70,
                                 help="Diversity of credit types")
            
        with col2:
            recent_inquiries = st.slider("Recent Credit Inquiries", 0, 15, 1,
                                       help="Number of inquiries in last 12 months")
            total_accounts = st.number_input("Total Credit Accounts", min_value=0, max_value=20, value=3)
            outstanding_debt = st.slider("Outstanding Debt (%)", 0, 100, 25)
            total_credit_limit = st.number_input("Total Credit Limit (₹)", min_value=10000, 
                                               max_value=5000000, value=200000, step=10000)
        
        col1, col2 = st.columns(2)
        with col1:
            late_payments = st.number_input("Late Payments (Last 2 Years)", min_value=0, max_value=20, value=0)
            settled_accounts = st.number_input("Settled Accounts", min_value=0, max_value=10, value=0)
            
        with col2:
            monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=30000, step=1000)
            savings_goal = st.number_input("Monthly Savings Goal (₹)", min_value=0, value=10000, step=1000)
        
        submit_profile = st.form_submit_button("Save Profile & Continue", use_container_width=True)
        
        if submit_profile:
            profile_data = {
                'personal_info': {
                    'age': age,
                    'gender': gender,
                    'phone': phone,
                    'city': city,
                    'state': state,
                    'occupation': occupation
                },
                'employment_info': {
                    'employment_type': employment_type,
                    'income_range': income_range,
                    'work_experience': work_experience,
                    'monthly_salary': monthly_salary
                },
                'financial_info': {
                    'payment_history': payment_history,
                    'credit_utilization': credit_utilization,
                    'credit_history_years': credit_history_years,
                    'credit_mix': credit_mix,
                    'recent_inquiries': recent_inquiries,
                    'total_accounts': total_accounts,
                    'outstanding_debt': outstanding_debt,
                    'total_credit_limit': total_credit_limit,
                    'late_payments': late_payments,
                    'settled_accounts': settled_accounts,
                    'monthly_expenses': monthly_expenses,
                    'savings_goal': savings_goal
                },
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            save_user_profile(st.session_state.current_user, profile_data)
            st.session_state.user_profile = profile_data
            st.session_state.profile_completed = True
            
            st.success("Profile saved successfully! Redirecting to dashboard...")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Credit Score Calculation Functions (same as before)
def calculate_enhanced_cibil_score(payment_history, credit_utilization, credit_history_years, 
                                 credit_mix, recent_inquiries, total_accounts, outstanding_debt,
                                 total_credit_limit, income_range, employment_type, late_payments,
                                 settled_accounts):
    """Enhanced CIBIL score calculation with additional factors"""
    weights = {
        "payment_history": 0.35,
        "credit_utilization": 0.30,
        "credit_history": 0.15,
        "credit_mix": 0.10,
        "recent_inquiries": 0.10
    }
    
    ph_score = payment_history * weights["payment_history"]
    late_payment_penalty = min(late_payments * 5, 20)
    ph_score = max(0, ph_score - (late_payment_penalty * weights["payment_history"] / 100))
    
    settled_penalty = settled_accounts * 10
    ph_score = max(0, ph_score - (settled_penalty * weights["payment_history"] / 100))
    
    cu_score = (100 - credit_utilization) * weights["credit_utilization"]
    if credit_utilization < 10:
        cu_score *= 1.1
    elif credit_utilization > 70:
        cu_score *= 0.8
    
    ch_score = min(credit_history_years * 7, 100) * weights["credit_history"]
    if credit_history_years > 10:
        ch_score *= 1.1
    
    cm_score = credit_mix * weights["credit_mix"]
    if total_accounts < 3:
        cm_score *= 0.8
    elif total_accounts > 10:
        cm_score *= 0.9
    
    ri_score = max(100 - (recent_inquiries * 20), 0) * weights["recent_inquiries"]
    
    income_bonus = 0
    if employment_type == "Salaried" and income_range == "Above 10 Lakhs":
        income_bonus = 5
    elif employment_type == "Self-employed" and income_range == "Above 10 Lakhs":
        income_bonus = 3
    elif income_range in ["5-10 Lakhs", "3-5 Lakhs"]:
        income_bonus = 2
    
    debt_impact = 0
    if outstanding_debt > 80:
        debt_impact = -10
    elif outstanding_debt > 50:
        debt_impact = -5
    elif outstanding_debt < 20:
        debt_impact = 2
    
    total_percentage = ph_score + cu_score + ch_score + cm_score + ri_score + income_bonus + debt_impact
    final_score = int(300 + (total_percentage / 100) * 600)
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
        return "Excellent", "excellent", "★"
    elif score >= 700:
        return "Good", "good", "✓"
    elif score >= 650:
        return "Fair", "fair", "!"
    else:
        return "Poor", "poor", "✗"

def get_top_recommendations(score, credit_utilization, recent_inquiries, late_payments):
    """Get top 2 personalized recommendations"""
    recommendations = []
    
    if late_payments > 0:
        recommendations.append("Set up auto-pay for all bills to ensure 100% on-time payments")
    
    if credit_utilization > 30:
        recommendations.append(f"Reduce credit card usage to below 30% (currently {credit_utilization}%)")
    
    if recent_inquiries > 3:
        recommendations.append("Avoid applying for new credit for the next 6 months")
    
    if len(recommendations) == 0:
        if score < 750:
            recommendations.append("Maintain consistent payment history across all accounts")
            recommendations.append("Keep credit utilization below 10% for optimal score")
        else:
            recommendations.append("Excellent score! Monitor quarterly for any changes")
            recommendations.append("Consider becoming an authorized user on family accounts")
    
    return recommendations[:2]

def display_credit_score_dashboard():
    """Credit Score Dashboard Component"""
    if st.session_state.calculated_score is not None:
        score = st.session_state.calculated_score
        category = st.session_state.score_category
        recommendations = st.session_state.score_recommendations
        
        if score >= 750:
            emoji = "★"
        elif score >= 700:
            emoji = "✓"
        elif score >= 650:
            emoji = "!"
        else:
            emoji = "✗"
        
        dashboard_html = f"""
        <div class="credit-score-dashboard">
            <div class="dashboard-content">
                <div class="dashboard-title">Your Credit Score</div>
                <div class="dashboard-score">{score}</div>
                <div class="dashboard-category">{emoji} {category}</div>
                <div class="dashboard-recommendations">
                    <div class="recommendation-title">Quick Improvements:</div>
                    {"".join([f'<div class="recommendation-item">• {rec}</div>' for rec in recommendations[:2]])}
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
                Your credit score will appear here once calculated
            </div>
        </div>
        """
        st.markdown(placeholder_html, unsafe_allow_html=True)

def show_main_dashboard():
    """Display the main dashboard after login"""
    # User info bar
    users = load_users()
    user_data = users.get(st.session_state.current_user, {})
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="user-info-bar">
            <div>
                <strong>Welcome back, {user_data.get('full_name', 'User')}!</strong><br>
                <small>Last login: {user_data.get('last_login', 'N/A')}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("Logout", key="logout_btn"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("## 📊 Your Financial Dashboard")
    display_credit_score_dashboard()
    
    st.markdown("## 🔧 Financial Tools")
    
    # Auto-calculate credit score if profile exists
    if st.session_state.user_profile and st.session_state.calculated_score is None:
        profile = st.session_state.user_profile
        financial = profile['financial_info']
        employment = profile['employment_info']
        
        score, components = calculate_enhanced_cibil_score(
            financial['payment_history'], financial['credit_utilization'], 
            financial['credit_history_years'], financial['credit_mix'], 
            financial['recent_inquiries'], financial['total_accounts'], 
            financial['outstanding_debt'], financial['total_credit_limit'], 
            employment['income_range'], employment['employment_type'], 
            financial['late_payments'], financial['settled_accounts']
        )
        
        category, css_class, emoji = get_score_category(score)
        recommendations = get_top_recommendations(
            score, financial['credit_utilization'], 
            financial['recent_inquiries'], financial['late_payments']
        )
        
        st.session_state.calculated_score = score
        st.session_state.score_category = category
        st.session_state.score_recommendations = recommendations
    
    # Financial tools with pre-populated data
    tools = [
        {
            "name": "SIP Calculator",
            "desc": "Master Systematic Investment Planning with your profile data pre-loaded for personalized calculations.",
            "link": "https://financialreach.streamlit.app/"
        },
        {
            "name": "Credit Score Analyzer", 
            "desc": "Your credit score has been calculated using your profile. View detailed analysis and improvement strategies.",
            "link": "#"
        },
        {
            "name": "Tax Calculator",
            "desc": "Smart tax optimization based on your income profile and employment type for accurate calculations.",
            "link": "#"
        },
        {
            "name": "EMI Calculator",
            "desc": "Calculate EMIs with your income and financial profile for realistic loan planning.",
            "link": "#"
        },
        {
            "name": "Expense Tracker",
            "desc": "Track expenses against your saved monthly budget and savings goals.",
            "link": "#"
        },
        {
            "name": "Retirement Planner",
            "desc": "Plan your retirement with personalized calculations based on your age and salary profile.",
            "link": "#"
        }
    ]
    
    # Create tools grid
    col1, col2, col3 = st.columns(3)
    
    for i, tool in enumerate(tools):
        with [col1, col2, col3][i % 3]:
            with st.container():
                st.markdown(f"### {tool['name']}")
                st.write(tool['desc'])
                
                # Show relevant pre-populated data
                if st.session_state.user_profile:
                    if tool['name'] == "Credit Score Analyzer" and st.session_state.calculated_score:
                        st.success(f"Current Score: {st.session_state.calculated_score} ({st.session_state.score_category})")
                    elif tool['name'] == "SIP Calculator":
                        savings = st.session_state.user_profile['financial_info']['savings_goal']
                        st.info(f"Monthly Investment Capacity: ₹{savings:,}")
                    elif tool['name'] == "Tax Calculator":
                        salary = st.session_state.user_profile['employment_info']['monthly_salary']
                        st.info(f"Annual Salary: ₹{salary * 12:,}")
                    elif tool['name'] == "EMI Calculator":
                        income = st.session_state.user_profile['employment_info']['monthly_salary']
                        st.info(f"Monthly Income: ₹{income:,}")
                
                if st.button(f"Launch {tool['name']}", key=f"tool_{i}"):
                    st.success(f"Opening {tool['name']} with your pre-loaded profile data...")

# Main application logic
def main():
    if not st.session_state.authenticated:
        show_login_page()
    elif not st.session_state.profile_completed:
        show_profile_setup()
    else:
        show_main_dashboard()

if __name__ == "__main__":
    main()
