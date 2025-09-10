import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Income Tax Calculator - New Regime",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def calculate_new_regime_tax(total_income, financial_year="2024-25", is_salaried=True):
    """
    Calculate income tax under the new tax regime for India
    """

    # Define tax slabs for different financial years
    if financial_year == "2024-25":
        tax_slabs = [
            (300000, 0.0),      # Up to 3 lakh - 0%
            (700000, 0.05),     # 3-7 lakh - 5%
            (1000000, 0.10),    # 7-10 lakh - 10%
            (1200000, 0.15),    # 10-12 lakh - 15%
            (1500000, 0.20),    # 12-15 lakh - 20%
            (float('inf'), 0.30) # Above 15 lakh - 30%
        ]
        basic_exemption = 300000
        rebate_limit = 700000
        rebate_amount = 25000
        standard_deduction = 75000 if is_salaried else 0

    elif financial_year == "2025-26":
        tax_slabs = [
            (400000, 0.0),      # Up to 4 lakh - 0%
            (800000, 0.05),     # 4-8 lakh - 5%
            (1200000, 0.10),    # 8-12 lakh - 10%
            (1600000, 0.15),    # 12-16 lakh - 15%
            (2000000, 0.20),    # 16-20 lakh - 20%
            (2400000, 0.25),    # 20-24 lakh - 25%
            (float('inf'), 0.30) # Above 24 lakh - 30%
        ]
        basic_exemption = 400000
        rebate_limit = 1200000
        rebate_amount = 60000
        standard_deduction = 75000 if is_salaried else 0

    # Calculate taxable income after standard deduction
    taxable_income = max(0, total_income - standard_deduction)

    # Calculate basic tax
    basic_tax = 0
    remaining_income = taxable_income
    tax_breakdown = []

    for i, (slab_limit, rate) in enumerate(tax_slabs):
        if remaining_income <= 0:
            break

        if i == 0:
            taxable_in_slab = min(remaining_income, slab_limit)
            slab_desc = f"Up to ₹{slab_limit:,}"
        else:
            prev_limit = tax_slabs[i-1][0]
            if slab_limit == float('inf'):
                taxable_in_slab = remaining_income
                slab_desc = f"Above ₹{prev_limit:,}"
            else:
                taxable_in_slab = min(remaining_income, slab_limit - prev_limit)
                slab_desc = f"₹{prev_limit:,} - ₹{slab_limit:,}"

        tax_in_slab = taxable_in_slab * rate
        basic_tax += tax_in_slab

        if taxable_in_slab > 0:
            tax_breakdown.append({
                'Slab': slab_desc,
                'Rate': f"{rate*100:.0f}%",
                'Taxable Amount': f"₹{taxable_in_slab:,.0f}",
                'Tax': f"₹{tax_in_slab:,.0f}"
            })

        remaining_income -= taxable_in_slab

        if remaining_income <= 0:
            break

    # Apply Section 87A rebate
    rebate = 0
    if taxable_income <= rebate_limit:
        rebate = min(basic_tax, rebate_amount)

    tax_after_rebate = basic_tax - rebate

    # Calculate surcharge
    surcharge = 0
    surcharge_rate = 0

    if taxable_income > 5000000:
        if taxable_income <= 10000000:
            surcharge_rate = 0.10
        elif taxable_income <= 20000000:
            surcharge_rate = 0.15
        elif taxable_income <= 50000000:
            surcharge_rate = 0.25
        else:
            surcharge_rate = 0.25

        surcharge = tax_after_rebate * surcharge_rate

    tax_after_surcharge = tax_after_rebate + surcharge

    # Calculate Health and Education Cess
    cess_rate = 0.04
    cess = tax_after_surcharge * cess_rate

    # Total tax liability
    total_tax = tax_after_surcharge + cess

    # Calculate effective tax rate
    effective_tax_rate = (total_tax / total_income * 100) if total_income > 0 else 0

    return {
        'total_income': total_income,
        'standard_deduction': standard_deduction,
        'taxable_income': taxable_income,
        'basic_tax': round(basic_tax, 2),
        'rebate_87a': round(rebate, 2),
        'tax_after_rebate': round(tax_after_rebate, 2),
        'surcharge_rate': surcharge_rate * 100,
        'surcharge': round(surcharge, 2),
        'tax_after_surcharge': round(tax_after_surcharge, 2),
        'cess_rate': cess_rate * 100,
        'cess': round(cess, 2),
        'total_tax_liability': round(total_tax, 2),
        'effective_tax_rate': round(effective_tax_rate, 2),
        'net_income_after_tax': round(total_income - total_tax, 2),
        'financial_year': financial_year,
        'tax_breakdown': tax_breakdown
    }

def create_tax_breakdown_chart(result):
    """Create a pie chart showing tax breakdown"""
    labels = []
    values = []

    if result['rebate_87a'] > 0:
        net_tax = result['basic_tax'] - result['rebate_87a']
        if net_tax > 0:
            labels.append(f"Income Tax (After Rebate)")
            values.append(net_tax)
    else:
        if result['basic_tax'] > 0:
            labels.append("Income Tax")
            values.append(result['basic_tax'])

    if result['surcharge'] > 0:
        labels.append("Surcharge")
        values.append(result['surcharge'])

    if result['cess'] > 0:
        labels.append("Health & Education Cess")
        values.append(result['cess'])

    labels.append("Net Income After Tax")
    values.append(result['net_income_after_tax'])

    fig = px.pie(
        values=values, 
        names=labels, 
        title=f"Income Distribution - FY {result['financial_year']}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)

    return fig

def create_comparison_chart(income, is_salaried):
    """Create comparison chart between financial years"""
    result_2024 = calculate_new_regime_tax(income, "2024-25", is_salaried)
    result_2025 = calculate_new_regime_tax(income, "2025-26", is_salaried)

    categories = ['Basic Tax', 'After Rebate', 'After Surcharge', 'Total Tax']
    fy_2024_values = [result_2024['basic_tax'], result_2024['tax_after_rebate'], 
                      result_2024['tax_after_surcharge'], result_2024['total_tax_liability']]
    fy_2025_values = [result_2025['basic_tax'], result_2025['tax_after_rebate'],
                      result_2025['tax_after_surcharge'], result_2025['total_tax_liability']]

    fig = go.Figure(data=[
        go.Bar(name='FY 2024-25', x=categories, y=fy_2024_values, marker_color='lightblue'),
        go.Bar(name='FY 2025-26', x=categories, y=fy_2025_values, marker_color='lightgreen')
    ])

    fig.update_layout(
        barmode='group',
        title='Tax Comparison: FY 2024-25 vs FY 2025-26',
        xaxis_title='Tax Components',
        yaxis_title='Amount (₹)',
        height=400
    )

    return fig, result_2024, result_2025

def create_slab_wise_chart(result):
    """Create a bar chart showing slab-wise tax calculation"""
    if not result['tax_breakdown']:
        return None

    df = pd.DataFrame(result['tax_breakdown'])
    df['Tax_Amount'] = df['Tax'].str.replace('₹', '').str.replace(',', '').astype(float)

    fig = px.bar(
        df, 
        x='Slab', 
        y='Tax_Amount',
        title=f"Slab-wise Tax Calculation - FY {result['financial_year']}",
        labels={'Tax_Amount': 'Tax Amount (₹)', 'Slab': 'Income Slab'},
        color='Rate',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(height=400, xaxis_tickangle=-45)

    return fig

# Main Streamlit App
def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .highlight {
        background-color: #e6f3ff;
        padding: 1rem;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<h1 class="main-header">💰 Income Tax Calculator - New Regime</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">Calculate your income tax under India's New Tax Regime for FY 2024-25 & 2025-26</p>', unsafe_allow_html=True)

    # Sidebar for inputs
    st.sidebar.markdown("## 📊 Tax Calculation Inputs")

    # Input fields
    annual_income = st.sidebar.number_input(
        "Annual Income (₹)", 
        min_value=0, 
        value=1200000, 
        step=50000,
        help="Enter your total annual income in Indian Rupees"
    )

    financial_year = st.sidebar.selectbox(
        "Financial Year",
        ["2024-25", "2025-26"],
        index=1,
        help="Select the financial year for tax calculation"
    )

    is_salaried = st.sidebar.checkbox(
        "Salaried Employee", 
        value=True,
        help="Check if you are a salaried employee (eligible for ₹75,000 standard deduction)"
    )

    # Calculate tax
    result = calculate_new_regime_tax(annual_income, financial_year, is_salaried)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'<h2 class="sub-header">Tax Calculation Results - FY {financial_year}</h2>', unsafe_allow_html=True)

        # Key metrics
        col1_1, col1_2, col1_3, col1_4 = st.columns(4)

        with col1_1:
            st.metric(
                "Total Tax Liability",
                f"₹{result['total_tax_liability']:,.0f}",
                delta=None
            )

        with col1_2:
            st.metric(
                "Effective Tax Rate",
                f"{result['effective_tax_rate']:.2f}%",
                delta=None
            )

        with col1_3:
            st.metric(
                "Net Income",
                f"₹{result['net_income_after_tax']:,.0f}",
                delta=None
            )

        with col1_4:
            monthly_net = result['net_income_after_tax'] / 12
            st.metric(
                "Monthly Take-Home",
                f"₹{monthly_net:,.0f}",
                delta=None
            )

    with col2:
        # Tax breakdown pie chart
        if result['total_tax_liability'] > 0:
            fig_pie = create_tax_breakdown_chart(result)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.success("🎉 No Tax Liability!")
            st.balloons()

    # Detailed breakdown
    st.markdown('<h3 class="sub-header">📋 Detailed Tax Breakdown</h3>', unsafe_allow_html=True)

    # Create detailed breakdown table
    breakdown_data = {
        'Component': [
            'Gross Annual Income',
            'Less: Standard Deduction',
            'Taxable Income',
            'Basic Income Tax',
            'Less: Rebate u/s 87A',
            'Tax After Rebate',
            'Add: Surcharge',
            'Tax After Surcharge', 
            'Add: Health & Education Cess (4%)',
            'Total Tax Liability'
        ],
        'Amount (₹)': [
            f"{result['total_income']:,.0f}",
            f"{result['standard_deduction']:,.0f}",
            f"{result['taxable_income']:,.0f}",
            f"{result['basic_tax']:,.0f}",
            f"{result['rebate_87a']:,.0f}",
            f"{result['tax_after_rebate']:,.0f}",
            f"{result['surcharge']:,.0f}",
            f"{result['tax_after_surcharge']:,.0f}",
            f"{result['cess']:,.0f}",
            f"{result['total_tax_liability']:,.0f}"
        ]
    }

    breakdown_df = pd.DataFrame(breakdown_data)
    st.table(breakdown_df)

    # Slab-wise breakdown
    if result['tax_breakdown']:
        st.markdown('<h3 class="sub-header">📊 Slab-wise Tax Calculation</h3>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            slab_df = pd.DataFrame(result['tax_breakdown'])
            st.table(slab_df)

        with col2:
            fig_slab = create_slab_wise_chart(result)
            if fig_slab:
                st.plotly_chart(fig_slab, use_container_width=True)

    # Comparison section
    st.markdown('<h2 class="sub-header">🔄 Year-on-Year Comparison</h2>', unsafe_allow_html=True)

    if st.button("Compare FY 2024-25 vs FY 2025-26", type="primary"):
        fig_comparison, result_2024, result_2025 = create_comparison_chart(annual_income, is_salaried)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.plotly_chart(fig_comparison, use_container_width=True)

        with col2:
            savings = result_2024['total_tax_liability'] - result_2025['total_tax_liability']
            if savings > 0:
                st.success(f"💰 Tax Savings in FY 2025-26: ₹{savings:,.0f}")
                st.info(f"📈 Additional monthly take-home: ₹{savings/12:,.0f}")
            elif savings < 0:
                st.warning(f"⚠ Additional tax in FY 2025-26: ₹{abs(savings):,.0f}")
            else:
                st.info("✅ No change in tax liability")

        # Comparison table
        comparison_data = {
            'Component': ['Total Income', 'Taxable Income', 'Basic Tax', 'Rebate u/s 87A', 'Total Tax', 'Effective Rate', 'Net Income'],
            'FY 2024-25': [
                f"₹{result_2024['total_income']:,.0f}",
                f"₹{result_2024['taxable_income']:,.0f}",
                f"₹{result_2024['basic_tax']:,.0f}",
                f"₹{result_2024['rebate_87a']:,.0f}",
                f"₹{result_2024['total_tax_liability']:,.0f}",
                f"{result_2024['effective_tax_rate']:.2f}%",
                f"₹{result_2024['net_income_after_tax']:,.0f}"
            ],
            'FY 2025-26': [
                f"₹{result_2025['total_income']:,.0f}",
                f"₹{result_2025['taxable_income']:,.0f}",
                f"₹{result_2025['basic_tax']:,.0f}",
                f"₹{result_2025['rebate_87a']:,.0f}",
                f"₹{result_2025['total_tax_liability']:,.0f}",
                f"{result_2025['effective_tax_rate']:.2f}%",
                f"₹{result_2025['net_income_after_tax']:,.0f}"
            ],
            'Difference': [
                "₹0",
                "₹0", 
                f"₹{result_2025['basic_tax'] - result_2024['basic_tax']:,.0f}",
                f"₹{result_2025['rebate_87a'] - result_2024['rebate_87a']:,.0f}",
                f"₹{result_2025['total_tax_liability'] - result_2024['total_tax_liability']:,.0f}",
                f"{result_2025['effective_tax_rate'] - result_2024['effective_tax_rate']:+.2f}%",
                f"₹{result_2025['net_income_after_tax'] - result_2024['net_income_after_tax']:,.0f}"
            ]
        }

        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)

    # Tax slabs information
    with st.expander("📚 Tax Slabs Information"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### FY 2024-25 Tax Slabs")
            slabs_2024 = pd.DataFrame({
                'Income Slab': ['Up to ₹3,00,000', '₹3,00,001 - ₹7,00,000', '₹7,00,001 - ₹10,00,000', 
                               '₹10,00,001 - ₹12,00,000', '₹12,00,001 - ₹15,00,000', 'Above ₹15,00,000'],
                'Tax Rate': ['0%', '5%', '10%', '15%', '20%', '30%']
            })
            st.table(slabs_2024)
            st.markdown("*Rebate u/s 87A*: Up to ₹25,000 (for income up to ₹7,00,000)")

        with col2:
            st.markdown("### FY 2025-26 Tax Slabs")
            slabs_2025 = pd.DataFrame({
                'Income Slab': ['Up to ₹4,00,000', '₹4,00,001 - ₹8,00,000', '₹8,00,001 - ₹12,00,000',
                               '₹12,00,001 - ₹16,00,000', '₹16,00,001 - ₹20,00,000', '₹20,00,001 - ₹24,00,000',
                               'Above ₹24,00,000'],
                'Tax Rate': ['0%', '5%', '10%', '15%', '20%', '25%', '30%']
            })
            st.table(slabs_2025)
            st.markdown("*Rebate u/s 87A*: Up to ₹60,000 (for income up to ₹12,00,000)")

    # Key benefits
    st.markdown('<h3 class="sub-header">✨ Key Benefits of New Tax Regime FY 2025-26</h3>', unsafe_allow_html=True)

    benefits = [
        "🎯 *Zero tax* for income up to ₹12,00,000 (including standard deduction)",
        "📈 Higher basic exemption: ₹4,00,000 (vs ₹3,00,000 in FY 2024-25)",
        "💡 New 25% tax slab for ₹20-24 lakh income bracket",
        "🎪 30% tax applies only above ₹24,00,000 (vs ₹15,00,000 earlier)",
        "🔻 Reduced maximum surcharge: 25% (vs 37% in old regime)",
        "💼 Standard deduction: ₹75,000 for salaried employees",
        "🚀 Simplified tax structure with fewer deductions"
    ]

    for benefit in benefits:
        st.markdown(benefit)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    <p>💡 This calculator is based on the New Tax Regime provisions for FY 2024-25 and FY 2025-26</p>
    <p>⚠ For actual tax planning, please consult a qualified tax advisor</p>
    </div>
    """, unsafe_allow_html=True)

if _name_ == "_main_":
    main()
