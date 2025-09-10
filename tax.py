import streamlit as st
import math

# Set page configuration
st.set_page_config(
    page_title="FinScore - Financial Health Assessment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary: #2c3e50;
        --secondary: #3498db;
        --accent: #e74c3c;
        --light: #ecf0f1;
        --dark: #2c3e50;
        --success: #2ecc71;
        --warning: #f39c12;
        --danger: #e74c3c;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --gradient: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        color: white;
        padding: 1.5rem;
        text-align: center;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 1rem;
    }
    
    .logo {
        font-size: 2.8rem;
        font-weight: bold;
        color: white;
    }
    
    .tagline {
        font-size: 1.2rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 25px;
        border-left: 5px solid var(--secondary);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        color: var(--primary);
    }
    
    .card-title {
        font-size: 1.6rem;
        font-weight: 600;
    }
    
    .status {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 15px;
    }
    
    .status-pending {
        background-color: #ffeaa7;
        color: #d35400;
    }
    
    .status-approved {
        background-color: #d1f7c4;
        color: #27ae60;
    }
    
    .status-rejected {
        background-color: #ffcfd2;
        color: #c0392b;
    }
    
    .stButton>button {
        background-color: var(--secondary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 25px;
        font-weight: 500;
        transition: background-color 0.3s ease, transform 0.2s;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: var(--primary);
        transform: translateY(-2px);
    }
    
    .progress-bar {
        height: 12px;
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 15px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        border-radius: 10px;
        width: 0%;
        transition: width 1s ease-in-out;
    }
    
    .factor-container {
        margin: 20px 0;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    .factor-title {
        font-weight: 600;
        margin-bottom: 10px;
        color: var(--primary);
    }
    
    .result-container {
        margin-top: 25px;
        padding: 20px;
        border-radius: 8px;
    }
    
    .result-success {
        background-color: #d1f7c4;
        border-left: 5px solid #27ae60;
    }
    
    .result-warning {
        background-color: #ffeaa7;
        border-left: 5px solid #f39c12;
    }
    
    .result-danger {
        background-color: #ffcfd2;
        border-left: 5px solid #e74c3c;
    }
    
    footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        color: #666;
        font-size: 0.9rem;
        background: white;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'completed_assessments' not in st.session_state:
    st.session_state.completed_assessments = {
        'credit': False,
        'tax': False,
        'insurance': False
    }

if 'credit_score' not in st.session_state:
    st.session_state.credit_score = 0

if 'tax_result' not in st.session_state:
    st.session_state.tax_result = {}

if 'insurance_result' not in st.session_state:
    st.session_state.insurance_result = {}

# Header
st.markdown("""
<div class="main-header">
    <div class="logo-container">
        <div class="logo">FinScore</div>
    </div>
    <div class="tagline">Comprehensive Financial Health Assessment for Inclusive Credit Scoring</div>
</div>
""", unsafe_allow_html=True)

# Main container
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Progress bar
        completed_count = sum(st.session_state.completed_assessments.values())
        progress_percentage = (completed_count / 3) * 100
        
        st.markdown(f"""
        <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 30px;">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_percentage}%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 1rem; color: #666; font-weight: 500;">
                <span>Loan Eligibility Progress</span>
                <span>{progress_percentage:.0f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dashboard cards
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Credit Assessment</h2>
                </div>
                <p>Calculate your credit score based on payment history, credit utilization, length of credit history, new credit, and credit mix.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Calculate Credit Score", key="credit_btn"):
                st.session_state.show_credit = True
        
        with col5:
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Tax Calculation</h2>
                </div>
                <p>Calculate your tax bracket, net vs gross income, and tax obligations.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Calculate Tax", key="tax_btn"):
                st.session_state.show_tax = True
                
        with col6:
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Insurance Coverage</h2>
                </div>
                <p>Review your insurance coverage across health, auto, home, and life policies.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Check Insurance", key="insurance_btn"):
                st.session_state.show_insurance = True
        
        # Credit Assessment
        if st.session_state.get('show_credit', False):
            with st.expander("Credit Score Calculation", expanded=True):
                st.subheader("Credit Score Calculation")
                st.write("Enter your financial information to calculate your credit score (300-850 range)")
                
                # Payment History
                with st.container():
                    st.markdown("""
                    <div class="factor-container">
                        <div class="factor-title">Payment History (35%)</div>
                        <div>Your track record of making timely payments</div>
                    </div>
                    """, unsafe_allow_html=True)
                    payment_history = st.slider("On-time payment percentage (0-100%)", 0, 100, 50, key="payment_history")
                
                # Credit Utilization
                with st.container():
                    st.markdown("""
                    <div class="factor-container">
                        <div class="factor-title">Credit Utilization (30%)</div>
                        <div>Your outstanding balances relative to your total credit limits</div>
                    </div>
                    """, unsafe_allow_html=True)
                    credit_utilization = st.slider("Credit utilization ratio (0-100%)", 0, 100, 30, key="credit_utilization")
                
                # Length of Credit History
                with st.container():
                    st.markdown("""
                    <div class="factor-container">
                        <div class="factor-title">Length of Credit History (15%)</div>
                        <div>How long you've had credit accounts</div>
                    </div>
                    """, unsafe_allow_html=True)
                    credit_history = st.slider("Credit history length (in years)", 0, 50, 5, key="credit_history")
                
                # New Credit
                with st.container():
                    st.markdown("""
                    <div class="factor-container">
                        <div class="factor-title">New Credit (10%)</div>
                        <div>Recent credit inquiries and new accounts</div>
                    </div>
                    """, unsafe_allow_html=True)
                    new_credit = st.slider("Number of new credit accounts in past year", 0, 20, 2, key="new_credit")
                
                # Credit Mix
                with st.container():
                    st.markdown("""
                    <div class="factor-container">
                        <div class="factor-title">Credit Mix (10%)</div>
                        <div>Variety of credit types (credit cards, mortgage, auto loans, etc.)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    credit_mix = st.slider("Number of different credit types", 0, 10, 3, key="credit_mix")
                
                if st.button("Calculate Credit Score", key="calculate_credit"):
                    # Calculate individual factor scores
                    payment_score = (payment_history / 100) * 35 * 10
                    utilization_score = (1 - min(credit_utilization, 100) / 100) * 30 * 10
                    history_score = (min(credit_history, 30) / 30) * 15 * 10
                    new_credit_score = (1 - min(new_credit, 10) / 10) * 10 * 10
                    mix_score = (min(credit_mix, 5) / 5) * 10 * 10
                    
                    # Calculate total score (300-850 range)
                    total_score = 300 + payment_score + utilization_score + history_score + new_credit_score + mix_score
                    total_score = round(min(max(total_score, 300), 850))
                    
                    # Determine rating
                    if total_score >= 800:
                        rating = "Excellent"
                        rating_color = "#27ae60"
                    elif total_score >= 740:
                        rating = "Very Good"
                        rating_color = "#2ecc71"
                    elif total_score >= 670:
                        rating = "Good"
                        rating_color = "#f39c12"
                    elif total_score >= 580:
                        rating = "Fair"
                        rating_color = "#e67e22"
                    else:
                        rating = "Poor"
                        rating_color = "#e74c3c"
                    
                    # Store results
                    st.session_state.credit_score = total_score
                    st.session_state.completed_assessments['credit'] = True
                    
                    # Display results
                    if total_score >= 670:
                        result_class = "result-success"
                    elif total_score >= 580:
                        result_class = "result-warning"
                    else:
                        result_class = "result-danger"
                    
                    st.markdown(f"""
                    <div class="result-container {result_class}">
                        <h3>Credit Score Results</h3>
                        <div style="font-size: 2.5rem; font-weight: bold; color: {rating_color}; margin: 15px 0;">
                            {total_score}
                        </div>
                        <div style="color: {rating_color}; font-weight: bold; font-size: 1.2rem; margin-bottom: 15px;">
                            {rating}
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px;">
                            <div>Payment History: <b>{round(payment_score/3.5)}/100</b></div>
                            <div>Credit Utilization: <b>{round(utilization_score/3)}/100</b></div>
                            <div>Credit History: <b>{round(history_score/1.5)}/100</b></div>
                            <div>New Credit: <b>{round(new_credit_score)}/100</b></div>
                            <div>Credit Mix: <b>{round(mix_score)}/100</b></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.success("Credit assessment completed!")
        
        # Tax Calculation
        if st.session_state.get('show_tax', False):
            with st.expander("Tax Calculation", expanded=True):
                st.subheader("Tax Calculation")
                
                annual_income = st.number_input("Annual Gross Income ($)", min_value=0, step=1000, key="annual_income")
                filing_status = st.selectbox("Filing Status", ["Single", "Married Filing Jointly", "Head of Household"], key="filing_status")
                deductions = st.number_input("Total Deductions ($)", min_value=0, step=1000, key="deductions")
                
                if st.button("Calculate Tax", key="calculate_tax"):
                    if annual_income <= 0:
                        st.error("Please enter your annual income")
                    else:
                        taxable_income = annual_income - deductions
                        
                        # Simplified tax brackets for demonstration
                        tax_bracket = ""
                        tax_amount = 0
                        
                        if filing_status == "Single":
                            if taxable_income <= 11000:
                                tax_bracket = "10%"
                                tax_amount = taxable_income * 0.1
                            elif taxable_income <= 44725:
                                tax_bracket = "12%"
                                tax_amount = 1100 + (taxable_income - 11000) * 0.12
                            elif taxable_income <= 95375:
                                tax_bracket = "22%"
                                tax_amount = 5147 + (taxable_income - 44725) * 0.22
                            else:
                                tax_bracket = "24%+"
                                tax_amount = 16290 + (taxable_income - 95375) * 0.24
                        elif filing_status == "Married Filing Jointly":
                            if taxable_income <= 22000:
                                tax_bracket = "10%"
                                tax_amount = taxable_income * 0.1
                            elif taxable_income <= 89450:
                                tax_bracket = "12%"
                                tax_amount = 2200 + (taxable_income - 22000) * 0.12
                            elif taxable_income <= 190750:
                                tax_bracket = "22%"
                                tax_amount = 10294 + (taxable_income - 89450) * 0.22
                            else:
                                tax_bracket = "24%+"
                                tax_amount = 32580 + (taxable_income - 190750) * 0.24
                        else:  # Head of Household
                            if taxable_income <= 15700:
                                tax_bracket = "10%"
                                tax_amount = taxable_income * 0.1
                            elif taxable_income <= 59850:
                                tax_bracket = "12%"
                                tax_amount = 1570 + (taxable_income - 15700) * 0.12
                            elif taxable_income <= 95350:
                                tax_bracket = "22%"
                                tax_amount = 6868 + (taxable_income - 59850) * 0.22
                            else:
                                tax_bracket = "24%+"
                                tax_amount = 14678 + (taxable_income - 95350) * 0.24
                        
                        net_income = annual_income - tax_amount
                        
                        # Store results
                        st.session_state.tax_result = {
                            "gross_income": annual_income,
                            "taxable_income": taxable_income,
                            "tax_bracket": tax_bracket,
                            "tax_amount": tax_amount,
                            "net_income": net_income
                        }
                        st.session_state.completed_assessments['tax'] = True
                        
                        # Display results
                        st.markdown(f"""
                        <div class="result-container result-success">
                            <h3>Tax Calculation Results</h3>
                            <p><strong>Gross Income:</strong> ${annual_income:,.2f}</p>
                            <p><strong>Taxable Income:</strong> ${taxable_income:,.2f}</p>
                            <p><strong>Tax Bracket:</strong> {tax_bracket}</p>
                            <p><strong>Estimated Tax:</strong> ${tax_amount:,.2f}</p>
                            <p><strong>Net Income:</strong> ${net_income:,.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("Tax assessment completed!")
        
        # Insurance Calculation
        if st.session_state.get('show_insurance', False):
            with st.expander("Insurance Coverage", expanded=True):
                st.subheader("Insurance Coverage")
                
                health_insurance = st.selectbox("Health Insurance Coverage", ["No Coverage", "Basic Coverage", "Comprehensive Coverage"], key="health_insurance")
                auto_insurance = st.selectbox("Auto Insurance Coverage", ["No Coverage", "Liability Only", "Full Coverage"], key="auto_insurance")
                home_insurance = st.selectbox("Home Insurance Coverage", ["No Coverage", "Renters Insurance", "Homeowners Insurance"], key="home_insurance")
                life_insurance = st.selectbox("Life Insurance Coverage", ["No Coverage", "Term Life", "Whole Life"], key="life_insurance")
                
                if st.button("Evaluate Coverage", key="evaluate_coverage"):
                    coverage_score = 0
                    recommendations = []
                    
                    # Evaluate health insurance
                    if health_insurance == "No Coverage":
                        recommendations.append("Consider getting health insurance to protect against medical costs")
                    elif health_insurance == "Basic Coverage":
                        coverage_score += 25
                    else:
                        coverage_score += 35
                    
                    # Evaluate auto insurance
                    if auto_insurance == "No Coverage":
                        recommendations.push("Auto insurance is legally required in most states")
                    elif auto_insurance == "Liability Only":
                        coverage_score += 15
                    else:
                        coverage_score += 20
                    
                    # Evaluate home insurance
                    if home_insurance == "No Coverage":
                        recommendations.append("Consider getting home/renters insurance to protect your property")
                    elif home_insurance == "Renters Insurance":
                        coverage_score += 15
                    else:
                        coverage_score += 25
                    
                    # Evaluate life insurance
                    if life_insurance == "No Coverage":
                        recommendations.append("Consider life insurance if you have dependents")
                    elif life_insurance == "Term Life":
                        coverage_score += 15
                    else:
                        coverage_score += 20
                    
                    # Store results
                    st.session_state.insurance_result = {
                        "coverage_score": coverage_score,
                        "recommendations": recommendations
                    }
                    st.session_state.completed_assessments['insurance'] = True
                    
                    # Display results
                    if coverage_score >= 70:
                        result_class = "result-success"
                    elif coverage_score >= 40:
                        result_class = "result-warning"
                    else:
                        result_class = "result-danger"
                    
                    recommendations_html = ""
                    if recommendations:
                        recommendations_html = "<h4>Recommendations:</h4><ul>"
                        for rec in recommendations:
                            recommendations_html += f"<li>{rec}</li>"
                        recommendations_html += "</ul>"
                    
                    st.markdown(f"""
                    <div class="result-container {result_class}">
                        <h3>Insurance Coverage Results</h3>
                        <p><strong>Coverage Score:</strong> {coverage_score}/100</p>
                        {recommendations_html}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.success("Insurance assessment completed!")
        
        # Final eligibility check
        st.markdown("""
        <div class="card">
            <h2 style="margin-bottom: 15px;">Loan Eligibility Result</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if completed_count == 3:
            if st.button("Check Eligibility", key="check_eligibility"):
                credit_score = st.session_state.credit_score
                annual_income = st.session_state.tax_result.get("gross_income", 0)
                
                eligible = True
                reasons = []
                
                if credit_score < 580:
                    eligible = False
                    reasons.append('Credit score is too low (below 580)')
                elif credit_score < 670:
                    reasons.append('Credit score is fair, which may result in higher interest rates')
                
                if annual_income < 30000:
                    reasons.append('Income is relatively low, which may limit loan amount')
                
                if eligible:
                    st.markdown(f"""
                    <div class="result-container result-success">
                        <h3 style="color: #27ae60;">Congratulations! You are eligible for a loan.</h3>
                        <p>Based on your financial assessment, you meet our criteria for loan approval.</p>
                        <p>Next steps: A loan officer will contact you to discuss options and amounts.</p>
                        {f'<p>Notes: <ul>{"".join([f"<li>{reason}</li>" for reason in reasons])}</ul></p>' if reasons else ''}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-container result-danger">
                        <h3 style="color: #e74c3c;">Currently not eligible for a loan.</h3>
                        <p>Reasons:</p>
                        <ul>
                            {"".join([f"<li>{reason}</li>" for reason in reasons])}
                        </ul>
                        <p>Please work on improving these areas and check back later.</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Complete all assessments above to determine your loan eligibility.")
        
        # Footer
        st.markdown("""
        <footer>
            <div>
                <p>FinScore - Alternative Credit Scoring for Financial Inclusion</p>
                <p>DSS INNOVATERS - Digital Dawn Track | Providing financial assistance to the masses</p>
                <p>Team: Divyanshu, Sukrit Pal, Shaurya Jha, Samarth Singh</p>
            </div>
        </footer>
        """, unsafe_allow_html=True)
