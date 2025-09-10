import streamlit as st

# Function to calculate EMI
def calculate_emi(principal, annual_rate, tenure_years):
    monthly_rate = annual_rate / (12 * 100)  # Annual to monthly interest
    tenure_months = tenure_years * 12        # Years to months
    
    if monthly_rate == 0:  # No interest case
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)
    return emi

# Streamlit App
st.title("💰 EMI Calculator")

# Input fields
P = st.number_input("Enter the loan amount (Principal):", min_value=0.0, step=1000.0)
R = st.number_input("Enter the annual interest rate (%):", min_value=0.0, step=0.1)
N = st.number_input("Enter the loan tenure (years):", min_value=1, step=1)

if st.button("Calculate EMI"):
    if P > 0 and N > 0:
        emi = calculate_emi(P, R, N)
        total_payment = emi * N * 12
        total_interest = total_payment - P

        st.success(f"📌 For a loan of ₹{P:,.2f} at {R}% annual interest over {N} years:")
        st.write(f"*Monthly EMI:* ₹{emi:,.2f}")
        st.write(f"*Total Payment:* ₹{total_payment:,.2f}")
        st.write(f"*Total Interest:* ₹{total_interest:,.2f}")
    else:
        st.warning("Please enter valid loan details.")
