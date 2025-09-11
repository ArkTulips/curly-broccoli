import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Personalized Advanced SIP Calculator", 
    layout="wide",
    page_icon="📈"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


# --- Core Functions ---
def calculate_sip_with_stepup(monthly_investment, annual_rate, years, step_up_rate=0, inflation_rate=0):
    """Enhanced SIP calculator with step-up and inflation adjustment"""
    monthly_rate = annual_rate / (100 * 12)
    total_invested = 0
    future_value = 0
    yearly_data = []
    current_monthly = monthly_investment

    for year in range(1, years + 1):
        year_invested = current_monthly * 12
        total_invested += year_invested

        remaining_years = years - year + 1
        months_remaining = remaining_years * 12

        if monthly_rate > 0:
            year_fv = current_monthly * (((1 + monthly_rate) ** 12 - 1) / monthly_rate) * (1 + monthly_rate) ** (months_remaining - 12)
        else:
            year_fv = current_monthly * 12 * remaining_years

        future_value += year_fv

        real_value = future_value / ((1 + inflation_rate/100) ** year) if inflation_rate > 0 else future_value

        yearly_data.append({
            'Year': year,
            'Monthly SIP': current_monthly,
            'Yearly Investment': year_invested,
            'Cumulative Investment': total_invested,
            'Future Value': future_value,
            'Real Value': real_value
        })

        current_monthly = current_monthly * (1 + step_up_rate/100)

    total_returns = future_value - total_invested
    inflation_adjusted_value = future_value / ((1 + inflation_rate/100) ** years) if inflation_rate > 0 else future_value

    return {
        'total_invested': total_invested,
        'future_value': future_value,
        'total_returns': total_returns,
        'inflation_adjusted_value': inflation_adjusted_value,
        'yearly_data': yearly_data,
        'effective_rate': ((future_value / total_invested) ** (1/years) - 1) * 100 if total_invested > 0 else 0
    }


def create_pie_chart(invested, returns):
    labels = ['Total Investment', 'Returns Generated']
    values = [invested, returns]
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=0.4,
        marker_colors=['#ff9999', '#66b3ff']
    )])
    fig.update_layout(
        title="Investment vs Returns Breakdown",
        title_x=0.5,
        height=400
    )
    return fig


def create_growth_chart(yearly_data):
    df = pd.DataFrame(yearly_data)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Cumulative Investment'],
        mode='lines+markers',
        name='Investment',
        line=dict(color='red', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Future Value'],
        mode='lines+markers',
        name='Future Value',
        line=dict(color='blue', width=2)
    ))

    if 'Real Value' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Real Value'],
            mode='lines+markers',
            name='Real Value',
            line=dict(color='green', width=2, dash='dash')
        ))

    fig.update_layout(
        title="Investment Growth Over Time",
        title_x=0.5,
        xaxis_title="Years",
        yaxis_title="Amount (₹)",
        height=500
    )
    return fig


# --- Main App ---
def main():
    st.markdown('<h1 class="main-header">📈 Advanced SIP Calculator</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## 📋 Investment Parameters")

        monthly_investment = st.number_input("Monthly SIP Amount (₹)", min_value=500, value=5000, step=500)
        years = st.number_input("Investment Duration (Years)", min_value=1, max_value=40, value=15, step=1)
        annual_rate = st.slider("Expected Annual Return (%)", min_value=5.0, max_value=20.0, value=12.0, step=0.5)
        step_up_rate = st.slider("Annual Step-up Rate (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5)
        inflation_rate = st.slider("Expected Inflation Rate (%)", min_value=0.0, max_value=10.0, value=6.0, step=0.5)

    if st.button("🧮 Calculate SIP", type="primary"):
        result = calculate_sip_with_stepup(monthly_investment, annual_rate, years, step_up_rate, inflation_rate)

        st.markdown('<h2 class="sub-header">📈 Investment Results</h2>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Invested", f"₹{result['total_invested']:,.0f}")
        with col2:
            st.metric("🎯 Future Value", f"₹{result['future_value']:,.0f}",
                      delta=f"+{((result['future_value']/result['total_invested'])*100-100):.1f}%")
        with col3:
            st.metric("📈 Total Returns", f"₹{result['total_returns']:,.0f}",
                      delta=f"{result['effective_rate']:.1f}% annually")
        with col4:
            st.metric("💵 Real Value", f"₹{result['inflation_adjusted_value']:,.0f}",
                      delta=f"After {inflation_rate}% inflation")

        st.markdown('<h2 class="sub-header">📊 Visual Analysis</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            pie_fig = create_pie_chart(result['total_invested'], result['total_returns'])
            st.plotly_chart(pie_fig, use_container_width=True)

        with col2:
            st.markdown("### 📊 Investment Summary")
            st.markdown(f"""
            - **Monthly Investment:** ₹{monthly_investment:,.0f}
            - **Investment Period:** {years} years
            - **Growth Multiple:** {result['future_value']/result['total_invested']:.1f}x
            - **Effective Return:** {result['effective_rate']:.1f}% p.a.
            """)

        growth_fig = create_growth_chart(result['yearly_data'])
        st.plotly_chart(growth_fig, use_container_width=True)

        st.markdown('<h2 class="sub-header">📋 Year-wise Breakdown</h2>', unsafe_allow_html=True)
        df = pd.DataFrame(result['yearly_data'])
        df_display = df.copy()
        for col in ['Monthly SIP', 'Yearly Investment', 'Cumulative Investment', 'Future Value', 'Real Value']:
            df_display[col] = df_display[col].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(df_display, use_container_width=True)


if __name__ == "__main__":
    main()
