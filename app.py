
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Personalized Advanced SIP Calculator", 
    layout="wide",
    page_icon="📈"
)



# Custom CSS for better styling
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
    .user-profile-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #28a745;
    }
    .personalized-section {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return {}

def load_user_profiles():
    """Load user profiles from JSON file"""
    try:
        if os.path.exists(USER_PROFILES_FILE):
            with open(USER_PROFILES_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Error loading user profiles: {e}")
        return {}

def get_user_profile(email):
    """Get specific user profile data"""
    profiles = load_user_profiles()
    return profiles.get(email, {})

def get_investment_suggestions(profile):
    """Get personalized investment suggestions based on user profile"""
    suggestions = {
        'recommended_sip': 5000,
        'investment_duration': 15,
        'expected_return': 12.0,
        'step_up_rate': 5.0,
        'investment_type': 'Equity Mutual Funds'
    }

    if profile:
        # Extract financial data
        personal_info = profile.get('personal_info', {})
        investments = profile.get('investments', {})
        expenses = profile.get('expenses', {})
        retirement_tax = profile.get('retirement_tax', {})
        stock_market = profile.get('stock_market', {})

        # Calculate recommended SIP based on income and expenses
        monthly_income = personal_info.get('monthly_income', 0)
        total_expenses = sum([
            expenses.get('rent_mortgage', 0),
            expenses.get('utilities', 0),
            expenses.get('food_dining', 0),
            expenses.get('transportation', 0),
            expenses.get('entertainment', 0),
            expenses.get('healthcare', 0)
        ])

        # Suggest 20-30% of surplus income for SIP
        surplus = monthly_income - total_expenses
        if surplus > 0:
            suggestions['recommended_sip'] = max(int(surplus * 0.25), investments.get('current_sip', 5000))

        # Set duration based on age and retirement plans
        age = personal_info.get('age', 30)
        retirement_age = retirement_tax.get('retirement_age', 60)
        suggestions['investment_duration'] = min(max(retirement_age - age, 5), 40)

        # Adjust returns based on risk tolerance
        risk_tolerance = personal_info.get('risk_tolerance', 'Moderate')
        if risk_tolerance == 'Conservative':
            suggestions['expected_return'] = 8.0
            suggestions['investment_type'] = 'Hybrid Funds'
        elif risk_tolerance == 'Aggressive':
            suggestions['expected_return'] = 15.0
            suggestions['investment_type'] = 'Equity Mutual Funds'
        else:
            suggestions['expected_return'] = 12.0
            suggestions['investment_type'] = 'Equity Mutual Funds'

        # Set step-up rate based on experience
        experience = investments.get('experience', 'Beginner')
        if 'Advanced' in experience or 'Expert' in experience:
            suggestions['step_up_rate'] = 10.0
        elif 'Intermediate' in experience:
            suggestions['step_up_rate'] = 7.5
        else:
            suggestions['step_up_rate'] = 5.0

    return suggestions

def display_user_profile_summary(profile, user_email):
    """Display user profile summary"""
    if profile:
        st.markdown('<div class="user-profile-card">', unsafe_allow_html=True)
        st.markdown("### 👤 Your Financial Profile")

        personal_info = profile.get('personal_info', {})
        investments = profile.get('investments', {})
        expenses = profile.get('expenses', {})

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 Monthly Income", f"₹{personal_info.get('monthly_income', 0):,}")
            st.metric("🎯 Current SIP", f"₹{investments.get('current_sip', 0):,}")

        with col2:
            st.metric("💰 Current Savings", f"₹{personal_info.get('current_savings', 0):,}")
            st.metric("📈 Risk Tolerance", personal_info.get('risk_tolerance', 'Not Set'))

        with col3:
            total_expenses = sum([
                expenses.get('rent_mortgage', 0),
                expenses.get('utilities', 0),
                expenses.get('food_dining', 0),
                expenses.get('transportation', 0),
                expenses.get('entertainment', 0),
                expenses.get('healthcare', 0)
            ])
            st.metric("💳 Monthly Expenses", f"₹{total_expenses:,}")
            st.metric("🎓 Experience", investments.get('experience', 'Not Set'))

        with col4:
            surplus = personal_info.get('monthly_income', 0) - total_expenses
            st.metric("💡 Surplus Income", f"₹{surplus:,}")
            st.metric("🎯 Financial Goal", personal_info.get('financial_goal', 'Not Set'))

        st.markdown('</div>', unsafe_allow_html=True)

        # Display preferred investment types
        preferred_types = investments.get('preferred_types', [])
        if preferred_types:
            st.markdown(f"**Preferred Investment Types:** {', '.join(preferred_types)}")

def calculate_sip_with_stepup(monthly_investment, annual_rate, years, step_up_rate=0, inflation_rate=0):
    """Enhanced SIP calculator with step-up and inflation adjustment"""
    monthly_rate = annual_rate / (100 * 12)
    total_invested = 0
    future_value = 0
    yearly_data = []
    current_monthly = monthly_investment

    for year in range(1, years + 1):
        # Calculate for this year
        year_invested = current_monthly * 12
        total_invested += year_invested

        # Calculate future value for this year's contributions
        remaining_years = years - year + 1
        months_remaining = remaining_years * 12

        if monthly_rate > 0:
            year_fv = current_monthly * (((1 + monthly_rate) ** 12 - 1) / monthly_rate) * (1 + monthly_rate) ** (months_remaining - 12)
        else:
            year_fv = current_monthly * 12 * remaining_years

        future_value += year_fv

        # Calculate inflation-adjusted values
        real_value = future_value / ((1 + inflation_rate/100) ** year) if inflation_rate > 0 else future_value

        yearly_data.append({
            'Year': year,
            'Monthly SIP': current_monthly,
            'Yearly Investment': year_invested,
            'Cumulative Investment': total_invested,
            'Future Value': future_value,
            'Real Value': real_value
        })

        # Apply step-up for next year
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
    """Create pie chart for investment breakdown"""
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
    """Create line chart showing growth over time"""
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

def display_personalized_insights(profile, result, monthly_investment, years):
    """Display personalized insights based on user profile"""
    if not profile:
        return

    st.markdown('<div class="personalized-section">', unsafe_allow_html=True)
    st.markdown("### 🎯 Personalized Financial Insights")

    personal_info = profile.get('personal_info', {})
    retirement_tax = profile.get('retirement_tax', {})
    expenses = profile.get('expenses', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💼 Career & Income Analysis")
        monthly_income = personal_info.get('monthly_income', 0)
        sip_percentage = (monthly_investment / monthly_income * 100) if monthly_income > 0 else 0

        st.markdown(f"""
        - **SIP as % of Income:** {sip_percentage:.1f}%
        - **Recommended:** 15-25% of income
        - **Current Status:** {"✅ Good" if sip_percentage >= 15 else "⚠️ Consider increasing"}
        - **Investment Horizon:** {years} years
        """)

        # Retirement planning
        age = personal_info.get('age', 30)
        retirement_age = retirement_tax.get('retirement_age', 60)
        years_to_retirement = retirement_age - age

        st.markdown("#### 🎯 Retirement Planning")
        target_corpus = retirement_tax.get('retirement_corpus', 100) * 100000  # Convert lakhs to rupees
        st.markdown(f"""
        - **Years to Retirement:** {years_to_retirement}
        - **Target Corpus:** ₹{target_corpus:,}
        - **Current Path:** ₹{result['future_value']:,}
        - **Gap:** ₹{max(0, target_corpus - result['future_value']):,}
        """)

    with col2:
        st.markdown("#### 📊 Investment Optimization")
        total_expenses = sum(expenses.values()) if expenses else 0
        surplus = monthly_income - total_expenses

        st.markdown(f"""
        - **Monthly Surplus:** ₹{surplus:,}
        - **Current SIP Allocation:** {(monthly_investment/surplus*100) if surplus > 0 else 0:.1f}% of surplus
        - **Optimization Scope:** ₹{max(0, surplus * 0.4 - monthly_investment):,}
        """)

        # Tax planning
        tax_bracket = retirement_tax.get('tax_bracket', '')
        annual_tax_saving = retirement_tax.get('annual_tax_saving', 0)

        st.markdown("#### 💰 Tax Optimization")
        st.markdown(f"""
        - **Tax Bracket:** {tax_bracket}
        - **Current Tax Saving:** ₹{annual_tax_saving:,}
        - **ELSS Potential:** ₹{monthly_investment * 12:,}/year
        - **Tax Benefit:** Up to ₹46,800/year (if 31% bracket)
        """)

    st.markdown('</div>', unsafe_allow_html=True)

# Main Streamlit App
def main():
    st.markdown('<h1 class="main-header">📈 Personalized Advanced SIP Calculator</h1>', unsafe_allow_html=True)
    st.markdown("**Powered by your financial profile - Get personalized SIP recommendations**")

    # Display user profile summary
    

    # Sidebar for inputs
    with st.sidebar:
        st.markdown("## 📋 Investment Parameters")

        # Show personalized recommendations
        if user_profile:
            st.markdown("### 🤖 AI Recommendations")
            st.info(f"""
            **Recommended Monthly SIP:** ₹{suggestions['recommended_sip']:,}

            **Duration:** {suggestions['investment_duration']} years

            **Expected Return:** {suggestions['expected_return']}%

            **Step-up Rate:** {suggestions['step_up_rate']}%
            """)

        # Calculation type
        calc_type = st.selectbox(
            "Calculation Type",
            ["Regular SIP", "Step-up SIP", "Goal Planning", "Personalized Recommendation"]
        )

        if calc_type == "Personalized Recommendation" and user_profile:
            # Use AI suggestions
            monthly_investment = suggestions['recommended_sip']
            years = suggestions['investment_duration']
            annual_rate = suggestions['expected_return']
            step_up_rate = suggestions['step_up_rate']
            investment_type = suggestions['investment_type']

            st.success("Using personalized recommendations based on your profile!")

        elif calc_type == "Goal Planning":
            target_amount = st.number_input(
                "Target Amount (₹)", 
                min_value=100000, 
                value=int(user_profile.get('retirement_tax', {}).get('retirement_corpus', 100) * 100000) if user_profile else 1000000,
                step=50000
            )
            years = st.number_input(
                "Time to Goal (Years)", 
                min_value=1, 
                max_value=40, 
                value=suggestions['investment_duration'], 
                step=1
            )
            annual_rate = st.slider(
                "Expected Annual Return (%)", 
                min_value=5.0, 
                max_value=20.0, 
                value=suggestions['expected_return'], 
                step=0.5
            )
            # Calculate required SIP
            monthly_rate = annual_rate / (100 * 12)
            total_months = years * 12
            if monthly_rate > 0:
                future_value_factor = ((1 + monthly_rate) ** total_months - 1) / monthly_rate
                required_sip = target_amount / (future_value_factor * (1 + monthly_rate))
            else:
                required_sip = target_amount / total_months
            monthly_investment = required_sip
            st.success(f"Required Monthly SIP: ₹{required_sip:,.0f}")
            step_up_rate = suggestions['step_up_rate']
            investment_type = suggestions['investment_type']

        else:
            # Regular inputs with suggestions as defaults
            monthly_investment = st.number_input(
                "Monthly SIP Amount (₹)", 
                min_value=500, 
                value=suggestions['recommended_sip'],
                step=500
            )
            years = st.number_input(
                "Investment Duration (Years)", 
                min_value=1, 
                max_value=40, 
                value=suggestions['investment_duration'], 
                step=1
            )
            annual_rate = st.slider(
                "Expected Annual Return (%)", 
                min_value=5.0, 
                max_value=20.0, 
                value=suggestions['expected_return'], 
                step=0.5
            )
            step_up_rate = st.slider(
                "Annual Step-up Rate (%)", 
                min_value=0.0, 
                max_value=15.0, 
                value=suggestions['step_up_rate'] if calc_type == "Step-up SIP" else 0.0, 
                step=0.5
            )
            investment_type = st.selectbox(
                "Investment Type",
                ["Equity Mutual Funds", "Hybrid Funds", "Debt Funds", "ELSS", "Index Funds"],
                index=0 if suggestions['investment_type'] == "Equity Mutual Funds" else 1
            )

        st.markdown("### Advanced Options")
        inflation_rate = st.slider(
            "Expected Inflation Rate (%)", 
            min_value=0.0, 
            max_value=10.0, 
            value=6.0, 
            step=0.5
        )

    # Calculate button
    if st.button("🧮 Calculate Personalized SIP", type="primary"):
        result = calculate_sip_with_stepup(
            monthly_investment, annual_rate, years, step_up_rate, inflation_rate
        )

        # Display results
        st.markdown('<h2 class="sub-header">📈 Investment Results</h2>', unsafe_allow_html=True)

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Invested", f"₹{result['total_invested']:,.0f}")
        with col2:
            st.metric(
                "🎯 Future Value", 
                f"₹{result['future_value']:,.0f}",
                delta=f"+{((result['future_value']/result['total_invested'])*100-100):.1f}%"
            )
        with col3:
            st.metric(
                "📈 Total Returns", 
                f"₹{result['total_returns']:,.0f}",
                delta=f"{result['effective_rate']:.1f}% annually"
            )
        with col4:
            st.metric(
                "💵 Real Value", 
                f"₹{result['inflation_adjusted_value']:,.0f}",
                delta=f"After {inflation_rate}% inflation"
            )

        # Personalized insights
        if user_profile:
            display_personalized_insights(user_profile, result, monthly_investment, years)

        # Charts section
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
            - **Total Months:** {years * 12} months
            - **Growth Multiple:** {result['future_value']/result['total_invested']:.1f}x
            - **Effective Return:** {result['effective_rate']:.1f}% p.a.
            """)

        # Growth chart
        growth_fig = create_growth_chart(result['yearly_data'])
        st.plotly_chart(growth_fig, use_container_width=True)

        # Detailed breakdown
        st.markdown('<h2 class="sub-header">📋 Year-wise Breakdown</h2>', unsafe_allow_html=True)
        df = pd.DataFrame(result['yearly_data'])
        # Format for display
        df_display = df.copy()
        for col in ['Monthly SIP', 'Yearly Investment', 'Cumulative Investment', 'Future Value', 'Real Value']:
            df_display[col] = df_display[col].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(df_display, use_container_width=True)

        # Insights
        st.markdown('<h2 class="sub-header">💡 Key Insights</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Financial Impact")
            st.markdown(f"""
            - Investment grows **{result['future_value']/result['total_invested']:.1f}x** in {years} years
            - Total returns: **₹{result['total_returns']:,.0f}**
            - Effective annual return: **{result['effective_rate']:.1f}%**
            - Time to double: **{70/annual_rate:.1f} years**
            """)

        with col2:
            st.markdown("### 📊 Inflation Impact")
            inflation_loss = result['future_value'] - result['inflation_adjusted_value']
            st.markdown(f"""
            - Nominal value: **₹{result['future_value']:,.0f}**
            - Real value: **₹{result['inflation_adjusted_value']:,.0f}**
            - Inflation impact: **₹{inflation_loss:,.0f}**
            - Real growth: **{(result['inflation_adjusted_value']/result['total_invested']):.1f}x**
            """)

        # Personalized Recommendations
        st.markdown('<h2 class="sub-header">🎯 Personalized Recommendations</h2>', unsafe_allow_html=True)
        recommendations = []

        if user_profile:
            personal_info = user_profile.get('personal_info', {})
            monthly_income = personal_info.get('monthly_income', 0)
            sip_percentage = (monthly_investment / monthly_income * 100) if monthly_income > 0 else 0

            if sip_percentage < 15:
                recommendations.append("📈 Increase SIP to 15-25% of income for better wealth creation")
            if step_up_rate == 0:
                recommendations.append("🔄 Consider Step-up SIP to beat inflation and salary increments")
            if personal_info.get('risk_tolerance') == 'Conservative' and annual_rate > 10:
                recommendations.append("⚖️ Consider balanced funds matching your risk profile")
            if investment_type == "ELSS":
                recommendations.append("💼 Tax benefit: Up to ₹1.5L deduction under 80C")
        else:
            if step_up_rate == 0:
                recommendations.append("🔄 Consider Step-up SIP to beat inflation")
            if annual_rate < 10:
                recommendations.append("⚡ Consider equity funds for higher growth")
            if years > 15:
                recommendations.append("🎯 Long horizon perfect for equity investments")

        for rec in recommendations:
            st.markdown(f"- {rec}")

        # Scenario analysis
        with st.expander("🔬 Scenario Analysis"):
            st.markdown("### Different Investment Amounts:")
            scenarios = []
            for mult in [0.5, 1, 1.5, 2]:
                amount = monthly_investment * mult
                scenario_result = calculate_sip_with_stepup(amount, annual_rate, years, step_up_rate, inflation_rate)
                scenarios.append({
                    'Monthly SIP': f"₹{amount:,.0f}",
                    'Future Value': f"₹{scenario_result['future_value']:,.0f}",
                    'Returns': f"₹{scenario_result['total_returns']:,.0f}"
                })
            st.table(pd.DataFrame(scenarios))

    # Show available profiles for testing
    if st.checkbox("🔍 Show Available User Profiles (for testing)"):
        profiles = load_user_profiles()
        if profiles:
            st.markdown("### Available User Profiles:")
            for email in profiles.keys():
                profile = profiles[email]
                personal_info = profile.get('personal_info', {})
                st.markdown(f"""
                **{email}**
                - Age: {personal_info.get('age', 'N/A')}
                - Income: ₹{personal_info.get('monthly_income', 0):,}
                - Risk: {personal_info.get('risk_tolerance', 'N/A')}
                - Current SIP: ₹{profile.get('investments', {}).get('current_sip', 0):,}
                """)
        else:
            st.info("No user profiles found. Please register through the login page first.")

    # Information section
    st.markdown("---")
    st.markdown("### ℹ️ About This Personalized Calculator")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Personalized Features:**
        - Profile-based recommendations
        - AI-suggested parameters
        - Income-based SIP calculation
        - Risk-adjusted returns
        - Goal-based planning
        """)

    with col2:
        st.markdown("""
        **Data Integration:**
        - User financial profile
        - Expense analysis
        - Retirement planning
        - Tax optimization
        - Investment preferences
        """)

    with col3:
        st.markdown("""
        **Enhanced Analytics:**
        - Personalized insights
        - Career-based projections
        - Surplus income analysis
        - Goal gap analysis
        - Tax-efficient planning
        """)

if __name__ == "__main__":
    main()
