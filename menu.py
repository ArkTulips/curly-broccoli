import streamlit as st
import json
import os

# ==============================
# USER AUTH SYSTEM
# ==============================

USER_FILE = "users.json"

# Load users
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


def save_users():
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def login_page():
    st.title("🔐 Welcome to Capital Compass")

    menu = st.radio("Select Option", ["Login", "Register"])

    if menu == "Register":
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            if new_user in users:
                st.warning("⚠️ User already exists!")
            elif new_user.strip() == "" or new_pass.strip() == "":
                st.warning("⚠️ Username and Password cannot be empty")
            else:
                users[new_user] = new_pass
                save_users()
                st.success("✅ Registration successful! Please log in.")

    elif menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Welcome {username}!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials")


# ==============================
# MAIN APP (Capital Compass)
# ==============================

def main_page():
    # Page config
    st.set_page_config(
        page_title="Capital Compass - Your Ultimate Financial Companion",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Sidebar logout
    with st.sidebar:
        st.subheader(f"👤 Logged in as {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

    # Main content
    st.title("📊 Capital Compass")
    st.write("Your personalized financial toolkit — plan, track, and grow your wealth.")

    st.subheader("Available Tools")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📈 SIP Calculator")
        st.write("Estimate future value of your SIP investments.")
        st.link_button("Launch Tool", "#")

    with col2:
        st.markdown("### 💳 Credit Score Estimator")
        st.write("Check your estimated credit score range.")
        st.link_button("Launch Tool", "#")

    with col3:
        st.markdown("### 🏦 Tax Calculator")
        st.write("Simplify your annual tax calculations.")
        st.link_button("Launch Tool", "#")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("### 📉 EMI Calculator")
        st.write("Plan your loans with detailed EMI breakdowns.")
        st.link_button("Launch Tool", "#")

    with col5:
        st.markdown("### 📊 Expense Tracker")
        st.write("Track daily expenses and manage budgets.")
        st.link_button("Launch Tool", "#")

    with col6:
        st.markdown("### 👵 Retirement Planner")
        st.write("Plan your retirement corpus and goals.")
        st.link_button("Launch Tool", "#")


# ==============================
# APP FLOW
# ==============================
if st.session_state.logged_in:
    main_page()
else:
    login_page()
