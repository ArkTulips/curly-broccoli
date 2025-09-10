import streamlit as st

# --- MENU SETUP ---
st.sidebar.title("📌 Finance Tools")
menu = st.sidebar.radio(
    "Navigate",
    ["🏦 SIP Calculator", "💳 Credit Score Estimator", "🧾 Tax Calculator"]
)

# --- PAGE HANDLER ---
if menu == "🏦 SIP Calculator":
    st.title("🏦 SIP Calculator")
    st.write("Calculate SIP returns with profit percentage.")
    # import or call your SIP calculator code here

elif menu == "💳 Credit Score Estimator":
    st.title("💳 Credit Score Estimator")
    st.write("Estimate your credit score based on CIBIL-like logic.")
    # import or call your Credit Score code here

elif menu == "🧾 Tax Calculator":
    st.title("🧾 Tax Calculator")
    st.write("Calculate your income tax under the new regime.")
    # import or call your Tax Calculator code here
