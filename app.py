import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def sip_calculator(monthly_investment, annual_rate, years):
    r = annual_rate / 100
    n = 12  # compounding monthly
    t = years

    # Future Value of SIP
    fv = monthly_investment * (((1 + r/n) ** (n * t) - 1) / (r/n)) * (1 + r/n)
    invested = monthly_investment * n * t
    gain = fv - invested
    profit_pct = (gain / invested) * 100
    return invested, fv, gain, profit_pct

def sip_growth_table(monthly_investment, annual_rate, years):
    r = annual_rate / 100
    n = 12
    data = []
    for yr in range(1, years + 1):
        fv = monthly_investment * (((1 + r/n) ** (n * yr) - 1) / (r/n)) * (1 + r/n)
        invested = monthly_investment * n * yr
        gain = fv - invested
        data.append([yr, invested, fv, gain])
    return pd.DataFrame(data, columns=["Year", "Invested (₹)", "Future Value (₹)", "Profit (₹)"])

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="SIP Calculator", layout="centered")
st.title("💰 SIP Calculator")

monthly = st.number_input("Monthly SIP (₹)", min_value=100, value=5000, step=500)
rate = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0, step=0.5)
years = st.number_input("Investment Duration (Years)", min_value=1, value=10, step=1)

if st.button("Calculate"):
    invested, fv, gain, pct = sip_calculator(monthly, rate, years)

    st.subheader("📊 Results")
    st.write(f"**Total Invested Amount:** ₹{invested:,.2f}")
    st.write(f"**Future Value (Maturity):** ₹{fv:,.2f}")
    st.write(f"**Total Returns (Profit):** ₹{gain:,.2f}")
    st.write(f"**Profit Percentage:** {pct:.2f}%")

    # Year-wise growth
    st.subheader("📈 Yearly Growth")
    df = sip_growth_table(monthly, rate, years)
    st.dataframe(df.style.format({"Invested (₹)": "{:,.2f}", "Future Value (₹)": "{:,.2f}", "Profit (₹)": "{:,.2f}"}))

    # Chart
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(df["Year"], df["Invested (₹)"], label="Invested Amount", marker="o")
    ax.plot(df["Year"], df["Future Value (₹)"], label="Future Value", marker="o")
    ax.fill_between(df["Year"], df["Invested (₹)"], df["Future Value (₹)"], alpha=0.2, color="green")
    ax.set_xlabel("Year")
    ax.set_ylabel("Amount (₹)")
    ax.set_title("SIP Growth Over Time")
    ax.legend()
    st.pyplot(fig)
