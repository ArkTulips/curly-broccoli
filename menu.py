
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="FinanceHub - Your Ultimate Financial Companion", 
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
    # Dark theme CSS
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

        /* Animated background overlay */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(118, 75, 162, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 40% 80%, rgba(74, 144, 226, 0.10) 0%, transparent 30%);
            animation: backgroundFloat 12s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes backgroundFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 1; }
            33% { transform: translateY(-15px) rotate(1deg); opacity: 0.8; }
            66% { transform: translateY(-30px) rotate(-1deg); opacity: 0.9; }
        }

        /* Creative title styling */
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
            animation: gradientShift 4s ease-in-out infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
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

        /* Logo styling */
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 25px;
            position: relative;
            z-index: 1;
        }

        .logo {
            width: 120px;
            height: 120px;
            background: rgba(40, 44, 52, 0.9);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(15px);
            border: 3px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
            font-size: 3.5rem;
            animation: logoFloat 4s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }

        .logo::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: logoShine 3s linear infinite;
        }

        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) scale(1) rotate(0deg); }
            50% { transform: translateY(-15px) scale(1.05) rotate(2deg); }
        }

        @keyframes logoShine {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }

        /* Enhanced tool cards - dark theme */
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
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            min-height: 350px;
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
            height: 5px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 100%;
            animation: borderShift 4s ease infinite;
        }

        .tool-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 0;
        }

        @keyframes borderShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .tool-card:hover {
            transform: translateY(-20px) scale(1.03);
            box-shadow: 0 25px 70px rgba(102, 126, 234, 0.5);
            background: rgba(50, 54, 62, 1);
            border-color: rgba(102, 126, 234, 0.3);
        }

        .tool-card:hover::after {
            opacity: 1;
        }

        .tool-icon {
            font-size: 5rem;
            margin-bottom: 25px;
            filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.4));
            transition: all 0.4s ease;
            position: relative;
            z-index: 1;
        }

        .tool-card:hover .tool-icon {
            transform: scale(1.15) rotate(8deg);
            filter: drop-shadow(0 15px 30px rgba(102, 126, 234, 0.6));
        }

        .tool-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 18px;
            line-height: 1.3;
            position: relative;
            z-index: 1;
        }

        .tool-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 1.05rem;
            color: #c1c7d0;
            line-height: 1.7;
            margin-bottom: 30px;
            flex-grow: 1;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }

        .tool-button {
            display: inline-block;
            padding: 18px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
            position: relative;
            z-index: 1;
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
            transition: left 0.5s ease;
        }

        .tool-button:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 45px rgba(102, 126, 234, 0.7);
            text-decoration: none;
            color: white;
        }

        .tool-button:hover::before {
            left: 100%;
        }

        /* Enhanced info sections */
        .features-section {
            background: rgba(40, 44, 52, 0.85);
            backdrop-filter: blur(25px);
            border-radius: 25px;
            padding: 40px;
            margin: 50px auto;
            max-width: 1000px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            position: relative;
            z-index: 1;
        }

        .features-title {
            font-family: 'Poppins', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            text-align: center;
            color: #ffffff;
            margin-bottom: 30px;
        }

        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .feature-item {
            background: rgba(60, 64, 72, 0.6);
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #667eea;
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
            border-radius: 25px;
            padding: 30px;
            margin: 50px auto;
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.95);
            font-family: 'Poppins', sans-serif;
            font-size: 1.15rem;
            max-width: 900px;
            position: relative;
            z-index: 1;
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
                grid-template-rows: repeat(6, 1fr);
                padding: 15px;
            }
            .tool-card {
                margin: 10px 0;
                padding: 30px 25px;
                min-height: 320px;
            }
            .logo {
                width: 90px;
                height: 90px;
                font-size: 2.8rem;
            }
        }

        @media (max-width: 480px) {
            .main-title {
                font-size: 2.5rem;
            }
            .tool-icon {
                font-size: 4rem;
            }
            .tool-title {
                font-size: 1.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # Light theme CSS (similar structure with light colors)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Light theme styling */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
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
                radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 30%);
            animation: backgroundFloat 12s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes backgroundFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 1; }
            33% { transform: translateY(-15px) rotate(1deg); opacity: 0.8; }
            66% { transform: translateY(-30px) rotate(-1deg); opacity: 0.9; }
        }

        /* Creative title styling */
        .main-title {
            font-family: 'Poppins', sans-serif;
            font-size: 4.5rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 20%, #ffffff 40%, #f1f3f4 60%, #ffffff 80%, #f8f9fa 100%);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 25px 0 15px 0;
            text-shadow: 0 4px 20px rgba(255, 255, 255, 0.5);
            position: relative;
            z-index: 1;
            animation: gradientShift 4s ease-in-out infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
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
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 50px;
            font-weight: 400;
            position: relative;
            z-index: 1;
            font-style: italic;
        }

        /* Logo styling */
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 25px;
            position: relative;
            z-index: 1;
        }

        .logo {
            width: 120px;
            height: 120px;
            background: rgba(255, 255, 255, 0.25);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(15px);
            border: 3px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 12px 40px rgba(255, 255, 255, 0.3);
            font-size: 3.5rem;
            animation: logoFloat 4s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }

        .logo::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: logoShine 3s linear infinite;
        }

        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) scale(1) rotate(0deg); }
            50% { transform: translateY(-15px) scale(1.05) rotate(2deg); }
        }

        @keyframes logoShine {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }

        /* Enhanced tool cards - light theme */
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
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px 30px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.4);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            min-height: 350px;
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
            height: 5px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 100%;
            animation: borderShift 4s ease infinite;
        }

        .tool-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 0;
        }

        @keyframes borderShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .tool-card:hover {
            transform: translateY(-20px) scale(1.03);
            box-shadow: 0 25px 70px rgba(102, 126, 234, 0.4);
            background: rgba(255, 255, 255, 1);
            border-color: rgba(102, 126, 234, 0.4);
        }

        .tool-card:hover::after {
            opacity: 1;
        }

        .tool-icon {
            font-size: 5rem;
            margin-bottom: 25px;
            filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.2));
            transition: all 0.4s ease;
            position: relative;
            z-index: 1;
        }

        .tool-card:hover .tool-icon {
            transform: scale(1.15) rotate(8deg);
            filter: drop-shadow(0 15px 30px rgba(102, 126, 234, 0.4));
        }

        .tool-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 18px;
            line-height: 1.3;
            position: relative;
            z-index: 1;
        }

        .tool-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 1.05rem;
            color: #5a6c7d;
            line-height: 1.7;
            margin-bottom: 30px;
            flex-grow: 1;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }

        .tool-button {
            display: inline-block;
            padding: 18px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
            position: relative;
            z-index: 1;
            overflow: hidden;
        }

        .tool-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }

        .tool-button:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 45px rgba(102, 126, 234, 0.7);
            text-decoration: none;
            color: white;
        }

        .tool-button:hover::before {
            left: 100%;
        }

        /* Enhanced info sections */
        .features-section {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(25px);
            border-radius: 25px;
            padding: 40px;
            margin: 50px auto;
            max-width: 1000px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            position: relative;
            z-index: 1;
        }

        .features-title {
            font-family: 'Poppins', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            text-align: center;
            color: #ffffff;
            margin-bottom: 30px;
        }

        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .feature-item {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #667eea;
        }

        .feature-title {
            font-weight: 600;
            color: #ffffff;
            font-size: 1.1rem;
            margin-bottom: 8px;
        }

        .feature-desc {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .info-section {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(25px);
            border-radius: 25px;
            padding: 30px;
            margin: 50px auto;
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: rgba(255, 255, 255, 0.95);
            font-family: 'Poppins', sans-serif;
            font-size: 1.15rem;
            max-width: 900px;
            position: relative;
            z-index: 1;
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
                grid-template-rows: repeat(6, 1fr);
                padding: 15px;
            }
            .tool-card {
                margin: 10px 0;
                padding: 30px 25px;
                min-height: 320px;
            }
            .logo {
                width: 90px;
                height: 90px;
                font-size: 2.8rem;
            }
        }

        @media (max-width: 480px) {
            .main-title {
                font-size: 2.5rem;
            }
            .tool-icon {
                font-size: 4rem;
            }
            .tool-title {
                font-size: 1.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Creative logo and centered title
st.markdown("""
<div class="logo-container">
    <div class="logo">💎</div>
</div>
<h1 class="main-title">FinanceHub Pro</h1>
<p class="subtitle"><strong>Your Ultimate Financial Intelligence Platform</strong></p>
<p class="tagline">"Where Smart Money Decisions Begin"</p>
""", unsafe_allow_html=True)

# Enhanced description section
st.markdown("""
<div class="features-section">
    <h2 class="features-title">🌟 What Makes FinanceHub Pro Unique?</h2>
    <div class="features-list">
        <div class="feature-item">
            <div class="feature-title">🚀 <strong>AI-Powered Precision</strong></div>
            <div class="feature-desc">Advanced algorithms provide 99.9% accurate calculations with real-time market data integration</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">🔐 <strong>Bank-Grade Security</strong></div>
            <div class="feature-desc">Your financial data is protected with enterprise-level encryption and zero data storage</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">⚡ <strong>Lightning Fast</strong></div>
            <div class="feature-desc">Get instant results with our optimized calculation engine - no waiting, no delays</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">📱 <strong>Mobile-First Design</strong></div>
            <div class="feature-desc">Perfect experience across all devices with responsive, touch-friendly interfaces</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">🎯 <strong>Personalized Insights</strong></div>
            <div class="feature-desc">Smart recommendations based on your financial profile and Indian market conditions</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">📊 <strong>Interactive Visualizations</strong></div>
            <div class="feature-desc">Beautiful charts and graphs that make complex financial data easy to understand</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Enhanced tools data with better descriptions and bold formatting
tools = [
    {
        "name": "SIP Calculator",
        "desc": "**Master Systematic Investment Planning** with advanced projections, goal-based planning, and wealth growth analysis. Calculate returns for mutual funds, equity SIPs, and index funds with Indian market data.",
        "link": "https://financialreach.streamlit.app/",
        "icon": "📈"
    },
    {
        "name": "Credit Score Estimator", 
        "desc": "**AI-Powered Credit Analysis** using CIBIL-compatible algorithms. Get accurate score estimates, improvement strategies, and loan eligibility insights with personalized action plans.",
        "link": "https://creditscores.streamlit.app/",
        "icon": "💳"
    },
    {
        "name": "Tax Calculator",
        "desc": "**Smart Tax Optimization** for India's new tax regime. Calculate income tax liability, compare old vs new regimes, and discover maximum savings with HRA, 80C, and other deductions.",
        "link": "https://taxreturncalc.streamlit.app/",
        "icon": "🧾"
    },
    {
        "name": "EMI Calculator",
        "desc": "**Complete Loan Planning Suite** with advanced EMI calculations, amortization schedules, prepayment analysis, and comparison tools for home loans, personal loans, and vehicle financing.",
        "link": "https://emicalculatorsj.streamlit.app/",
        "icon": "🏦"
    },
    {
        "name": "Expense Tracker",
        "desc": "**Intelligent Expense Management** with AI-powered categorization, smart budgeting, spending pattern analysis, and financial health insights to optimize your money flow.",
        "link": "https://expensetrac.streamlit.app/",
        "icon": "💵"
    },
    {
        "name": "Retirement Planner",
        "desc": "**Strategic Retirement Planning** with inflation-adjusted calculations, corpus estimation, pension planning, and lifestyle maintenance analysis for a secure financial future.",
        "link": "https://retirementtrack.streamlit.app/",
        "icon": "👨‍🦳"
    }
]

# Create enhanced tools grid in 3x2 format
st.markdown('<div class="tools-grid">', unsafe_allow_html=True)
for tool in tools:
    st.markdown(
        f"""
        <div class="tool-card">
            <div>
                <div class="tool-icon">{tool["icon"]}</div>
                <h4 class="tool-title"><strong>{tool["name"]}</strong></h4>
                <p class="tool-desc">{tool["desc"]}</p>
            </div>
            <a href="{tool["link"]}" target="_blank" class="tool-button">
                <strong>Launch Tool →</strong>
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
    ✨ <strong>Completely Free Forever</strong> ✨<br>
    <strong>25,000+ Users Trust FinanceHub Pro</strong> for their financial decisions<br>
    🔒 <strong>Zero Data Storage</strong> • <strong>No Registration Required</strong> • <strong>Instant Results</strong> 🔒<br><br>
    <em>Powered by cutting-edge fintech algorithms trusted by leading financial institutions</em>
</div>
""", unsafe_allow_html=True)
