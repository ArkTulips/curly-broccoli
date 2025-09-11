import streamlit as st
import json
import os

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Capital Compass",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# JSON Helpers
# -----------------------------
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {"admin": "admin123"}  # default user

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# -----------------------------
# Session state setup
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"  # login | register | menu
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "username" not in st.session_state:
    st.session_state.username = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# -----------------------------
# Navigation helper
# -----------------------------
def go_to(page):
    st.session_state.page = page
    st.rerun()

# -----------------------------
# Login Page
# -----------------------------
def login_page():
    st.title("🔐 Login - Capital Compass")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.username = username
            go_to("menu")
        else:
            st.error("❌ Invalid username or password")

    st.markdown("Don't have an account?")
    if st.button("👉 Go to Register"):
        go_to("register")

# -----------------------------
# Register Page
# -----------------------------
def register_page():
    st.title("📝 Register - Capital Compass")

    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")

    if st.button("Register"):
        if new_user in st.session_state.users:
            st.error("⚠️ Username already exists!")
        elif not new_user or not new_pass:
            st.warning("⚠️ Username and password cannot be empty")
        else:
            st.session_state.users[new_user] = new_pass
            save_users(st.session_state.users)
            st.success("✅ Registration successful! Please login.")
            go_to("login")

    if st.button("⬅️ Back to Login"):
        go_to("login")

# -----------------------------
# Main Capital Compass Menu
# -----------------------------
def menu_page():
    st.sidebar.success(f"✅ Logged in as: {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.username = None
        go_to("login")

    # Dark/Light theme toggle
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # Hero section
    st.markdown(
        f"""
        <div style="padding:20px; border-radius:15px; text-align:center; 
            background: {"#111111; color:white" if st.session_state.dark_mode else "#f4f4f4; color:black"}">
            <h1>💹 Capital Compass</h1>
            <p>Your Ultimate Financial Companion</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main menu (replace with your full menu items)
    menu = st.radio(
        "Choose a section:",
        ["🏠 Dashboard", "📈 Stock Tools", "💳 Credit Tools", "⚙️ Settings"],
        horizontal=True,
    )

    if menu == "🏠 Dashboard":
        st.subheader("📊 Overview Dashboard")
        st.write("Show key metrics here...")

    elif menu == "📈 Stock Tools":
        st.subheader("📈 Stock Analysis")
        st.write("Stock tools go here...")

    elif menu == "💳 Credit Tools":
        st.subheader("💳 Credit Tools")
        st.write("Credit calculators, reports, etc.")

    elif menu == "⚙️ Settings":
        st.subheader("⚙️ User Settings")
        st.write("Preferences, profile, etc.")

# -----------------------------
# Router
# -----------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "menu":
    menu_page()
