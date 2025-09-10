import streamlit as st

def calculate_cibil_score(payment_history, credit_utilization, credit_history_years, credit_mix, recent_inquiries):
    weights = {
        "payment_history": 0.35,
        "credit_utilization": 0.30,
        "credit_history": 0.15,
        "credit_mix": 0.10,
        "recent_inquiries": 0.10
    }

    ph_score = payment_history * weights["payment_history"]
    cu_score = (100 - credit_utilization) * weights["credit_utilization"]
    ch_score = min(credit_history_years * 7, 100) * weights["credit_history"]
    cm_score = credit_mix * weights["credit_mix"]
    ri_score = max(100 - (recent_inquiries * 20), 0) * weights["recent_inquiries"]

    total_percentage = ph_score + cu_score + ch_score + cm_score + ri_score
    return int(300 + (total_percentage / 100) * 600)

st.set_page_config(page_title="CIBIL Score Estimator", layout="centered")
st.title("📊 CIBIL Score Estimator")

ph = st.slider("Payment History (% on-time)", 0, 100, 90)
cu = st.slider("Credit Utilization (%)", 0, 100, 30)
ch = st.slider("Credit History Length (years)", 0, 20, 5)
cm = st.slider("Credit Mix (0=poor, 100=excellent)", 0, 100, 70)
ri = st.slider("Recent Credit Inquiries", 0, 10, 1)

if st.button("Calculate CIBIL Score"):
    score = calculate_cibil_score(ph, cu, ch, cm, ri)
    st.success(f"Your Estimated CIBIL Score: {score}")

    if score >= 750:
        st.write("✅ Excellent: Eligible for best loans & cards")
    elif score >= 700:
        st.write("🙂 Good: Eligible for most loans")
    elif score >= 650:
        st.write("😐 Fair: Might face higher interest rates")
    else:
        st.write("❌ Poor: Loan approval chances low")
st.markdown(
    """
    ---
    🔙 [Back to SIP Calculator](https://yourname-sip.streamlit.app)
    """,
    unsafe_allow_html=True
)
