import streamlit as st

st.set_page_config(page_title="Finance Tools", layout="wide")

st.title(" Finance Tools Dashboard")
st.write("Welcome! Select a tool below to get started:")

st.markdown("---")

# Define tools
tools = [
    {
        "name": "SIP Calculator",
        "desc": "Calculate SIP returns and profit percentage.",
        "link": "https://financialreach.streamlit.app/",
        "icon": "📈"
    },
    {
        "name": "Credit Score Estimator",
        "desc": "Estimate your credit score based on CIBIL-like logic.",
        "link": "https://creditscores.streamlit.app/",
        "icon": "💳"
    },
    {
        "name": "Tax Calculator",
        "desc": "Calculate your income tax under the new regime.",
        "link": "https://taxreturncalc.streamlit.app/",
        "icon": "🧾"
    },
    {
        "name": "EMI Calculator",
        "desc": "Calculate your monthly loan EMI.",
        "link": "https://emicalculatorsj.streamlit.app/",
        "icon": "🏦"
    },
    {
        "name": "Expense Tracker",
        "desc": "Track your monthly and overall expenses.",
        "link": "https://expensetrac.streamlit.app/",
        "icon": "💵"
    }
]

# Display in columns
cols = st.columns(3)

for i, tool in enumerate(tools):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:15px; background-color:#f9f9f9;
                        margin:10px; text-align:center; box-shadow:0px 4px 8px rgba(0,0,0,0.1);">
                <div style="font-size:100px; margin-bottom:10px;">{tool['icon']}</div>
                <h4 style="margin-bottom:5px;">{tool['name']}</h4>
                <p style="font-size:30px; color:#555;">{tool['desc']}</p>
                <a href="{tool['link']}" target="_blank"
                   style="display:inline-block; padding:10px 18px; background:#4CAF50; color:white;
                          border-radius:8px; text-decoration:none; margin-top:10px; font-weight:bold;">
                   Open Tool ➡️
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")
st.info("Each tool will open in a new tab on Streamlit Cloud.")
