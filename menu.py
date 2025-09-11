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

# Professional Images Integration
hero_image_url = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
dashboard_image_url = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
analytics_image_url = "https://plus.unsplash.com/premium_photo-1682310156923-3f4a463610f0?q=80&w=912&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
calculator_image_url = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"

# Apply CSS based on theme state
if st.session_state.dark_mode:
    # Professional Dark theme CSS with navigation dashboard
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Hide Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Smooth scrolling */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* Dark theme styling */
        .stApp {{
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            font-family: 'Inter', sans-serif;
        }}
        
        /* Navigation Dashboard Styling */
        .nav-dashboard {{
            background: #2d3748;
            border: 1px solid #4a5568;
            border-radius: 12px;
            padding: 20px;
            margin: 30px auto;
            max-width: 1200px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            position: sticky;
            top: 10px;
            z-index: 100;
        }}
        
        .nav-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            font-weight: 600;
            text-align: center;
            color: #ffffff;
            margin-bottom: 20px;
            letter-spacing: 0.02em;
        }}
        
        .nav-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
        }}
        
        .nav-link {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px 16px;
            background: #374151;
            color: #e5e7eb;
            text-decoration: none;
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 0.9rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid #4b5563;
            min-height: 45px;
            cursor: pointer;
        }}
        
        .nav-link:hover {{
            background: #4F46E5;
            color: white;
            text-decoration: none;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }}
        
        .nav-link:active {{
            transform: translateY(0px);
        }}
        
        /* Main title styling */
        .main-title {{
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            text-align: center;
            color: #ffffff;
            margin: 40px 0 20px 0;
            letter-spacing: -0.02em;
        }}
        
        .subtitle {{
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            color: #e2e8f0;
            margin-bottom: 20px;
            font-weight: 500;
        }}
        
        .tagline {{
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #cbd5e0;
            margin-bottom: 40px;
            font-weight: 400;
            font-style: italic;
        }}
        
        /* Hero section styling */
        .hero-section {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 40px auto 60px auto;
            max-width: 1200px;
            padding: 40px 20px;
            background: rgba(45, 55, 72, 0.6);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            gap: 40px;
        }}
        
        .hero-content {{
            flex: 1;
            max-width: 500px;
        }}
        
        .hero-image {{
            flex: 1;
            max-width: 500px;
        }}
        
        .hero-image img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }}
        
        .hero-title {{
            font-size: 1.8rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 20px;
            line-height: 1.3;
        }}
        
        .hero-desc {{
            font-size: 1.1rem;
            line-height: 1.6;
            color: #cbd5e0;
            margin-bottom: 25px;
        }}
        
        .badge-container {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .badge {{
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            color: white;
        }}
        
        .badge-primary {{ background: #4F46E5; }}
        .badge-success {{ background: #10B981; }}
        .badge-warning {{ background: #F59E0B; }}
        
        /* Tools section header */
        .tools-header {{
            text-align: center;
            margin: 60px auto 40px auto;
            max-width: 800px;
        }}
        
        .tools-main-title {{
            font-family: 'Inter', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 20px;
        }}
        
        .tools-subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 1.2rem;
            color: #cbd5e0;
            margin-bottom: 40px;
        }}
        
        /* Professional tool cards */
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .tool-card {{
            background: #2d3748;
            border: 1px solid #4a5568;
            border-radius: 12px;
            padding: 24px;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            scroll-margin-top: 120px;
        }}
        
        .tool-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            transform: translateY(-2px);
            border-color: #718096;
        }}
        
        .tool-card:target {{
            border-color: #4F46E5;
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
            animation: highlight 2s ease-in-out;
        }}
        
        @keyframes highlight {{
            0% {{ box-shadow: 0 0 20px rgba(79, 70, 229, 0.8); }}
            50% {{ box-shadow: 0 0 30px rgba(79, 70, 229, 0.6); }}
            100% {{ box-shadow: 0 0 20px rgba(79, 70, 229, 0.4); }}
        }}
        
        .tool-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        
        .tool-desc {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #cbd5e0;
            line-height: 1.5;
            margin-bottom: 16px;
            flex-grow: 1;
        }}
        
        .tool-button {{
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
        }}
        
        .tool-button:hover {{
            background: #3B37DB;
            text-decoration: none;
            color: white;
        }}
        
        /* Professional info sections */
        .features-section {{
            background: #2d3748;
            border: 1px solid #4a5568;
            border-radius: 12px;
            padding: 32px;
            margin: 48px auto;
            max-width: 1000px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }}
        
        .features-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            text-align: center;
            color: #ffffff;
            margin-bottom: 28px;
        }}
        
        .features-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        
        .feature-item {{
            background: #374151;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4F46E5;
        }}
        
        .feature-title {{
            font-weight: 600;
            color: #ffffff;
            font-size: 1rem;
            margin-bottom: 8px;
        }}
        
        .feature-desc {{
            color: #d1d5db;
            font-size: 0.9rem;
            line-height: 1.5;
        }}
        
        .info-section {{
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
        }}
        
        /* Image showcase section */
        .showcase-section {{
            margin: 60px auto;
            max-width: 1200px;
            padding: 0 20px;
        }}
        
        .showcase-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            text-align: center;
            color: #ffffff;
            margin-bottom: 15px;
        }}
        
        .showcase-subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            text-align: center;
            color: #cbd5e0;
            margin-bottom: 40px;
        }}
        
        .showcase-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        
        .showcase-item {{
            background: #2d3748;
            border: 1px solid #4a5568;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
        
        .showcase-item img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        
        .showcase-caption {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #cbd5e0;
            line-height: 1.4;
        }}
        
        /* Responsive design */
        @media (max-width: 1024px) {{
            .tools-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .hero-section {{
                flex-direction: column;
                text-align: center;
            }}
            .nav-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 2.5rem;
            }}
            .tools-grid {{
                grid-template-columns: 1fr;
            }}
            .tool-card {{
                min-height: 140px;
            }}
            .nav-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .nav-dashboard {{
                position: static;
            }}
        }}
        
        @media (max-width: 480px) {{
            .nav-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)
    
else:
    # Professional Light theme CSS with navigation dashboard
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Hide Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Smooth scrolling */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* Professional light theme styling */
        .stApp {{
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
            color: #1a202c;
            font-family: 'Inter', sans-serif;
        }}
        
        /* Navigation Dashboard Styling */
        .nav-dashboard {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin: 30px auto;
            max-width: 1200px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 10px;
            z-index: 100;
        }}
        
        .nav-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            font-weight: 600;
            text-align: center;
            color: #2d3748;
            margin-bottom: 20px;
            letter-spacing: 0.02em;
        }}
        
        .nav-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
        }}
        
        .nav-link {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px 16px;
            background: #f7fafc;
            color: #4a5568;
            text-decoration: none;
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 0.9rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid #e2e8f0;
            min-height: 45px;
            cursor: pointer;
        }}
        
        .nav-link:hover {{
            background: #4F46E5;
            color: white;
            text-decoration: none;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
        }}
        
        .nav-link:active {{
            transform: translateY(0px);
        }}
        
        /* Main title styling */
        .main-title {{
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            text-align: center;
            color: #1a365d;
            margin: 40px 0 20px 0;
            letter-spacing: -0.02em;
        }}
        
        .subtitle {{
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            color: #4a5568;
            margin-bottom: 20px;
            font-weight: 500;
        }}
        
        .tagline {{
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #718096;
            margin-bottom: 40px;
            font-weight: 400;
            font-style: italic;
        }}
        
        /* Hero section styling */
        .hero-section {{
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
        }}
        
        .hero-content {{
            flex: 1;
            max-width: 500px;
        }}
        
        .hero-image {{
            flex: 1;
            max-width: 500px;
        }}
        
        .hero-image img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .hero-title {{
            font-size: 1.8rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 20px;
            line-height: 1.3;
        }}
        
        .hero-desc {{
            font-size: 1.1rem;
            line-height: 1.6;
            color: #4a5568;
            margin-bottom: 25px;
        }}
        
        .badge-container {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .badge {{
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            color: white;
        }}
        
        .badge-primary {{ background: #4F46E5; }}
        .badge-success {{ background: #10B981; }}
        .badge-warning {{ background: #F59E0B; }}
        
        /* Tools section header */
        .tools-header {{
            text-align: center;
            margin: 60px auto 40px auto;
            max-width: 800px;
        }}
        
        .tools-main-title {{
            font-family: 'Inter', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 20px;
        }}
        
        .tools-subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 1.2rem;
            color: #4a5568;
            margin-bottom: 40px;
        }}
        
        /* Professional tool cards */
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .tool-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            scroll-margin-top: 120px;
        }}
        
        .tool-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
            border-color: #cbd5e0;
        }}
        
        .tool-card:target {{
            border-color: #4F46E5;
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.3);
            animation: highlight 2s ease-in-out;
        }}
        
        @keyframes highlight {{
            0% {{ box-shadow: 0 0 20px rgba(79, 70, 229, 0.6); }}
            50% {{ box-shadow: 0 0 30px rgba(79, 70, 229, 0.4); }}
            100% {{ box-shadow: 0 0 20px rgba(79, 70, 229, 0.3); }}
        }}
        
        .tool-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        
        .tool-desc {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #718096;
            line-height: 1.5;
            margin-bottom: 16px;
            flex-grow: 1;
        }}
        
        .tool-button {{
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
        }}
        
        .tool-button:hover {{
            background: #3B37DB;
            text-decoration: none;
            color: white;
        }}
        
        /* Professional info sections */
        .features-section {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 32px;
            margin: 48px auto;
            max-width: 1000px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        
        .features-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            text-align: center;
            color: #2d3748;
            margin-bottom: 28px;
        }}
        
        .features-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        
        .feature-item {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4F46E5;
        }}
        
        .feature-title {{
            font-weight: 600;
            color: #2d3748;
            font-size: 1rem;
            margin-bottom: 8px;
        }}
        
        .feature-desc {{
            color: #4a5568;
            font-size: 0.9rem;
            line-height: 1.5;
        }}
        
        .info-section {{
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
        }}
        
        /* Image showcase section */
        .showcase-section {{
            margin: 60px auto;
            max-width: 1200px;
            padding: 0 20px;
        }}
        
        .showcase-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            text-align: center;
            color: #2d3748;
            margin-bottom: 15px;
        }}
        
        .showcase-subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            text-align: center;
            color: #718096;
            margin-bottom: 40px;
        }}
        
        .showcase-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        
        .showcase-item {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        .showcase-item img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        
        .showcase-caption {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #4a5568;
            line-height: 1.4;
        }}
        
        /* Responsive design */
        @media (max-width: 1024px) {{
            .tools-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .hero-section {{
                flex-direction: column;
                text-align: center;
            }}
            .nav-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 2.5rem;
            }}
            .tools-grid {{
                grid-template-columns: 1fr;
            }}
            .tool-card {{
                min-height: 140px;
            }}
            .nav-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .nav-dashboard {{
                position: static;
            }}
        }}
        
        @media (max-width: 480px) {{
            .nav-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

# Header section
st.markdown("""
<h1 class="main-title">Capital Compass</h1>
<p class="subtitle"><strong>All your financial solutions in one place</strong></p>
<p class="tagline">"Where Smart Money Decisions Begin"</p>
""", unsafe_allow_html=True)

# Navigation Dashboard with internal anchor links
st.markdown("""
<div class="nav-dashboard">
    <h3 class="nav-title"> Quick Access Financial Tools </h3>
    <div class="nav-grid">
        <a href="#sip-calculator" class="nav-link">📈 SIP Calculator</a>
        <a href="#credit-score" class="nav-link">💳 Credit Score</a>
        <a href="#tax-calculator" class="nav-link">📊 Tax Calculator</a>
        <a href="#emi-calculator" class="nav-link">🏠 EMI Calculator</a>
        <a href="#expense-tracker" class="nav-link">💰 Expense Tracker</a>
        <a href="#retirement-planner" class="nav-link">🏖️ Retirement Planner</a>
        <a href="#stock-market" class="nav-link">📈 Stock Market</a>
    </div>
</div>
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

# Tools section header
st.markdown("""
<div class="tools-header">
    <h2 class="tools-main-title">🛠️ Our Financial Tools Suite</h2>
    <p class="tools-subtitle">Comprehensive tools to manage every aspect of your financial journey</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Tools section with anchor IDs
tools = [
    {
        "id": "sip-calculator",
        "name": "SIP Calculator",
        "desc": "Master Systematic Investment Planning with advanced projections and wealth growth analysis for mutual funds and equity investments.",
        "link": "https://financialreach.streamlit.app/"
    },
    {
        "id": "credit-score",
        "name": "Credit Score Estimator", 
        "desc": "AI-Powered Credit Analysis using CIBIL-compatible algorithms with accurate score estimates and improvement strategies.",
        "link": "https://creditscores.streamlit.app/"
    },
    {
        "id": "tax-calculator",
        "name": "Tax Calculator",
        "desc": "Smart Tax Optimization for India's tax regime with liability calculations and deduction comparisons.",
        "link": "https://taxreturncalc.streamlit.app/"
    },
    {
        "id": "emi-calculator",
        "name": "EMI Calculator",
        "desc": "Complete Loan Planning Suite with EMI calculations, amortization schedules, and prepayment analysis.",
        "link": "https://emicalculatorsj.streamlit.app/"
    },
    {
        "id": "expense-tracker",
        "name": "Expense Tracker",
        "desc": "Intelligent Expense Management with AI-powered categorization and smart budgeting insights.",
        "link": "https://expensetrac.streamlit.app/"
    },
    {
        "id": "retirement-planner",
        "name": "Retirement Planner",
        "desc": "Strategic Retirement Planning with inflation-adjusted calculations and corpus estimation tools.",
        "link": "https://retirementtrack.streamlit.app/"
    },
    {
        "id": "stock-market",
        "name": "Stock Market checker",
        "desc": "Check realtime stock prices of your favourite stocks",
        "link": "https://demo-stockpeers.streamlit.app/?ref=streamlit-io-gallery-favorites&stocks=AAPL%2CMSFT%2CGOOGL%2CNVDA%2CAMZN%2CTSLA%2CMETA"
    }
]

st.markdown('<div class="tools-grid">', unsafe_allow_html=True)
for tool in tools:
    st.markdown(
        f"""
        <div class="tool-card" id="{tool["id"]}">
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

# Professional showcase section with images
st.markdown(f"""
<div class="showcase-section">
    <h2 class="showcase-title">Trusted by Financial Professionals</h2>
    <p class="showcase-subtitle">See how our tools compare to industry-leading financial platforms</p>
    <div class="showcase-grid">
        <div class="showcase-item">
            <img src="{dashboard_image_url}" alt="Modern Financial Dashboard" />
            <p class="showcase-caption">Advanced Analytics Dashboard - Real-time portfolio tracking and performance analysis</p>
        </div>
        <div class="showcase-item">
            <img src="{analytics_image_url}" alt="Investment Portfolio Interface" />
            <p class="showcase-caption">Investment Portfolio Management - Professional-grade tools for wealth management</p>
        </div>
        <div class="showcase-item">
            <img src="{calculator_image_url}" alt="Financial Calculator Interface" />
            <p class="showcase-caption">Professional Calculator Interface - Precision tools for complex financial calculations</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Enhanced info section
st.markdown("""
<div class="info-section">
    <strong>Completely Free Forever</strong><br>
    <em>Powered by cutting-edge fintech algorithms trusted by leading financial institutions</em>
</div>
""", unsafe_allow_html=True)
