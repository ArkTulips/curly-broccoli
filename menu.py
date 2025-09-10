import streamlit as st

st.set_page_config(page_title="Finance Tools", layout="centered")
st.title("💰 Finance Tools Dashboard")
st.write("Welcome! Use the links below to navigate to your preferred financial tool.")

st.markdown("---")

st.subheader("1️⃣ SIP Calculator")
st.write("Calculate SIP returns and profit percentage.")
st.markdown("[➡️ Go to SIP Calculator](https://financialreach.streamlit.app/)")

st.subheader("2️⃣ Credit Score Estimator")
st.write("Estimate your credit score based on CIBIL-like logic.")
st.markdown("[➡️ Go to Credit Score Estimator](https://creditscores.streamlit.app/)")

st.subheader("3️⃣ Tax Calculator")
st.write("Calculate your income tax under the new regime.")
st.markdown("[➡️ Go to Tax Calculator](https://yourname-tax.streamlit.app)")

st.subheader("4️⃣ EMI calculator")
st.write("Calculate your EMI.")
st.markdown("[➡️ Go to EMI calculator](https://emicalculatorsj.streamlit.app/)")

st.markdown("---")
st.info("Each tool opens in a new tab on Streamlit Cloud.")
