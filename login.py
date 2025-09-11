import streamlit as st
import json
import os

# File to store user credentials
USER_FILE = "users.json"

# Load users
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {"admin": "admin123"}  # default user

# Save users
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Load existing users
users = load_users()

st.title("🔐 Login Page")

# Login inputs
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    if username in users and users[username] == password:
        st.success("✅ Login successful!")
        st.markdown(
            """
            <meta http-equiv="refresh" content="0; url='https://menufin.streamlit.app/'" />
            """,
        )
            unsafe_allow_html=True,
    else:
        st.error("❌ Invalid credentials")

# Register new user
st.write("Don't have an account? Register below:")
new_user = st.text_input("New Username")
new_pass = st.text_input("New Password", type="password")

if st.button("Register"):
    if new_user in users:
        st.error("⚠️ Username already exists!")
    elif not new_user or not new_pass:
        st.warning("⚠️ Username and password cannot be empty")
    else:
        users[new_user] = new_pass
        save_users(users)
        st.success("✅ Registration successful! You can now login.")
