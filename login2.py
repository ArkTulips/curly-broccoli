
import streamlit as st
import json
import time
import hashlib
import os
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Capital Compass - Professional Financial Management Portal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# File paths for data storage
USERS_FILE = "users_data.json"
USER_PROFILES_FILE = "user_profiles.json"

# Custom CSS for humanized styling with natural images and white color scheme
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {height: 0;}

    /* Global styles with natural dark background */
    .stApp {
        background: #2c3e50;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    /* Main container with slightly imperfect rounded corners */
    .main-container {
        display: flex;
        min-height: 100vh;
        background: #34495e;
        border-radius: 18px 25px 20px 22px;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0,0,0,0.4), 0 8px 20px rgba(0,0,0,0.2);
        margin: 15px 25px 20px 18px;
        max-width: 1380px;
        margin-left: auto;
        margin-right: auto;
        border: 2px solid rgba(255, 255, 255, 0.1);
        transform: rotate(-0.2deg);
    }

    /* Left panel with natural business meeting image */
    .left-panel {
        flex: 1.1;
        background: #2c3e50;
        color: white;
        padding: 55px 45px 60px 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }

    .left-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url('https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=85');
        background-size: cover;
        background-position: center 30%;
        opacity: 0.12;
        z-index: 0;
        transform: scale(1.05);
    }

    .left-panel::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="0.5" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23dots)"/></svg>');
        opacity: 0.3;
        z-index: 1;
    }

    .brand-content {
        position: relative;
        z-index: 2;
    }

    .brand-logo {
        width: 95px;
        height: 98px;
        background: #ffffff;
        border-radius: 16px 20px 18px 19px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 28px;
        font-size: 34px;
        font-weight: 700;
        color: #2c3e50;
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
        transform: rotate(1deg);
    }

    .brand-title {
        font-size: 54px;
        font-weight: 700;
        margin-bottom: 18px;
        color: #ffffff;
        line-height: 1.05;
        text-shadow: 0 0 25px rgba(255, 255, 255, 0.3);
        letter-spacing: -1px;
    }

    .brand-subtitle {
        font-size: 21px;
        opacity: 0.88;
        margin-bottom: 18px;
        line-height: 1.35;
        font-weight: 500;
        color: #ecf0f1;
    }

    .brand-tagline {
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 45px;
        font-style: italic;
        color: #bdc3c7;
        font-weight: 300;
        line-height: 1.4;
    }

    .features-list {
        margin-top: 22px;
    }

    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 22px;
        padding: 20px 25px 21px 26px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px 15px 13px 14px;
        border-left: 4px solid #00d4ff;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        transform: rotate(-0.1deg);
    }

    .feature-item:nth-child(even) {
        transform: rotate(0.1deg);
        margin-left: 5px;
    }

    .feature-item:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateX(3px) rotate(0deg);
    }

    .feature-icon {
        width: 30px;
        height: 30px;
        background: #ffffff;
        border-radius: 6px 8px 7px 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 18px;
        font-size: 13px;
        font-weight: bold;
        color: #2c3e50;
        box-shadow: 0 3px 12px rgba(255, 255, 255, 0.25);
    }

    .feature-text {
        font-size: 17px;
        font-weight: 500;
        line-height: 1.3;
        color: #ecf0f1;
    }

    /* Right panel with natural workspace image */
    .right-panel {
        flex: 1;
        padding: 55px 45px 60px 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #34495e;
        position: relative;
    }

    .right-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=85');
        background-size: cover;
        background-position: center;
        opacity: 0.08;
        z-index: 0;
        transform: scale(1.02);
    }

    .right-panel-content {
        position: relative;
        z-index: 1;
    }

    /* Natural business meeting image container */
    .dashboard-image {
        width: 100%;
        max-width: 390px;
        height: 240px;
        background-image: url('https://png.pngtree.com/png-clipart/20200226/original/pngtree-financial-consulting-logo-vector-template-png-image_5314396.jpg');
        background-size: cover;
        background-position: center 35%;
        border-radius: 12px 18px 15px 16px;
        margin-bottom: 28px;
        box-shadow: 0 12px 30px rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: rotate(0.3deg);
    }

    /* Form styles with natural, slightly imperfect styling */
    .stTextInput > div > div > input {
        padding: 18px 24px 19px 25px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px 14px 12px 13px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: rgba(52, 73, 94, 0.8) !important;
        color: white !important;
        font-weight: 500 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.15) !important;
        outline: none !important;
        background: rgba(44, 62, 80, 0.9) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #bdc3c7 !important;
        font-weight: 400 !important;
    }

    .stTextInput > label {
        font-weight: 600 !important;
        color: #ecf0f1 !important;
        margin-bottom: 8px !important;
        font-size: 14px !important;
    }

    .stSelectbox > div > div > div {
        background: rgba(52, 73, 94, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px 14px 12px 13px !important;
        color: white !important;
    }

    .stNumberInput > div > div > input {
        padding: 18px 24px 19px 25px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px 14px 12px 13px !important;
        font-size: 16px !important;
        background: rgba(52, 73, 94, 0.8) !important;
        color: white !important;
        font-weight: 500 !important;
    }

    /* Button styles with organic feel */
    .stButton > button {
        width: 100% !important;
        padding: 18px 32px 19px 34px !important;
        background: #ffffff !important;
        color: #2c3e50 !important;
        border: none !important;
        border-radius: 11px 16px 13px 14px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        margin: 8px 0 10px 0 !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25) !important;
    }

    .stButton > button:hover {
        background: #ecf0f1 !important;
        transform: translateY(-2px) rotate(-0.1deg) !important;
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.35) !important;
    }

    /* Create Account Button - More Visible with natural styling */
    .create-account-btn {
        background: #3498db !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        padding: 20px 34px 21px 36px !important;
        margin: 15px 0 17px 0 !important;
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.35) !important;
    }

    .create-account-btn:hover {
        background: #2980b9 !important;
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.45) !important;
    }

   

    /* Success/Error messages with natural styling */
    .stAlert {
        border-radius: 8px 12px 10px 11px !important;
        margin: 15px 0 17px 0 !important;
        padding: 16px 20px 17px 21px !important;
        background: rgba(44, 62, 80, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }

    /* Onboarding styles with organic feel */
    .onboarding-container {
        background: #2c3e50;
        border-radius: 18px 25px 20px 22px;
        padding: 45px 50px 48px 52px;
        margin: 20px 25px 22px 23px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        transform: rotate(-0.1deg);
    }

    .onboarding-title {
        color: #ffffff;
        font-size: 34px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 18px;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }

    .onboarding-subtitle {
        color: #ecf0f1;
        font-size: 19px;
        text-align: center;
        margin-bottom: 45px;
        line-height: 1.4;
    }

    .section-header {
        color: #ffffff;
        font-size: 24px;
        font-weight: 600;
        margin: 35px 0 18px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-container {
            flex-direction: column;
            margin: 10px 15px;
            transform: rotate(0deg);
        }

        .left-panel, .right-panel {
            padding: 35px 25px;
        }

        .brand-title {
            font-size: 40px;
        }

        .dashboard-image {
            height: 180px;
            transform: rotate(0deg);
        }
    }

    /* Signup prompt with natural styling */
    .signup-prompt {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 14px 20px 16px 18px;
        padding: 25px 28px 26px 30px;
        margin: 25px 0 27px 0;
        text-align: center;
        backdrop-filter: blur(10px);
        transform: rotate(-0.1deg);
    }

    .signup-prompt h3 {
        color: #ffffff;
        margin-bottom: 12px;
        font-size: 20px;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }

    .signup-prompt p {
        color: #bdc3c7;
        margin-bottom: 18px;
        font-size: 16px;
        line-height: 1.35;
    }

    /* Stats display with human touch */
    .stats-container {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 10px 15px 12px 13px;
        padding: 18px 20px 19px 22px;
        margin: 18px 0 20px 0;
        text-align: center;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .stats-container:nth-child(even) {
        transform: rotate(0.1deg);
    }

    .stats-container:nth-child(odd) {
        transform: rotate(-0.1deg);
    }

    .stat-number {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    .stat-label {
        font-size: 14px;
        color: #bdc3c7;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Checkbox styles */
    .stCheckbox {
        color: #ecf0f1 !important;
    }

    .stCheckbox > div {
        color: #ecf0f1 !important;
    }

    /* Form section headers */
    .stSubheader {
        color: #ffffff !important;
        font-weight: 600 !important;
        margin-bottom: 18px !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2) !important;
        padding-bottom: 8px !important;
    }

    /* Multiselect styling */
    .stMultiSelect > div > div {
        background: rgba(52, 73, 94, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px 14px 12px 13px !important;
        color: white !important;
    }

    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: rgba(52, 73, 94, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px 14px 12px 13px !important;
        color: white !important;
        padding: 14px 18px 15px 19px !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Data management functions
def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return {}

def save_users(users_data):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving users: {e}")
        return False

def load_user_profiles():
    """Load user profiles from JSON file"""
    try:
        if os.path.exists(USER_PROFILES_FILE):
            with open(USER_PROFILES_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Error loading user profiles: {e}")
        return {}

def save_user_profiles(profiles_data):
    """Save user profiles to JSON file"""
    try:
        with open(USER_PROFILES_FILE, 'w') as f:
            json.dump(profiles_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving user profiles: {e}")
        return False

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_account(email, password, full_name, phone):
    """Create a new user account"""
    users = load_users()

    if email in users:
        return False, "Account already exists with this email address"

    users[email] = {
        'password_hash': hash_password(password),
        'full_name': full_name,
        'phone': phone,
        'created_date': datetime.now().isoformat(),
        'last_login': None,
        'first_login': True
    }

    if save_users(users):
        return True, "Account created successfully"
    else:
        return False, "Error creating account"

# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    if 'first_login' not in st.session_state:
        st.session_state.first_login = False

# Authentication functions
def validate_credentials(email, password):
    """Validate user credentials - ONLY registered users"""
    users = load_users()
    if email in users:
        stored_hash = users[email]['password_hash']
        if hash_password(password) == stored_hash:
            first_login = users[email].get('first_login', False)

            # Update last login and first login status
            users[email]['last_login'] = datetime.now().isoformat()
            if first_login:
                users[email]['first_login'] = False
            save_users(users)

            return True, first_login

    return False, False

def authenticate_user(email, password):
    """Authenticate user and set session state"""
    is_valid, first_login = validate_credentials(email, password)

    if is_valid:
        users = load_users()
        user_data = users.get(email, {})

        st.session_state.authenticated = True
        st.session_state.first_login = first_login
        st.session_state.user_info = {
            'email': email,
            'name': user_data.get('full_name', email.split('@')[0].title()),
            'phone': user_data.get('phone', ''),
            'login_time': time.time(),
            'first_login': first_login
        }
        return True
    return False

# Signup form
def render_signup_form():
    st.markdown("""
    <div class="main-container">
        <div class="left-panel">
            <div class="brand-content">
                <div class="brand-logo">CC</div>
                <h1 class="brand-title">Join Capital Compass</h1>
                <p class="brand-subtitle">Start Your Financial Journey</p>
                <p class="brand-tagline">"Your Gateway to Smart Financial Management"</p>
                <div class="features-list">
                    <div class="feature-item">
                        <div class="feature-icon">A</div>
                        <span class="feature-text">Advanced Financial Calculators</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">P</div>
                        <span class="feature-text">Personalized Investment Planning</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">M</div>
                        <span class="feature-text">Real-time Market Analysis</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">I</div>
                        <span class="feature-text">Smart Financial Insights</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="right-panel">
            <div class="right-panel-content">
                <div class="dashboard-image"></div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        st.subheader("Personal Information")

        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Enter your first name")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Enter your last name")

        email = st.text_input("Email Address", placeholder="Enter your email address")
        phone = st.text_input("Phone Number", placeholder="Enter your phone number")

        st.subheader("Account Security")
        password = st.text_input("Password", type="password", placeholder="Create a secure password (min 8 characters)")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")

        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")

        signup_submitted = st.form_submit_button("Create My Capital Compass Account", use_container_width=True)

        if signup_submitted:
            full_name = f"{first_name} {last_name}".strip()

            # Validation
            if not all([first_name, last_name, email, phone, password, confirm_password]):
                st.error("Please fill in all required fields")
            elif not "@" in email or not "." in email.split("@")[-1]:
                st.error("Please enter a valid email address")
            elif len(phone) < 10:
                st.error("Please enter a valid phone number")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not agree_terms:
                st.error("Please agree to the Terms of Service and Privacy Policy")
            else:
                with st.spinner("Creating your Capital Compass account..."):
                    time.sleep(2)
                    success, message = create_user_account(email, password, full_name, phone)
                    if success:
                        st.success(f"{message}! Welcome to Capital Compass!")
                        time.sleep(3)
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error(f"{message}")

    if st.button("Already have an account? Sign In", use_container_width=True, type="secondary"):
        st.session_state.show_signup = False
        st.rerun()

    st.markdown("</div></div></div>", unsafe_allow_html=True)

# Onboarding form for new users
def render_onboarding():
    st.markdown("""
    <div class="onboarding-container">
        <h1 class="onboarding-title">Welcome to Capital Compass!</h1>
        <p class="onboarding-subtitle">Let's set up your financial profile to provide personalized insights and recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("onboarding_form"):
        # Personal Finance Information
        st.markdown('<h2 class="section-header">Personal Finance Profile</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            monthly_income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=5000)
            current_savings = st.number_input("Current Savings (₹)", min_value=0, value=100000, step=10000)

        with col2:
            occupation = st.selectbox("Occupation", [
                "Salaried Employee", "Business Owner", "Freelancer", 
                "Student", "Retired", "Other"
            ])
            risk_tolerance = st.selectbox("Investment Risk Tolerance", [
                "Conservative", "Moderate", "Aggressive"
            ])
            financial_goal = st.selectbox("Primary Financial Goal", [
                "Wealth Building", "Retirement Planning", "Tax Saving",
                "Emergency Fund", "Home Purchase", "Education Fund"
            ])

        # Investment Information
        st.markdown('<h2 class="section-header">Investment & SIP Details</h2>', unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            current_sip = st.number_input("Current Monthly SIP Amount (₹)", min_value=0, value=5000, step=500)
            investment_experience = st.selectbox("Investment Experience", [
                "Beginner (0-2 years)", "Intermediate (2-5 years)", 
                "Advanced (5+ years)", "Expert (10+ years)"
            ])

        with col4:
            preferred_investment = st.multiselect("Preferred Investment Types", [
                "Mutual Funds", "Stocks", "Fixed Deposits", "PPF", 
                "ELSS", "Gold", "Real Estate", "Crypto"
            ])

        # Loan & Credit Information
        st.markdown('<h2 class="section-header">Loans & Credit Profile</h2>', unsafe_allow_html=True)

        col5, col6 = st.columns(2)
        with col5:
            home_loan = st.number_input("Outstanding Home Loan (₹)", min_value=0, value=0, step=50000)
            other_loans = st.number_input("Other Loans/EMI per month (₹)", min_value=0, value=0, step=1000)

        with col6:
            credit_cards = st.number_input("Number of Credit Cards", min_value=0, max_value=10, value=1)
            estimated_credit_score = st.selectbox("Estimated Credit Score Range", [
                "Below 600 (Poor)", "600-650 (Fair)", "650-750 (Good)", 
                "750-800 (Very Good)", "Above 800 (Excellent)", "Don't Know"
            ])

        # Expense Tracking
        st.markdown('<h2 class="section-header">Monthly Expenses</h2>', unsafe_allow_html=True)

        col7, col8 = st.columns(2)
        with col7:
            rent_mortgage = st.number_input("Rent/Mortgage (₹)", min_value=0, value=15000, step=1000)
            utilities = st.number_input("Utilities & Bills (₹)", min_value=0, value=5000, step=500)
            food_dining = st.number_input("Food & Dining (₹)", min_value=0, value=8000, step=500)

        with col8:
            transportation = st.number_input("Transportation (₹)", min_value=0, value=3000, step=500)
            entertainment = st.number_input("Entertainment & Lifestyle (₹)", min_value=0, value=5000, step=500)
            healthcare = st.number_input("Healthcare (₹)", min_value=0, value=2000, step=500)

        # Retirement Planning
        st.markdown('<h2 class="section-header">Retirement & Tax Planning</h2>', unsafe_allow_html=True)

        col9, col10 = st.columns(2)
        with col9:
            retirement_age = st.number_input("Planned Retirement Age", min_value=45, max_value=75, value=60)
            retirement_corpus = st.number_input("Target Retirement Corpus (₹ in Lakhs)", min_value=0, value=100, step=10)

        with col10:
            tax_bracket = st.selectbox("Current Tax Bracket", [
                "0% (Income < 2.5L)", "5% (2.5L - 5L)", "20% (5L - 10L)", 
                "30% (Above 10L)", "New Tax Regime", "Not Sure"
            ])
            annual_tax_saving = st.number_input("Annual Tax Saving Investment (₹)", min_value=0, value=50000, step=10000)

        # Stock Market Interest
        st.markdown('<h2 class="section-header">Stock Market Preferences</h2>', unsafe_allow_html=True)

        favorite_stocks = st.text_area("Favorite Stocks to Track (comma separated)", 
                                     placeholder="e.g., RELIANCE, TCS, INFY, HDFC")

        stock_investment_budget = st.number_input("Monthly Stock Investment Budget (₹)", min_value=0, value=10000, step=1000)

        # Submit onboarding
        if st.form_submit_button("Complete Setup & Continue to Dashboard", use_container_width=True):
            # Save user profile data
            user_profile = {
                'personal_info': {
                    'age': age,
                    'occupation': occupation,
                    'monthly_income': monthly_income,
                    'current_savings': current_savings,
                    'risk_tolerance': risk_tolerance,
                    'financial_goal': financial_goal
                },
                'investments': {
                    'current_sip': current_sip,
                    'experience': investment_experience,
                    'preferred_types': preferred_investment
                },
                'credit_loans': {
                    'home_loan': home_loan,
                    'other_loans': other_loans,
                    'credit_cards': credit_cards,
                    'credit_score_range': estimated_credit_score
                },
                'expenses': {
                    'rent_mortgage': rent_mortgage,
                    'utilities': utilities,
                    'food_dining': food_dining,
                    'transportation': transportation,
                    'entertainment': entertainment,
                    'healthcare': healthcare
                },
                'retirement_tax': {
                    'retirement_age': retirement_age,
                    'retirement_corpus': retirement_corpus,
                    'tax_bracket': tax_bracket,
                    'annual_tax_saving': annual_tax_saving
                },
                'stock_market': {
                    'favorite_stocks': favorite_stocks,
                    'investment_budget': stock_investment_budget
                },
                'created_date': datetime.now().isoformat(),
                'profile_completed': True
            }

            # Save to file
            profiles = load_user_profiles()
            profiles[st.session_state.user_info['email']] = user_profile

            if save_user_profiles(profiles):
                st.success("Profile setup complete! Welcome to Capital Compass!")
                st.session_state.onboarding_complete = True
                time.sleep(3)
                st.rerun()
            else:
                st.error("Error saving profile. Please try again.")

# Main login interface
def render_login_page():
    # Get user statistics
    users = load_users()
    user_count = len(users)
    profiles = load_user_profiles()
    profile_count = len(profiles)

    st.markdown("""
    <div class="main-container">
        <div class="left-panel">
            <div class="brand-content">
                <div class="brand-logo">CC</div>
                <h1 class="brand-title">Capital Compass</h1>
                <p class="brand-subtitle">Professional Financial Management</p>
                <p class="brand-tagline">"Where Smart Money Decisions Begin"</p>
                <div class="features-list">
                    <div class="feature-item">
                        <div class="feature-icon">L</div>
                        <span class="feature-text">Lightning Fast Calculations</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">M</div>
                        <span class="feature-text">Mobile-First Design</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">S</div>
                        <span class="feature-text">Bank-Grade Security</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">R</div>
                        <span class="feature-text">Real-time Analytics</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="right-panel">
            <div class="right-panel-content">
                <div class="dashboard-image"></div>
    """, unsafe_allow_html=True)

    # Show user statistics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-number">{user_count}</div>
            <div class="stat-label">Registered Users</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-number">{profile_count}</div>
            <div class="stat-label">Complete Profiles</div>
        </div>
        """, unsafe_allow_html=True)

    # Prominent Create Account Section
    st.markdown("""
    <div class="signup-prompt">
        <h3>New to Capital Compass?</h3>
        <p>Join professionals who trust us with their financial planning!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Create Your Free Account Now!", use_container_width=True, key="create_account_main"):
        st.session_state.show_signup = True
        st.rerun()

    st.markdown("---")

    # Login form
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email Address", placeholder="Enter your registered email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember Me")
       

        login_submitted = st.form_submit_button("Sign In to Capital Compass", use_container_width=True, type="primary")

        if login_submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
            elif not "@" in email or not "." in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            elif len(password) < 3:
                st.error("Password must be at least 3 characters long.")
            else:
                with st.spinner("Authenticating your credentials..."):
                    time.sleep(1.5)

                    if authenticate_user(email, password):
                        st.success("Login successful! Welcome back!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.session_state.login_attempts += 1
                        if st.session_state.login_attempts >= 5:
                            st.error("Too many failed attempts. Please try creating an account or contact support.")
                        else:
                            remaining = 5 - st.session_state.login_attempts
                            st.error(f"Invalid credentials. {remaining} attempts remaining.")
                            st.info("Don't have an account? Create one using the button above!")

    
# Success page with redirect
def render_success_page():
    user_name = st.session_state.user_info.get('name', 'User')

    st.markdown(f"""
    <div style="text-align: center; padding: 50px 20px 52px 22px; background: #2c3e50; 
         border-radius: 15px 20px 17px 18px; margin: 18px 22px 20px 25px; border: 2px solid rgba(255, 255, 255, 0.2);">
        <h1 style="color: #ffffff; margin-bottom: 18px; font-size: 34px; text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);">
            Welcome, {user_name}!</h1>
        <p style="font-size: 17px; color: #ecf0f1; margin-bottom: 28px;">
            Successfully logged into Capital Compass
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Auto redirect
    with st.spinner("Redirecting to your Capital Compass dashboard..."):
        time.sleep(3)

    # Redirect link
    st.markdown("""
    <div style="text-align: center; margin: 35px 0 38px 0;">
        <a href="https://menufin.streamlit.app/" target="_blank" 
           style="background: #ffffff; color: #2c3e50; 
                  padding: 14px 28px 16px 30px; border-radius: 12px 16px 14px 15px; text-decoration: none; 
                  font-weight: 600; font-size: 17px; box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25);">
            Open Capital Compass Dashboard
        </a>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript redirect
    st.markdown("""
    <script>
        setTimeout(function() {
            window.open('https://menufin.streamlit.app/', '_blank');
        }, 1000);
    </script>
    """, unsafe_allow_html=True)

    # Logout button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Logout", type="secondary", use_container_width=True):
            # Reset all session states
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()

# Main application
def main():
    load_custom_css()
    init_session_state()

    if not st.session_state.authenticated:
        if st.session_state.show_signup:
            render_signup_form()
        else:
            render_login_page()
    else:
        # Check if first login and onboarding needed
        if st.session_state.first_login and not st.session_state.onboarding_complete:
            render_onboarding()
        else:
            render_success_page()

if __name__ == "__main__":
    main()
