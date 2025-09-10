import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="Advanced EMI Calculator", layout="wide")

# Advanced EMI calculation functions
def calculate_emi(principal, annual_rate, tenure_years):
    '''Calculate standard EMI'''
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) /               ((1 + monthly_rate) ** tenure_months - 1)
    return emi

def calculate_step_up_emi(principal, annual_rate, tenure_years, step_up_rate, step_frequency=12):
    '''Calculate step-up EMI with periodic increases'''
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12

    # Start with a lower EMI and calculate step-up pattern
    initial_emi = calculate_emi(principal, annual_rate, tenure_years) * 0.8  # Start 20% lower

    schedule = []
    remaining_balance = principal
    current_emi = initial_emi

    for month in range(1, tenure_months + 1):
        if month % step_frequency == 1 and month > 1:  # Increase EMI annually
            current_emi *= (1 + step_up_rate / 100)

        interest_payment = remaining_balance * monthly_rate
        principal_payment = min(current_emi - interest_payment, remaining_balance)

        if principal_payment <= 0:
            principal_payment = remaining_balance
            current_emi = interest_payment + principal_payment

        remaining_balance -= principal_payment

        schedule.append({
            'Month': month,
            'EMI': current_emi,
            'Principal': principal_payment,
            'Interest': interest_payment,
            'Balance': remaining_balance
        })

        if remaining_balance <= 0:
            break

    return pd.DataFrame(schedule)

def calculate_step_down_emi(principal, annual_rate, tenure_years, step_down_rate, step_frequency=12):
    '''Calculate step-down EMI with periodic decreases'''
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12

    # Start with a higher EMI
    initial_emi = calculate_emi(principal, annual_rate, tenure_years) * 1.3  # Start 30% higher

    schedule = []
    remaining_balance = principal
    current_emi = initial_emi

    for month in range(1, tenure_months + 1):
        if month % step_frequency == 1 and month > 1:  # Decrease EMI annually
            current_emi *= (1 - step_down_rate / 100)

        interest_payment = remaining_balance * monthly_rate
        principal_payment = min(current_emi - interest_payment, remaining_balance)

        if principal_payment <= 0:
            principal_payment = remaining_balance
            current_emi = interest_payment + principal_payment

        remaining_balance -= principal_payment

        schedule.append({
            'Month': month,
            'EMI': current_emi,
            'Principal': principal_payment,
            'Interest': interest_payment,
            'Balance': remaining_balance
        })

        if remaining_balance <= 0:
            break

    return pd.DataFrame(schedule)

def calculate_amortization_schedule(principal, annual_rate, tenure_years, extra_payment=0):
    '''Generate complete amortization schedule'''
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    emi = calculate_emi(principal, annual_rate, tenure_years)

    schedule = []
    remaining_balance = principal

    for month in range(1, tenure_months + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = emi - interest_payment + extra_payment

        if principal_payment > remaining_balance:
            principal_payment = remaining_balance
            emi_actual = interest_payment + principal_payment
        else:
            emi_actual = emi + extra_payment

        remaining_balance -= principal_payment

        schedule.append({
            'Month': month,
            'EMI': emi_actual,
            'Principal': principal_payment,
            'Interest': interest_payment,
            'Balance': remaining_balance,
            'Cumulative_Interest': sum([row['Interest'] for row in schedule]) + interest_payment,
            'Cumulative_Principal': principal - remaining_balance
        })

        if remaining_balance <= 0:
            break

    return pd.DataFrame(schedule)

def calculate_interest_only(principal, annual_rate, tenure_years):
    '''Calculate interest-only payments'''
    monthly_rate = annual_rate / (12 * 100)
    monthly_interest = principal * monthly_rate
    return monthly_interest

def calculate_balloon_payment(principal, annual_rate, tenure_years, balloon_percent=30):
    '''Calculate balloon payment scenario'''
    balloon_amount = principal * (balloon_percent / 100)
    reduced_principal = principal - balloon_amount
    regular_emi = calculate_emi(reduced_principal, annual_rate, tenure_years)

    return regular_emi, balloon_amount

# Streamlit App
st.title("🏦 Advanced EMI Calculator & Loan Comparison Tool")
st.markdown("### Calculate EMIs, compare repayment methods, and plan your finances effectively")

# Sidebar for inputs
with st.sidebar:
    st.header("📊 Loan Parameters")

    # Basic loan details
    P = st.number_input("💰 Loan Amount (Principal):", min_value=0.0, value=500000.0, step=10000.0, format="%.2f")
    R = st.number_input("📈 Annual Interest Rate (%):", min_value=0.0, value=8.5, step=0.1, format="%.2f")
    N = st.number_input("📅 Loan Tenure (years):", min_value=1, value=20, step=1)

    st.markdown("---")

    # Advanced options
    st.subheader("🔧 Advanced Options")

    extra_payment = st.number_input("💵 Extra Monthly Payment:", min_value=0.0, value=0.0, step=500.0)

    # Step-up/Step-down parameters
    step_up_rate = st.slider("📈 Step-up Rate (%/year):", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
    step_down_rate = st.slider("📉 Step-down Rate (%/year):", min_value=0.0, max_value=20.0, value=5.0, step=0.5)

    # Balloon payment
    balloon_percent = st.slider("🎈 Balloon Payment (% of loan):", min_value=0, max_value=50, value=30, step=5)

# Main content area with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Standard EMI", "📈 Payment Comparison", "📋 Amortization Schedule", "💡 Advanced Scenarios", "📖 Payment Methods Guide"])

with tab1:
    st.header("Standard EMI Calculation")

    if P > 0 and N > 0:
        # Standard EMI calculation
        emi = calculate_emi(P, R, N)
        total_payment = emi * N * 12
        total_interest = total_payment - P

        # Display results in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Monthly EMI", f"₹{emi:,.2f}")
        with col2:
            st.metric("Total Payment", f"₹{total_payment:,.2f}")
        with col3:
            st.metric("Total Interest", f"₹{total_interest:,.2f}")

        # EMI Breakdown Chart
        fig = go.Figure(data=[
            go.Pie(labels=['Principal', 'Interest'], 
                   values=[P, total_interest],
                   hole=0.3,
                   marker_colors=['#2E8B57', '#DC143C'])
        ])
        fig.update_layout(title="Loan Breakdown: Principal vs Interest")
        st.plotly_chart(fig, use_container_width=True)

        # Impact of extra payments
        if extra_payment > 0:
            st.subheader("💵 Impact of Extra Payments")
            schedule_extra = calculate_amortization_schedule(P, R, N, extra_payment)
            total_months_extra = len(schedule_extra)
            total_interest_extra = schedule_extra['Interest'].sum()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Reduced Tenure", f"{total_months_extra} months", f"-{N*12 - total_months_extra} months")
            with col2:
                st.metric("Interest Savings", f"₹{total_interest - total_interest_extra:,.2f}")
            with col3:
                st.metric("Time Saved", f"{(N*12 - total_months_extra)/12:.1f} years")

with tab2:
    st.header("Payment Method Comparison")

    if P > 0 and N > 0:
        # Calculate different payment methods
        standard_emi = calculate_emi(P, R, N)
        interest_only = calculate_interest_only(P, R, N)
        balloon_emi, balloon_amount = calculate_balloon_payment(P, R, N, balloon_percent)

        # Step-up and step-down calculations
        step_up_schedule = calculate_step_up_emi(P, R, N, step_up_rate)
        step_down_schedule = calculate_step_down_emi(P, R, N, step_down_rate)

        # Comparison table
        comparison_data = {
            'Payment Method': [
                'Standard EMI',
                'Step-up EMI (Initial)',
                'Step-up EMI (Final)',
                'Step-down EMI (Initial)', 
                'Step-down EMI (Final)',
                'Interest Only',
                'Balloon Payment + Final'
            ],
            'Monthly Payment': [
                f"₹{standard_emi:,.2f}",
                f"₹{step_up_schedule.iloc[0]['EMI']:,.2f}",
                f"₹{step_up_schedule.iloc[-1]['EMI']:,.2f}",
                f"₹{step_down_schedule.iloc[0]['EMI']:,.2f}",
                f"₹{step_down_schedule.iloc[-1]['EMI']:,.2f}",
                f"₹{interest_only:,.2f}",
                f"₹{balloon_emi:,.2f} + ₹{balloon_amount:,.2f}"
            ],
            'Total Interest': [
                f"₹{(standard_emi * N * 12) - P:,.2f}",
                f"₹{step_up_schedule['Interest'].sum():,.2f}",
                "-",
                f"₹{step_down_schedule['Interest'].sum():,.2f}",
                "-",
                f"₹{interest_only * N * 12:,.2f}",
                f"₹{(balloon_emi * N * 12) - (P - balloon_amount):,.2f}"
            ],
            'Best For': [
                'Stable income, predictable budgeting',
                'Young professionals expecting salary growth',
                '',
                'High current income, expecting reduction',
                '',
                'Short-term cash flow management',
                'Business loans, expecting future lump sum'
            ]
        }

        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)

with tab3:
    st.header("📋 Detailed Amortization Schedule")

    if P > 0 and N > 0:
        schedule = calculate_amortization_schedule(P, R, N, extra_payment)

        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Months", len(schedule))
        with col2:
            st.metric("Total Interest", f"₹{schedule['Interest'].sum():,.2f}")
        with col3:
            st.metric("Interest Saved", f"₹{(calculate_emi(P, R, N) * N * 12 - P) - schedule['Interest'].sum():,.2f}")
        with col4:
            st.metric("Time Saved", f"{N*12 - len(schedule)} months")

        # Show data table with pagination
        st.subheader("📊 Amortization Table")

        # Add year grouping option
        view_option = st.radio("View by:", ["Monthly", "Yearly"])

        if view_option == "Yearly":
            yearly_data = []
            for year in range(1, int(len(schedule)/12) + 2):
                year_data = schedule[(schedule['Month'] > (year-1)*12) & (schedule['Month'] <= year*12)]
                if not year_data.empty:
                    yearly_data.append({
                        'Year': year,
                        'EMI Payments': len(year_data),
                        'Total EMI': year_data['EMI'].sum(),
                        'Principal Paid': year_data['Principal'].sum(),
                        'Interest Paid': year_data['Interest'].sum(),
                        'Year-end Balance': year_data.iloc[-1]['Balance'] if len(year_data) > 0 else 0
                    })

            yearly_df = pd.DataFrame(yearly_data)
            st.dataframe(yearly_df, use_container_width=True)
        else:
            # Display monthly schedule (first 60 months by default)
            display_months = st.slider("Show first N months:", min_value=12, max_value=len(schedule), value=min(60, len(schedule)))
            display_schedule = schedule.head(display_months).copy()

            # Format currency columns
            for col in ['EMI', 'Principal', 'Interest', 'Balance']:
                display_schedule[col] = display_schedule[col].apply(lambda x: f"₹{x:,.2f}")

            st.dataframe(display_schedule, use_container_width=True)

with tab4:
    st.header("💡 Advanced Loan Scenarios")

    # Loan comparison tool
    st.subheader("🔍 Compare Multiple Loan Offers")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Loan Option 1**")
        rate1 = st.number_input("Interest Rate 1 (%):", value=8.5, key="rate1")
        tenure1 = st.number_input("Tenure 1 (years):", value=20, key="tenure1")

    with col2:
        st.write("**Loan Option 2**")
        rate2 = st.number_input("Interest Rate 2 (%):", value=9.0, key="rate2")
        tenure2 = st.number_input("Tenure 2 (years):", value=15, key="tenure2")

    with col3:
        st.write("**Loan Option 3**")
        rate3 = st.number_input("Interest Rate 3 (%):", value=8.75, key="rate3")
        tenure3 = st.number_input("Tenure 3 (years):", value=25, key="tenure3")

    if st.button("Compare Loan Options"):
        options_data = []
        for i, (rate, tenure) in enumerate([(rate1, tenure1), (rate2, tenure2), (rate3, tenure3)], 1):
            emi = calculate_emi(P, rate, tenure)
            total_payment = emi * tenure * 12
            total_interest = total_payment - P

            options_data.append({
                'Option': f'Loan {i}',
                'Interest Rate': f"{rate}%",
                'Tenure': f"{tenure} years",
                'Monthly EMI': f"₹{emi:,.2f}",
                'Total Payment': f"₹{total_payment:,.2f}",
                'Total Interest': f"₹{total_interest:,.2f}",
                'Interest %': f"{(total_interest/P)*100:.1f}%"
            })

        comparison_df = pd.DataFrame(options_data)
        st.dataframe(comparison_df, use_container_width=True)

    # Affordability Calculator
    st.subheader("💰 Loan Affordability Calculator")

    col1, col2 = st.columns(2)
    with col1:
        monthly_income = st.number_input("Monthly Income:", value=50000.0)
        existing_emis = st.number_input("Existing EMIs:", value=0.0)
        other_expenses = st.number_input("Other Monthly Expenses:", value=20000.0)

    with col2:
        emi_ratio = st.slider("Max EMI as % of Income:", min_value=20, max_value=60, value=40)

        max_affordable_emi = (monthly_income * emi_ratio / 100) - existing_emis
        disposable_income = monthly_income - existing_emis - other_expenses

        st.metric("Max Affordable EMI", f"₹{max_affordable_emi:,.2f}")
        st.metric("Disposable Income", f"₹{disposable_income:,.2f}")

        if max_affordable_emi > 0:
            affordable_loan = (max_affordable_emi * ((1 + R/1200) ** (N*12) - 1)) / (R/1200 * (1 + R/1200) ** (N*12))
            st.metric("Max Loan Amount", f"₹{affordable_loan:,.2f}")

with tab5:
    st.header("📖 Loan Payment Methods Guide")

    st.markdown('''
    ## Understanding Different Loan Repayment Methods

    ### 1. Standard EMI (Equated Monthly Installment)
    - **How it works**: Fixed monthly payments throughout the loan tenure
    - **Pros**: Predictable, easy budgeting, widely available
    - **Cons**: Higher initial burden for young professionals
    - **Best for**: Stable income earners

    ### 2. Step-up EMI
    - **How it works**: Lower EMIs initially, increasing periodically (usually annually)
    - **Pros**: Lower initial financial burden, aligns with salary growth
    - **Cons**: Higher total interest if salary doesn't grow as expected
    - **Best for**: Young professionals expecting salary increases

    ### 3. Step-down EMI
    - **How it works**: Higher EMIs initially, decreasing over time
    - **Pros**: Lower total interest, faster debt clearance
    - **Cons**: Higher initial financial burden
    - **Best for**: High current income, expecting income reduction (pre-retirement)

    ### 4. Interest-Only Payments
    - **How it works**: Pay only interest during initial period, principal later
    - **Pros**: Lower monthly outgo initially
    - **Cons**: No principal reduction, higher total cost
    - **Best for**: Short-term cash flow management

    ### 5. Balloon Payment
    - **How it works**: Lower regular EMIs + large final payment
    - **Pros**: Lower monthly burden
    - **Cons**: Risk of large final payment
    - **Best for**: Business loans, expecting future lump sum

    ### 6. Bullet Repayment
    - **How it works**: Only interest during tenure, entire principal at end
    - **Pros**: Minimal monthly outgo
    - **Cons**: Very high final burden
    - **Best for**: Investment-backed loans, short-term financing

    ## Choosing the Right Method

    **Consider your:**
    - Current income stability
    - Expected income growth
    - Risk tolerance
    - Financial goals
    - Cash flow requirements

    ## Pro Tips

    1. **Use prepayments**: Even small additional payments can significantly reduce interest
    2. **Compare total cost**: Don't just look at monthly EMI
    3. **Plan for contingencies**: Keep emergency fund separate
    4. **Review periodically**: Refinance if better rates available
    5. **Tax benefits**: Consider tax implications (especially for home loans)
    ''')

    # Interactive decision helper
    st.subheader("Payment Method Recommendation")

    col1, col2 = st.columns(2)

    with col1:
        career_stage = st.selectbox("Career Stage:", 
                                  ["Early Career (0-5 years)", "Mid Career (5-15 years)", 
                                   "Senior Career (15-25 years)", "Pre-retirement (25+ years)"])

        income_stability = st.selectbox("Income Stability:", 
                                      ["Very Stable", "Moderately Stable", "Variable", "Uncertain"])

    with col2:
        expected_growth = st.selectbox("Expected Income Growth:", 
                                     ["High (>15% annually)", "Moderate (5-15% annually)", 
                                      "Low (<5% annually)", "Declining"])

        risk_tolerance = st.selectbox("Risk Tolerance:", 
                                    ["High", "Moderate", "Low", "Very Low"])

    # Recommendation logic
    recommendations = []

    if career_stage == "Early Career (0-5 years)" and expected_growth in ["High (>15% annually)", "Moderate (5-15% annually)"]:
        recommendations.append("**Step-up EMI** - Aligns with your expected salary growth")

    if career_stage == "Pre-retirement (25+ years)" and expected_growth == "Declining":
        recommendations.append("**Step-down EMI** - Higher payments now, lower burden later")

    if income_stability == "Very Stable" and risk_tolerance in ["Low", "Very Low"]:
        recommendations.append("**Standard EMI** - Predictable and safe")

    if risk_tolerance == "High" and income_stability != "Uncertain":
        recommendations.append("**Balloon Payment** - Lower monthly burden with planned final payment")

    if not recommendations:
        recommendations.append("**Standard EMI** - Safe and predictable option for your profile")

    st.subheader("Recommended Payment Methods:")
    for rec in recommendations:
        st.markdown(f"- {rec}")

# Footer
st.markdown("---")
st.markdown('''
**Disclaimer:** This calculator provides estimates for planning purposes. 
Actual loan terms may vary based on lender policies, credit score, and other factors.

**Advanced EMI Calculator** - Make informed financial decisions
