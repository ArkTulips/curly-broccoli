import streamlit as st
import mysql.connector
import hashlib
import secrets
import time
from datetime import datetime

# ---------------------- Page Config ----------------------
st.set_page_config(
    page_title="Capital Compass - Professional Financial Management Portal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------- MySQL Connection ----------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",     # 🔹 change as needed
        user="root",          # 🔹 change as needed
        password="yourpassword",  # 🔹 change as needed
        database="capital_compass"
    )

# ---------------------- DB Setup ----------------------
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE,
            name VARCHAR(255),
            phone VARCHAR(20),
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            annual_income VARCHAR(50),
            monthly_expenses VARCHAR(50),
            investment_experience VARCHAR(50),
            risk_tolerance VARCHAR(50),
            financial_goals VARCHAR(255),
            savings_ratio VARCHAR(50),
            current_loans VARCHAR(50),
            loan_details VARCHAR(255),
            retirement_age VARCHAR(10),
            investment_strategy VARCHAR(255),
            stock_experience VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

setup_database()

# ---------------------- Password Hashing ----------------------
def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored_password, provided_password):
    try:
        salt, hashed = stored_password.split("$")
        return hashlib.sha256((salt + provided_password).encode()).hexdigest() == hashed
    except:
        return False

# ---------------------- User Management ----------------------
def register_user(email, full_name, phone, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if email exists
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False, "Email already registered!"

    # Insert new user
    password_hash = hash_password(password)
    cursor.execute(
        "INSERT INTO users (email, name, phone, password_hash) VALUES (%s, %s, %s, %s)",
        (email, full_name, phone, password_hash)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Registration successful!"

def authenticate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and verify_password(user['password_hash'], password):
        return user
    return None

def save_user_profile(user_id, profile_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM profiles WHERE user_id=%s", (user_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE profiles SET 
                annual_income=%s, monthly_expenses=%s, investment_experience=%s,
                risk_tolerance=%s, financial_goals=%s, savings_ratio=%s,
                current_loans=%s, loan_details=%s, retirement_age=%s,
                investment_strategy=%s, stock_experience=%s
            WHERE user_id=%s
        """, (
            profile_data['annual_income'],
            profile_data['monthly_expenses'],
            profile_data['investment_experience'],
            profile_data['risk_tolerance'],
            profile_data['financial_goals'],
            profile_data['savings_ratio'],
            profile_data['current_loans'],
            profile_data['loan_details'],
            profile_data['retirement_age'],
            profile_data['investment_strategy'],
            profile_data['stock_experience'],
            user_id
        ))
    else:
        cursor.execute("""
            INSERT INTO profiles (
                user_id, annual_income, monthly_expenses, investment_experience,
                risk_tolerance, financial_goals, savings_ratio,
                current_loans, loan_details, retirement_age,
                investment_strategy, stock_experience
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            user_id,
            profile_data['annual_income'],
            profile_data['monthly_expenses'],
            profile_data['investment_experience'],
            profile_data['risk_tolerance'],
            profile_data['financial_goals'],
            profile_data['savings_ratio'],
            profile_data['current_loans'],
            profile_data['loan_details'],
            profile_data['retirement_age'],
            profile_data['investment_strategy'],
            profile_data['stock_experience']
        ))

    conn.commit()
    cursor.close()
    conn.close()

# ---------------------- Session State ----------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "first_login" not in st.session_state:
    st.session_state.first_login = False

# ---------------------- UI Flow ----------------------
menu = st.sidebar.radio("Navigation", ["Login", "Register"])

if not st.session_state.authenticated:
    if menu == "Register":
        st.subheader("Create an Account")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if password != confirm_password:
                st.error("Passwords do not match!")
            else:
                success, msg = register_user(email, full_name, phone, password)
                if success:
                    st.success(msg)
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(msg)

    elif menu == "Login":
        st.subheader("Login to Capital Compass")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = authenticate_user(email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.first_login = True
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid email or password!")

# ---------------------- Onboarding ----------------------
if st.session_state.authenticated and st.session_state.first_login:
    st.subheader("Welcome! Complete Your Financial Profile")

    with st.form("onboarding_form"):
        annual_income = st.selectbox("Annual Income", ["<5L", "5-10L", "10-20L", "20L+"])
        monthly_expenses = st.selectbox("Monthly Expenses", ["<20K", "20-50K", "50-100K", "100K+"])
        investment_experience = st.selectbox("Investment Experience", ["None", "Beginner", "Intermediate", "Expert"])
        risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
        financial_goals = st.text_area("Financial Goals")
        savings_ratio = st.selectbox("Savings Ratio", ["<10%", "10-30%", "30-50%", "50%+"])
        current_loans = st.selectbox("Do you have loans?", ["Yes", "No"])
        loan_details = st.text_area("Loan Details (if any)")
        retirement_age = st.text_input("Planned Retirement Age")
        investment_strategy = st.text_area("Preferred Investment Strategy")
        stock_experience = st.selectbox("Stock Market Experience", ["None", "Beginner", "Intermediate", "Expert"])

        submitted = st.form_submit_button("Save Profile")

    if submitted:
        profile_data = {
            "annual_income": annual_income,
            "monthly_expenses": monthly_expenses,
            "investment_experience": investment_experience,
            "risk_tolerance": risk_tolerance,
            "financial_goals": financial_goals,
            "savings_ratio": savings_ratio,
            "current_loans": current_loans,
            "loan_details": loan_details,
            "retirement_age": retirement_age,
            "investment_strategy": investment_strategy,
            "stock_experience": stock_experience
        }
        save_user_profile(st.session_state.user['id'], profile_data)
        st.success("Profile saved successfully!")
        st.session_state.first_login = False
        time.sleep(2)
        st.rerun()

# ---------------------- Dashboard ----------------------
if st.session_state.authenticated and not st.session_state.first_login:
    st.subheader(f"Welcome back, {st.session_state.user['name']}!")
    st.write("✅ You are logged in and your profile is saved.")
    st.write("This is where your dashboard content will appear (financial analytics, recommendations, etc.).")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.first_login = False
        st.rerun()
