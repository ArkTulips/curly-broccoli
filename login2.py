
import streamlit as st
import requests
import time
from urllib.parse import urlencode
import base64
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="FinanceHub - Professional Financial Management Portal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    /* ... existing CSS ... */
    .stTextInput > div > div > input {
        padding: 16px 20px;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: white;
        color: black !important;  /* This makes input text black */
    }
    /* ... rest of your CSS ... */
    </style>
    """, unsafe_allow_html=True)

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {height: 0;}

    /* Global styles */
    .stApp {
        background: linear-gradient(135 deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
                                   )

    /* Main container */
    .main-container {
        display: flex;
        min-height: 100vh;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 20px;
    }

    /* Left panel */
    .left-panel {
        flex: 1;
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        color: white;
        padding: 60px 40px;
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
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }

    .brand-content {
        position: relative;
        z-index: 1;
    }

    .brand-title {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 16px;
        background: linear-gradient(45deg, #ffffff, #e8f4f8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .brand-subtitle {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 40px;
        line-height: 1.6;
    }

    .features-list {
        space: 20px;
    }

    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding: 15px 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }

    .feature-text {
        font-size: 16px;
        font-weight: 500;
    }

    /* Right panel */
    .right-panel {
        flex: 1;
        padding: 60px 40px;
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
        font-size: 32px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 8px;
    }

    .login-subtitle {
        font-size: 16px;
        color: #7f8c8d;
        line-height: 1.5;
    }

    /* Form styles */
    .stTextInput > div > div > input {
        padding: 16px 20px;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: white;
    }

    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }

    .stTextInput > label {
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 8px;
    }

    /* Button styles */
    .stButton > button {
        width: 100%;
        padding: 16px 24px;
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2980b9, #3498db);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(52, 152, 219, 0.3);
    }

    /* GitHub button */
    .github-btn {
        background: #24292e !important;
        color: white !important;
        margin-top: 12px;
    }

    .github-btn:hover {
        background: #1a1e22 !important;
    }

    /* Success/Error messages */
    .stAlert {
        border-radius: 8px;
        margin: 16px 0;
    }

    /* Loading spinner */
    .stSpinner {
        text-align: center;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-container {
            flex-direction: column;
            margin: 10px;
        }

        .left-panel, .right-panel {
            padding: 40px 20px;
        }

        .brand-title {
            font-size: 36px;
        }

        .login-title {
            font-size: 28px;
        }
    }

    /* Demo credentials box */
    .demo-box {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
    }

    .demo-title {
        font-weight: 600;
        color: #2e7d32;
        margin-bottom: 8px;
    }

    .demo-credentials {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #1b5e20;
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
    # Demo credentials
    demo_credentials = {
        'demo@financehub.com': 'demo123',
        'admin@financehub.com': 'admin123',
        'user@financehub.com': 'user123'
    }

    return demo_credentials.get(email) == password

def authenticate_user(email, password):
    """Authenticate user and set session state"""
    if validate_credentials(email, password):
        st.session_state.authenticated = True
        st.session_state.user_info = {
            'email': email,
            'name': email.split('@')[0].title(),
            'login_time': time.time()
        }
        return True
    return False

def github_auth():
    """Simulate GitHub OAuth authentication"""
    # In a real application, this would redirect to GitHub OAuth
    st.info("GitHub authentication would redirect to OAuth flow. For demo purposes, using demo login.")
    st.session_state.authenticated = True
    st.session_state.user_info = {
        'email': 'github@financehub.com',
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
                <h1 class="brand-title">FinanceHub</h1>
                <p class="brand-subtitle">Professional Financial Management Portal</p>
                <div class="features-list">
                    <div class="feature-item">
                        <span class="feature-text">Secure Authentication</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-text">Financial Dashboard Access</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-text">GitHub Integration</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-text">Professional Interface</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="right-panel">
            <div class="login-header">
                <h2 class="login-title">Welcome Back</h2>
                <p class="login-subtitle">Sign in to access your financial dashboard</p>
            </div>
    """, unsafe_allow_html=True)

    # Demo credentials info
    with st.expander("Demo Credentials", expanded=False):
        st.markdown("""
        <div class="demo-box">
            <div class="demo-title">Available Demo Accounts:</div>
            <div class="demo-credentials">
                • demo@financehub.com / demo123<br>
                • admin@financehub.com / admin123<br>
                • user@financehub.com / user123
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Login form
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember Me")
        with col2:
            forgot_password = st.form_submit_button("Forgot Password?")  # ✅ FIXED

        login_submitted = st.form_submit_button("Sign In", use_container_width=True)


        if login_submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
            elif not "@" in email or not "." in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            elif len(password) < 3:
                st.error("Password must be at least 3 characters long.")
            else:
                with st.spinner("Authenticating..."):
                    time.sleep(1)  # Simulate authentication delay

                    if authenticate_user(email, password):
                        st.success("Login successful! Redirecting to dashboard...")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.session_state.login_attempts += 1
                        if st.session_state.login_attempts >= 3:
                            st.error("Too many failed attempts. Please try again later.")
                        else:
                            st.error("Invalid email or password. Please try again.")

    # GitHub login
    st.markdown("---")
    if st.button("Continue with GitHub", use_container_width=True, type="secondary"):
        github_auth()
        st.success("GitHub authentication successful! Redirecting...")
        time.sleep(2)
        st.rerun()

    # Additional options
    st.markdown("""
    <div style="text-align: center; margin-top: 24px;">
        <p style="color: #7f8c8d;">Don't have an account? <a href="#" style="color: #3498db; text-decoration: none;">Sign up here</a></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# Success page with redirect
def render_success_page():
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="color: #27ae60; margin-bottom: 20px;">Login Successful!</h1>
        <p style="font-size: 18px; color: #7f8c8d; margin-bottom: 30px;">
            Welcome back, {}! Redirecting to your financial dashboard...
        </p>
    </div>
    """.format(st.session_state.user_info['name']), unsafe_allow_html=True)

    # Auto redirect after 3 seconds
    with st.spinner("Redirecting to https://menufin.streamlit.app/..."):
        time.sleep(3)

    # JavaScript redirect
    st.markdown("""
    <script>
        window.open('https://menufin.streamlit.app/', '_blank');
    </script>
    """, unsafe_allow_html=True)

    # Manual link as fallback
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <a href="https://menufin.streamlit.app/" target="_blank" 
           style="background: #3498db; color: white; padding: 12px 24px; 
                  border-radius: 6px; text-decoration: none; font-weight: 600;">
            Click here if not redirected automatically
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Logout option
    if st.button("Logout", type="secondary"):
        logout()
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
