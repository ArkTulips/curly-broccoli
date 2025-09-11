
import streamlit as st
import requests
import time
from urllib.parse import urlencode
import base64
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Capital Compass - Professional Financial Management Portal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
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

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    /* Main container */
    .main-container {
        display: flex;
        min-height: 100vh;
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        margin: 20px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Left panel */
    .left-panel {
        flex: 1.2;
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 50%, #5c6bc0 100%);
        color: white;
        padding: 60px 50px;
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
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="15" height="15" patternUnits="userSpaceOnUse"><path d="M 15 0 L 0 0 0 15" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.4;
    }

    .brand-content {
        position: relative;
        z-index: 1;
    }

    .brand-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(45deg, #ffffff, #e3f2fd);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 24px;
        font-size: 32px;
        font-weight: 700;
        color: #1a237e;
    }

    .brand-title {
        font-size: 52px;
        font-weight: 700;
        margin-bottom: 16px;
        background: linear-gradient(45deg, #ffffff, #e8eaf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }

    .brand-subtitle {
        font-size: 20px;
        opacity: 0.9;
        margin-bottom: 16px;
        line-height: 1.4;
        font-weight: 500;
    }

    .brand-tagline {
        font-size: 16px;
        opacity: 0.8;
        margin-bottom: 40px;
        font-style: italic;
        color: #e8eaf6;
    }

    .features-list {
        margin-top: 20px;
    }

    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding: 18px 24px;
        background: rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        border-left: 4px solid #64b5f6;
        backdrop-filter: blur(10px);
    }

    .feature-icon {
        width: 24px;
        height: 24px;
        background: #64b5f6;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;
        font-size: 12px;
        font-weight: bold;
        color: #1a237e;
    }

    .feature-text {
        font-size: 16px;
        font-weight: 500;
        line-height: 1.4;
    }

    /* Right panel */
    .right-panel {
        flex: 1;
        padding: 60px 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #fafbfc;
    }

    .login-header {
        text-align: center;
        margin-bottom: 40px;
    }

    .login-title {
        font-size: 36px;
        font-weight: 700;
        color: #1a237e;
        margin-bottom: 12px;
    }

    .login-subtitle {
        font-size: 18px;
        color: #5f6368;
        line-height: 1.5;
        margin-bottom: 8px;
    }

    .login-description {
        font-size: 14px;
        color: #80868b;
        line-height: 1.4;
    }

    /* Form styles */
    .stTextInput > div > div > input {
        padding: 18px 24px !important;
        border: 2px solid #e8eaed !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: white !important;
        color: black !important;
        font-weight: 500 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #1a237e !important;
        box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #9aa0a6 !important;
        font-weight: 400 !important;
    }

    .stTextInput > label {
        font-weight: 600 !important;
        color: #1a237e !important;
        margin-bottom: 8px !important;
        font-size: 14px !important;
    }

    /* Button styles */
    .stButton > button {
        width: 100% !important;
        padding: 18px 32px !important;
        background: linear-gradient(135deg, #1a237e, #3949ab) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        margin: 8px 0 !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #3949ab, #1a237e) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(26, 35, 126, 0.3) !important;
    }

    /* GitHub button */
    .github-btn {
        background: linear-gradient(135deg, #24292e, #40464f) !important;
        color: white !important;
    }

    .github-btn:hover {
        background: linear-gradient(135deg, #40464f, #24292e) !important;
    }

    /* Success/Error messages */
    .stAlert {
        border-radius: 12px !important;
        margin: 16px 0 !important;
        padding: 16px 20px !important;
    }

    /* Loading spinner */
    .stSpinner {
        text-align: center;
    }

    /* Checkbox styles */
    .stCheckbox {
        margin: 16px 0 !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-container {
            flex-direction: column;
            margin: 10px;
        }

        .left-panel, .right-panel {
            padding: 40px 30px;
        }

        .brand-title {
            font-size: 40px;
        }

        .login-title {
            font-size: 28px;
        }
    }

    /* Demo credentials box */
    .demo-box {
        background: linear-gradient(135deg, #e8f5e8, #f1f8e9);
        border: 2px solid #4caf50;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }

    .demo-title {
        font-weight: 700;
        color: #1b5e20;
        margin-bottom: 12px;
        font-size: 16px;
    }

    .demo-credentials {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
        font-size: 14px;
        color: #2e7d32;
        line-height: 1.6;
    }

    /* Success page styles */
    .success-container {
        text-align: center;
        padding: 80px 40px;
        background: linear-gradient(135deg, #e8f5e8, #f1f8e9);
        border-radius: 20px;
        margin: 40px;
    }

    .success-icon {
        width: 80px;
        height: 80px;
        background: #4caf50;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px;
        font-size: 32px;
        color: white;
    }

    .redirect-link {
        display: inline-block;
        background: linear-gradient(135deg, #1a237e, #3949ab);
        color: white;
        padding: 16px 32px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 24px;
        transition: all 0.3s ease;
    }

    .redirect-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(26, 35, 126, 0.3);
        text-decoration: none;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0

# Authentication functions
def validate_credentials(email, password):
    """Validate user credentials"""
    # Demo credentials for Capital Compass
    demo_credentials = {
        'admin@capitalcompass.com': 'compass123',
        'demo@capitalcompass.com': 'demo123',
        'user@capitalcompass.com': 'user123',
        'finance@capitalcompass.com': 'finance123'
    }

    return demo_credentials.get(email) == password

def authenticate_user(email, password):
    """Authenticate user and set session state"""
    if validate_credentials(email, password):
        st.session_state.authenticated = True
        st.session_state.user_info = {
            'email': email,
            'name': email.split('@')[0].title().replace('_', ' ').replace('.', ' '),
            'login_time': time.time()
        }
        return True
    return False

def github_auth():
    """Simulate GitHub OAuth authentication"""
    st.info("Redirecting to GitHub OAuth... For demo purposes, automatically logging in.")
    time.sleep(1)
    st.session_state.authenticated = True
    st.session_state.user_info = {
        'email': 'github.user@capitalcompass.com',
        'name': 'GitHub User',
        'login_time': time.time(),
        'provider': 'github'
    }

def logout():
    """Clear session state and logout user"""
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.login_attempts = 0

# Main login interface
def render_login_page():
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
                        <div class="feature-icon">⚡</div>
                        <span class="feature-text">Lightning Fast Calculations</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">📱</div>
                        <span class="feature-text">Mobile-First Design</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🔒</div>
                        <span class="feature-text">Bank-Grade Security</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">📊</div>
                        <span class="feature-text">Real-time Analytics</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🎯</div>
                        <span class="feature-text">Personalized Insights</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="right-panel">
            <div class="login-header">
                <h2 class="login-title">Welcome Back</h2>
                <p class="login-subtitle">Access Your Financial Dashboard</p>
                <p class="login-description">Sign in to continue to Capital Compass and manage your financial tools</p>
            </div>
    """, unsafe_allow_html=True)

    # Demo credentials info
    with st.expander("🔑 Demo Credentials", expanded=False):
        st.markdown("""
        <div class="demo-box">
            <div class="demo-title">Available Demo Accounts:</div>
            <div class="demo-credentials">
                • admin@capitalcompass.com / compass123<br>
                • demo@capitalcompass.com / demo123<br>
                • user@capitalcompass.com / user123<br>
                • finance@capitalcompass.com / finance123
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Login form
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email Address", placeholder="Enter your email address", key="email_input")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="password_input")

        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember Me")
        with col2:
            if st.form_submit_button("Forgot Password?", type="secondary"):
                st.info("Password reset functionality would be implemented here.")

        login_submitted = st.form_submit_button("Sign In to Capital Compass", use_container_width=True, type="primary")

        if login_submitted:
            if not email or not password:
                st.error("⚠️ Please enter both email and password.")
            elif not "@" in email or not "." in email.split("@")[-1]:
                st.error("⚠️ Please enter a valid email address.")
            elif len(password) < 3:
                st.error("⚠️ Password must be at least 3 characters long.")
            else:
                with st.spinner("🔐 Authenticating your credentials..."):
                    time.sleep(1.5)  # Simulate authentication delay

                    if authenticate_user(email, password):
                        st.success("✅ Login successful! Redirecting to your dashboard...")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.session_state.login_attempts += 1
                        if st.session_state.login_attempts >= 5:
                            st.error("🚫 Too many failed attempts. Account temporarily locked.")
                        else:
                            remaining_attempts = 5 - st.session_state.login_attempts
                            st.error(f"❌ Invalid credentials. {remaining_attempts} attempts remaining.")

    # Divider
    st.markdown("---")

    # GitHub login
    github_col1, github_col2, github_col3 = st.columns([1, 2, 1])
    with github_col2:
        if st.button("🐙 Continue with GitHub", use_container_width=True, type="secondary"):
            with st.spinner("🔄 Connecting to GitHub..."):
                github_auth()
                st.success("✅ GitHub authentication successful!")
                time.sleep(1.5)
                st.rerun()

    # Additional options
    st.markdown("""
    <div style="text-align: center; margin-top: 32px;">
        <p style="color: #5f6368; font-size: 14px;">
            New to Capital Compass? 
            <a href="#" style="color: #1a237e; text-decoration: none; font-weight: 600;">
                Create an account
            </a>
        </p>
        <p style="color: #80868b; font-size: 12px; margin-top: 16px;">
            By signing in, you agree to our Terms of Service and Privacy Policy
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# Success page with redirect
def render_success_page():
    user_name = st.session_state.user_info.get('name', 'User')
    provider = st.session_state.user_info.get('provider', 'email')

    st.markdown("""
    <div class="success-container">
        <div class="success-icon">✓</div>
        <h1 style="color: #1b5e20; margin-bottom: 16px; font-size: 36px; font-weight: 700;">Login Successful!</h1>
        <p style="font-size: 20px; color: #2e7d32; margin-bottom: 24px; font-weight: 500;">
            Welcome back, {}! 🎉
        </p>
        <p style="font-size: 16px; color: #4caf50; margin-bottom: 32px;">
            You have successfully signed in via {}. Redirecting to your Capital Compass dashboard...
        </p>
    </div>
    """.format(user_name, provider.title()), unsafe_allow_html=True)

    # Auto redirect countdown
    placeholder = st.empty()
    for i in range(5, 0, -1):
        with placeholder.container():
            st.info(f"🚀 Redirecting to Capital Compass in {i} seconds...")
            time.sleep(1)

    placeholder.empty()

    # Manual redirect link
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <a href="https://menufin.streamlit.app/" target="_blank" class="redirect-link">
            🧭 Open Capital Compass Dashboard
        </a>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript redirect as fallback
    st.markdown("""
    <script>
        setTimeout(function() {
            window.open('https://menufin.streamlit.app/', '_blank');
        }, 1000);
    </script>
    """, unsafe_allow_html=True)

    # Session info and logout
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()
            st.success("👋 Logged out successfully!")
            time.sleep(1)
            st.rerun()

# Main application
def main():
    load_custom_css()
    init_session_state()

    if st.session_state.authenticated:
        render_success_page()
    else:
        render_login_page()

if __name__ == "__main__":
    main()
