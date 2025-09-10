import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Retirement Planner - India",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with Indian theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF9933;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #138808;
        margin-bottom: 1rem;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #FF9933;
    }
    .result-box {
        background-color: #e6f3ff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #138808;
    }
    .positive {
        color: #138808;
        font-weight: bold;
    }
    .warning {
        color: #FF0000;
        font-weight: bold;
    }
    .stButton button {
        background-color: #FF9933;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<h1 class="main-header">💰 Indian Retirement Planner</h1>', unsafe_allow_html=True)
st.write("Plan your retirement with this interactive calculator. Adjust the inputs in the sidebar to see how different factors affect your retirement savings.")

# Sidebar for user inputs
with st.sidebar:
    st.header("Personal Information")
    
    # User inputs
    current_age = st.slider("Current Age", 20, 70, 35)
    retirement_age = st.slider("Desired Retirement Age", 50, 80, 60)
    life_expectancy = st.slider("Life Expectancy", 75, 100, 85)
    
    st.header("Financial Information")
    
    current_savings = st.number_input("Current Retirement Savings (₹)", min_value=0, value=500000, step=10000)
    annual_contribution = st.number_input("Annual Contribution (₹)", min_value=0, value=100000, step=10000)
    annual_return = st.slider("Expected Annual Return (%)", 1.0, 15.0, 8.0, step=0.5)
    inflation_rate = st.slider("Expected Inflation Rate (%)", 0.5, 10.0, 5.5, step=0.1)
    
    st.header("Retirement Income")
    
    desired_income = st.number_input("Desired Annual Retirement Income (Today's ₹)", min_value=0, value=600000, step=50000)
    pension_income = st.number_input("Expected Annual Pension Income (₹)", min_value=0, value=0, step=10000)
    provident_fund = st.number_input("Expected Annual Provident Fund Income (₹)", min_value=0, value=120000, step=10000)
    
    # Calculate button
    calculate = st.button("Calculate Retirement Plan", type="primary")

# Format numbers in Indian numbering system
def format_inr(amount):
    amount = float(amount)
    if amount >= 10000000:
        return f'₹{amount/10000000:.2f} Crore'
    elif amount >= 100000:
        return f'₹{amount/100000:.2f} Lakh'
    else:
        return f'₹{amount:,.0f}'

# Main calculation function
def calculate_retirement(current_age, retirement_age, life_expectancy, current_savings, 
                         annual_contribution, annual_return, inflation_rate, desired_income, 
                         pension_income, provident_fund):
    
    # Calculate years until retirement and retirement duration
    years_to_retirement = retirement_age - current_age
    retirement_duration = life_expectancy - retirement_age
    
    # Initialize lists for results
    years = []
    ages = []
    savings = []
    contributions = []
    growth = []
    inflation_adjusted_savings = []
    retirement_income_needed = []
    
    # Calculate savings growth until retirement
    savings_balance = current_savings
    for year in range(years_to_retirement + 1):
        age = current_age + year
        years.append(year)
        ages.append(age)
        
        if year == 0:
            contributions.append(0)
            growth.append(0)
        else:
            # Calculate investment growth
            investment_growth = savings_balance * (annual_return / 100)
            growth.append(investment_growth)
            
            # Add contribution at the beginning of the year
            savings_balance += annual_contribution
            contributions.append(annual_contribution)
            
            # Add investment growth
            savings_balance += investment_growth
        
        savings.append(savings_balance)
        
        # Calculate inflation-adjusted savings
        inflation_adjusted = savings_balance / ((1 + inflation_rate/100) ** year)
        inflation_adjusted_savings.append(inflation_adjusted)
        
        # Calculate retirement income needed in future rupees
        future_income_needed = desired_income * ((1 + inflation_rate/100) ** year)
        retirement_income_needed.append(future_income_needed)
    
    # Calculate retirement phase
    retirement_savings = savings_balance
    annual_retirement_income = pension_income + provident_fund
    shortfall = retirement_income_needed[-1] - annual_retirement_income
    
    # Calculate if savings will last through retirement
    savings_last = True
    retirement_years = []
    retirement_ages = []
    retirement_savings_balance = []
    retirement_withdrawals = []
    
    for year in range(retirement_duration + 1):
        retirement_year = year
        age = retirement_age + year
        retirement_years.append(retirement_year)
        retirement_ages.append(age)
        
        if year == 0:
            balance = retirement_savings
            withdrawal = 0
        else:
            # Calculate investment growth
            investment_growth = balance * (annual_return / 100)
            
            # Withdraw shortfall amount
            withdrawal = shortfall
            balance -= withdrawal
            balance += investment_growth
            
            # Check if savings are depleted
            if balance < 0:
                balance = 0
                savings_last = False
        
        retirement_savings_balance.append(balance)
        retirement_withdrawals.append(withdrawal)
    
    # Create results dictionary
    results = {
        'years': years,
        'ages': ages,
        'savings': savings,
        'contributions': contributions,
        'growth': growth,
        'inflation_adjusted_savings': inflation_adjusted_savings,
        'retirement_income_needed': retirement_income_needed,
        'retirement_years': retirement_years,
        'retirement_ages': retirement_ages,
        'retirement_savings_balance': retirement_savings_balance,
        'retirement_withdrawals': retirement_withdrawals,
        'retirement_savings': retirement_savings,
        'shortfall': shortfall,
        'savings_last': savings_last,
        'retirement_duration': retirement_duration
    }
    
    return results

# Display results if calculate button is clicked
if calculate:
    # Calculate retirement plan
    results = calculate_retirement(
        current_age, retirement_age, life_expectancy, current_savings,
        annual_contribution, annual_return, inflation_rate, desired_income,
        pension_income, provident_fund
    )
    
    # Display summary
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown(f'<h2 class="sub-header">Retirement Plan Summary</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Years Until Retirement", f"{retirement_age - current_age}")
        st.metric("Projected Retirement Savings", format_inr(results['retirement_savings']))
    
    with col2:
        st.metric("Annual Shortfall in Retirement", format_inr(results['shortfall']))
        st.metric("Retirement Duration", f"{results['retirement_duration']} years")
    
    with col3:
        status = "✅ Sufficient" if results['savings_last'] else "❌ Insufficient"
        st.metric("Savings Status", status)
        st.metric("Monthly Shortfall in Retirement", format_inr(results['shortfall']/12))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Savings Growth", "Retirement Projection", "Detailed Analysis"])
    
    with tab1:
        # Create savings growth chart using Streamlit's native line chart
        st.subheader("Savings Growth Until Retirement")
        
        df_savings = pd.DataFrame({
            'Age': results['ages'],
            'Savings': results['savings'],
            'Inflation Adjusted Savings': results['inflation_adjusted_savings']
        })
        
        st.line_chart(df_savings.set_index('Age'))
    
    with tab2:
        # Create retirement projection chart
        st.subheader("Retirement Savings Projection")
        
        df_retirement = pd.DataFrame({
            'Age': results['retirement_ages'],
            'Savings Balance': results['retirement_savings_balance']
        })
        
        st.line_chart(df_retirement.set_index('Age'))
        
        # Display warning if savings are insufficient
        if not results['savings_last']:
            st.error("*Warning*: Your savings may not last through your retirement. Consider increasing your contributions, working longer, or adjusting your retirement income expectations.")
    
    with tab3:
        # Detailed analysis
        st.subheader("Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Pre-Retirement Projection")
            df_pre = pd.DataFrame({
                'Age': results['ages'],
                'Savings (₹)': results['savings'],
                'Contributions (₹)': results['contributions'],
                'Investment Growth (₹)': results['growth']
            })
            df_pre['Savings (₹)'] = df_pre['Savings (₹)'].apply(lambda x: format_inr(x))
            df_pre['Contributions (₹)'] = df_pre['Contributions (₹)'].apply(lambda x: format_inr(x))
            df_pre['Investment Growth (₹)'] = df_pre['Investment Growth (₹)'].apply(lambda x: format_inr(x))
            st.dataframe(df_pre.set_index('Age'), use_container_width=True)
        
        with col2:
            st.markdown("##### Post-Retirement Projection")
            df_post = pd.DataFrame({
                'Age': results['retirement_ages'],
                'Savings Balance (₹)': results['retirement_savings_balance'],
                'Annual Withdrawal (₹)': results['retirement_withdrawals']
            })
            df_post['Savings Balance (₹)'] = df_post['Savings Balance (₹)'].apply(lambda x: format_inr(x))
            df_post['Annual Withdrawal (₹)'] = df_post['Annual Withdrawal (₹)'].apply(lambda x: format_inr(x))
            st.dataframe(df_post.set_index('Age'), use_container_width=True)
    
    # Recommendations section
    st.markdown("---")
    st.markdown('<h2 class="sub-header">Recommendations</h2>', unsafe_allow_html=True)
    
    if results['savings_last']:
        st.success("""
        - Your current plan appears to be on track for retirement
        - Continue with your current savings strategy
        - Consider investing in a mix of equity and debt instruments
        - Explore tax-saving investment options under Section 80C
        - Consider periodically reviewing your plan as your circumstances change
        """)
    else:
        st.warning("""
        - *Increase your savings rate*: Try to save more each year
        - *Consider working longer*: Delaying retirement by a few years can significantly improve your financial security
        - *Adjust your retirement expectations*: You may need to reduce your desired retirement income
        - *Review your investment strategy*: Ensure your portfolio is appropriately allocated for your age and risk tolerance
        - *Consider additional income sources*: Part-time work during retirement could help bridge the gap
        - *Explore higher-yielding investments*: Consider increasing equity exposure for higher long-term returns
        """)
    
else:
    # Show instructions before calculation
    st.info("""
    ### How to Use This Calculator
    1. Adjust the input parameters in the sidebar to match your situation
    2. Click the 'Calculate Retirement Plan' button to see your personalized results
    3. Explore the different tabs to see detailed projections and analysis
    4. Use the recommendations to improve your retirement plan
    """)
    
    # Placeholder for demonstration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Why Plan for Retirement?")
        st.write("""
        - Retirement can last 20-30 years or more in India
        - EPF/PPF may not provide enough income for comfortable retirement
        - Healthcare costs tend to increase with age
        - Inflation erodes purchasing power over time
        - Starting early gives your investments more time to grow
        - Family support systems are changing in modern India
        """)
    
    with col2:
        st.subheader("Key Retirement Planning Tips for India")
        st.write("""
        - Start saving as early as possible
        - Maximize contributions to EPF, PPF, and NPS
        - Diversify your investments across asset classes
        - Consider equity investments for long-term growth
        - Regularly review and adjust your plan
        - Consider tax implications of your investments
        - Account for healthcare costs in retirement
        """)
    
    # Sample chart placeholder using Streamlit's native chart
    st.subheader("The Power of Compound Interest")
    
 # Sample data for demonstration
years = list(range(65))
savings_early = [100000 * (1.08)**y for y in years]
savings_late = [0] * 25 + [100000 * (1.08)**(y-25) for y in range(25, 65)]

df_compound = pd.DataFrame({
    'Age': [25 + y for y in years],
    'Starting at 25': savings_early,
    'Starting at 50': savings_late
})

st.line_chart(df_compound.set_index('Age'))


# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>This retirement calculator is for educational purposes only. Actual results may vary based on market conditions and personal circumstances. Consult with a financial advisor for personalized advice.</p>", unsafe_allow_html=True)
