import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration
st.set_page_config(
    page_title=" Advanced CIBIL Score Estimator", 
    layout="wide",
    page_icon=""
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #fb8c00;
        margin-bottom: 1rem;
    }
    .score-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    .excellent { background: linear-gradient(135deg, #4caf50, #81c784); color: white; }
    .good { background: linear-gradient(135deg, #2196f3, #64b5f6); color: white; }
    .fair { background: linear-gradient(135deg, #ff9800, #ffb74d); color: white; }
    .poor { background: linear-gradient(135deg, #f44336, #e57373); color: white; }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 5px solid #1e88e5;
    }

    .improvement-tip {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

def calculate_enhanced_cibil_score(payment_history, credit_utilization, credit_history_years, 
                                 credit_mix, recent_inquiries, total_accounts, outstanding_debt,
                                 total_credit_limit, income_range, employment_type, late_payments,
                                 settled_accounts):
    """
    Enhanced CIBIL score calculation with additional factors
    """
    # Base weights (adjusted based on research)
    weights = {
        "payment_history": 0.35,
        "credit_utilization": 0.30,
        "credit_history": 0.15,
        "credit_mix": 0.10,
        "recent_inquiries": 0.10
    }

    # Payment history score (35%)
    ph_score = payment_history * weights["payment_history"]

    # Adjust for late payments
    late_payment_penalty = min(late_payments * 5, 20)
    ph_score = max(0, ph_score - (late_payment_penalty * weights["payment_history"] / 100))

    # Adjust for settled accounts
    settled_penalty = settled_accounts * 10
    ph_score = max(0, ph_score - (settled_penalty * weights["payment_history"] / 100))

    # Credit utilization score (30%)
    cu_score = (100 - credit_utilization) * weights["credit_utilization"]

    # Bonus for very low utilization
    if credit_utilization < 10:
        cu_score *= 1.1
    elif credit_utilization > 70:
        cu_score *= 0.8

    # Credit history score (15%)
    ch_score = min(credit_history_years * 7, 100) * weights["credit_history"]

    # Bonus for very long history
    if credit_history_years > 10:
        ch_score *= 1.1

    # Credit mix score (10%)
    cm_score = credit_mix * weights["credit_mix"]

    # Adjust for number of accounts
    if total_accounts < 3:
        cm_score *= 0.8
    elif total_accounts > 10:
        cm_score *= 0.9

    # Recent inquiries score (10%)
    ri_score = max(100 - (recent_inquiries * 20), 0) * weights["recent_inquiries"]

    # Additional factors adjustments

    # Income stability bonus
    income_bonus = 0
    if employment_type == "Salaried" and income_range == "Above 10 Lakhs":
        income_bonus = 5
    elif employment_type == "Self-employed" and income_range == "Above 10 Lakhs":
        income_bonus = 3
    elif income_range in ["5-10 Lakhs", "3-5 Lakhs"]:
        income_bonus = 2

    # Outstanding debt impact
    debt_impact = 0
    if outstanding_debt > 80:
        debt_impact = -10
    elif outstanding_debt > 50:
        debt_impact = -5
    elif outstanding_debt < 20:
        debt_impact = 2

    # Calculate total percentage
    total_percentage = ph_score + cu_score + ch_score + cm_score + ri_score + income_bonus + debt_impact

    # Convert to CIBIL score range (300-900)
    final_score = int(300 + (total_percentage / 100) * 600)

    # Ensure score is within bounds
    final_score = max(300, min(900, final_score))

    return final_score, {
        'payment_history': ph_score,
        'credit_utilization': cu_score,
        'credit_history': ch_score,
        'credit_mix': cm_score,
        'recent_inquiries': ri_score,
        'income_bonus': income_bonus,
        'debt_impact': debt_impact
    }

def get_score_category(score):
    """Get score category and color"""
    if score >= 750:
        return "Excellent", "excellent", "🌟"
    elif score >= 700:
        return "Good", "good", "✅"
    elif score >= 650:
        return "Fair", "fair", "⚠️"
    else:
        return "Poor", "poor", "❌"

def create_score_breakdown_pie(score_components):
    """Create pie chart showing score factor breakdown"""
    labels = ['Payment History (35%)', 'Credit Utilization (30%)', 'Credit History (15%)', 
              'Credit Mix (10%)', 'Recent Inquiries (10%)']
    values = [
        score_components['payment_history'],
        score_components['credit_utilization'], 
        score_components['credit_history'],
        score_components['credit_mix'],
        score_components['recent_inquiries']
    ]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent',
        textfont_size=12
    )])

    fig.update_layout(
        title="CIBIL Score Factor Breakdown",
        title_x=0.5,
        height=500,
        showlegend=True
    )

    return fig

def create_score_gauge(score):
    """Create gauge chart for credit score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "CIBIL Score"},
        delta = {'reference': 750},
        gauge = {
            'axis': {'range': [None, 900]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [300, 650], 'color': "lightgray"},
                {'range': [650, 700], 'color': "yellow"},
                {'range': [700, 750], 'color': "lightgreen"},
                {'range': [750, 900], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 750
            }
        }
    ))

    fig.update_layout(height=400)
    return fig

def create_improvement_roadmap(current_score):
    """Create improvement roadmap chart"""
    months = ['Current', '3 Months', '6 Months', '12 Months', '24 Months']

    # Simulate improvement trajectory
    if current_score < 600:
        projected_scores = [current_score, current_score+30, current_score+60, current_score+120, current_score+180]
    elif current_score < 700:
        projected_scores = [current_score, current_score+20, current_score+40, current_score+70, current_score+100]
    else:
        projected_scores = [current_score, current_score+10, current_score+20, current_score+35, current_score+50]

    # Cap at 900
    projected_scores = [min(900, score) for score in projected_scores]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=projected_scores,
        mode='lines+markers+text',
        text=projected_scores,
        textposition="top center",
        line=dict(color='#1e88e5', width=3),
        marker=dict(size=10),
        name='Projected Score'
    ))

    # Add target line
    fig.add_hline(y=750, line_dash="dash", line_color="green", 
                  annotation_text="Target Score (750)")

    fig.update_layout(
        title="Credit Score Improvement Roadmap",
        title_x=0.5,
        xaxis_title="Timeline",
        yaxis_title="CIBIL Score",
        height=400,
        yaxis=dict(range=[300, 900])
    )

    return fig

def get_loan_eligibility(score, income_range):
    """Get loan eligibility and interest rates"""
    eligibility_data = []

    # Home Loan
    if score >= 750:
        home_rate = "8.5-9.5%"
        home_eligible = "✅ Highly Eligible"
    elif score >= 700:
        home_rate = "9.5-10.5%"
        home_eligible = "✅ Eligible"
    elif score >= 650:
        home_rate = "10.5-12%"
        home_eligible = "⚠️ May Need Co-signer"
    else:
        home_rate = "12%+"
        home_eligible = "❌ Difficult"

    # Personal Loan
    if score >= 750:
        personal_rate = "10-14%"
        personal_eligible = "✅ Highly Eligible"
    elif score >= 700:
        personal_rate = "14-18%"
        personal_eligible = "✅ Eligible"
    elif score >= 650:
        personal_rate = "18-24%"
        personal_eligible = "⚠️ Higher Interest"
    else:
        personal_rate = "24%+"
        personal_eligible = "❌ Very Difficult"

    # Credit Card
    if score >= 750:
        cc_eligible = "✅ Premium Cards Available"
        cc_limit = "High Limits"
    elif score >= 700:
        cc_eligible = "✅ Most Cards Available"
        cc_limit = "Good Limits"
    elif score >= 650:
        cc_eligible = "⚠️ Basic Cards"
        cc_limit = "Low Limits"
    else:
        cc_eligible = "❌ Secured Cards Only"
        cc_limit = "Very Low Limits"

    return {
        'home_loan': {'eligibility': home_eligible, 'rate': home_rate},
        'personal_loan': {'eligibility': personal_eligible, 'rate': personal_rate},
        'credit_card': {'eligibility': cc_eligible, 'limit': cc_limit}
    }

def get_improvement_tips(score_components, credit_utilization, recent_inquiries, late_payments):
    """Get personalized improvement tips"""
    tips = []

    # Payment history tips
    if score_components['payment_history'] < 25:
        tips.append({
            'category': '💳 Payment History',
            'tip': 'Set up auto-pay for all bills and EMIs to ensure 100% on-time payments',
            'impact': 'High Impact',
            'timeline': '3-6 months'
        })

    # Credit utilization tips
    if credit_utilization > 30:
        tips.append({
            'category': '📊 Credit Utilization',
            'tip': f'Reduce credit card usage to below 30% (currently {credit_utilization}%)',
            'impact': 'High Impact',
            'timeline': 'Immediate'
        })

    # Recent inquiries tips
    if recent_inquiries > 3:
        tips.append({
            'category': '🔍 Credit Inquiries',
            'tip': 'Avoid applying for new credit for the next 6 months',
            'impact': 'Medium Impact',
            'timeline': '6 months'
        })

    # Late payments tips
    if late_payments > 0:
        tips.append({
            'category': '⏰ Late Payments',
            'tip': 'Contact lenders to request goodwill deletion of late payment records',
            'impact': 'Medium Impact',
            'timeline': '2-3 months'
        })

    # General tips
    tips.extend([
        {
            'category': '📈 Credit Mix',
            'tip': 'Maintain a healthy mix of secured (home/car) and unsecured (personal/credit card) loans',
            'impact': 'Low Impact',
            'timeline': '6-12 months'
        },
        {
            'category': '📋 Credit Report',
            'tip': 'Check your credit report quarterly for errors and dispute immediately',
            'impact': 'Medium Impact',
            'timeline': 'Ongoing'
        }
    ])

    return tips

# Main Streamlit App
def main():
    st.markdown('<h1 class="main-header">🎯 Advanced CIBIL Score Estimator</h1>', unsafe_allow_html=True)
    st.markdown("**Comprehensive credit score analysis with personalized improvement strategies**")

    # Sidebar for inputs
    with st.sidebar:
        st.markdown("## 📋 Credit Profile Details")

        # Basic factors
        st.markdown("### Core Credit Factors")

        payment_history = st.slider(
            "Payment History (%)", 
            0, 100, 90, 
            help="Percentage of payments made on time"
        )

        credit_utilization = st.slider(
            "Credit Utilization (%)", 
            0, 100, 30, 
            help="Percentage of credit limit used"
        )

        credit_history_years = st.slider(
            "Credit History (Years)", 
            0, 25, 5, 
            help="Age of your oldest credit account"
        )

        credit_mix = st.slider(
            "Credit Mix Score", 
            0, 100, 70, 
            help="Diversity of credit types (0=poor, 100=excellent)"
        )

        recent_inquiries = st.slider(
            "Recent Credit Inquiries", 
            0, 15, 1, 
            help="Number of credit inquiries in last 12 months"
        )

        # Enhanced factors
        st.markdown("### Additional Details")

        total_accounts = st.number_input(
            "Total Credit Accounts", 
            min_value=0, 
            max_value=20, 
            value=3,
            help="Total number of credit accounts"
        )

        outstanding_debt = st.slider(
            "Outstanding Debt (%)", 
            0, 100, 25, 
            help="Percentage of total debt outstanding"
        )

        total_credit_limit = st.number_input(
            "Total Credit Limit (₹)", 
            min_value=10000, 
            max_value=5000000, 
            value=200000, 
            step=10000,
            help="Combined credit limit across all cards"
        )

        late_payments = st.number_input(
            "Late Payments (Last 2 Years)", 
            min_value=0, 
            max_value=20, 
            value=0,
            help="Number of late payments in last 24 months"
        )

        settled_accounts = st.number_input(
            "Settled Accounts", 
            min_value=0, 
            max_value=10, 
            value=0,
            help="Number of settled/closed accounts"
        )

        # Personal details
        st.markdown("### Personal Information")

        employment_type = st.selectbox(
            "Employment Type",
            ["Salaried", "Self-employed", "Business Owner", "Retired", "Student"]
        )

        income_range = st.selectbox(
            "Annual Income Range",
            ["Below 3 Lakhs", "3-5 Lakhs", "5-10 Lakhs", "Above 10 Lakhs"]
        )

    # Calculate score button
    if st.button("🧮 Calculate CIBIL Score", type="primary", use_container_width=True):

        # Calculate the score
        score, components = calculate_enhanced_cibil_score(
            payment_history, credit_utilization, credit_history_years,
            credit_mix, recent_inquiries, total_accounts, outstanding_debt,
            total_credit_limit, income_range, employment_type, late_payments,
            settled_accounts
        )

        category, css_class, emoji = get_score_category(score)

        # Display main score
        st.markdown(f'<div class="score-display {css_class}">{emoji} Your CIBIL Score: {score}<br><small>{category}</small></div>', 
                   unsafe_allow_html=True)

        # Score interpretation
        if score >= 750:
            st.success("🎉 Excellent! You have access to the best loan rates and premium credit cards.")
        elif score >= 700:
            st.info("✅ Good score! You qualify for most loans with competitive interest rates.")
        elif score >= 650:
            st.warning("⚠️ Fair score. You may face higher interest rates. Focus on improvement.")
        else:
            st.error("❌ Poor score. Loan approval will be challenging. Immediate improvement needed.")

        # Main content area with tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Score Analysis", 
            "📈 Improvement Plan", 
            "🏦 Loan Eligibility", 
            "🎯 Score Simulator", 
            "📚 Credit Education"
        ])

        with tab1:
            st.markdown('<h2 class="sub-header">📊 Detailed Score Analysis</h2>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                # Score breakdown pie chart
                pie_fig = create_score_breakdown_pie(components)
                st.plotly_chart(pie_fig, use_container_width=True)

            with col2:
                # Score gauge
                gauge_fig = create_score_gauge(score)
                st.plotly_chart(gauge_fig, use_container_width=True)

            # Factor analysis
            st.markdown("### 🔍 Factor-wise Analysis")

            factors_df = pd.DataFrame({
                'Factor': ['Payment History', 'Credit Utilization', 'Credit History', 'Credit Mix', 'Recent Inquiries'],
                'Weight': ['35%', '30%', '15%', '10%', '10%'],
                'Your Score': [f"{components['payment_history']:.1f}/35", 
                              f"{components['credit_utilization']:.1f}/30",
                              f"{components['credit_history']:.1f}/15", 
                              f"{components['credit_mix']:.1f}/10",
                              f"{components['recent_inquiries']:.1f}/10"],
                'Status': ['🟢 Excellent' if components['payment_history'] > 28 else '🟡 Good' if components['payment_history'] > 21 else '🔴 Needs Work',
                          '🟢 Excellent' if credit_utilization < 10 else '🟡 Good' if credit_utilization < 30 else '🔴 Too High',
                          '🟢 Excellent' if credit_history_years > 7 else '🟡 Good' if credit_history_years > 3 else '🔴 Too Short',
                          '🟢 Good' if credit_mix > 60 else '🟡 Average' if credit_mix > 40 else '🔴 Limited',
                          '🟢 Good' if recent_inquiries < 2 else '🟡 Moderate' if recent_inquiries < 5 else '🔴 Too Many']
            })

            st.dataframe(factors_df, use_container_width=True, hide_index=True)

        with tab2:
            st.markdown('<h2 class="sub-header">📈 Personalized Improvement Plan</h2>', unsafe_allow_html=True)

            # Improvement roadmap
            roadmap_fig = create_improvement_roadmap(score)
            st.plotly_chart(roadmap_fig, use_container_width=True)

            # Improvement tips
            st.markdown("### 💡 Action Items to Improve Your Score")

            tips = get_improvement_tips(components, credit_utilization, recent_inquiries, late_payments)

            for tip in tips:
                st.markdown(f"""
                <div class="improvement-tip">
                    <h4>{tip['category']}</h4>
                    <p><strong>Action:</strong> {tip['tip']}</p>
                    <small><strong>Impact:</strong> {tip['impact']} | <strong>Timeline:</strong> {tip['timeline']}</small>
                </div>
                """, unsafe_allow_html=True)

        with tab3:
            st.markdown('<h2 class="sub-header">🏦 Loan Eligibility & Interest Rates</h2>', unsafe_allow_html=True)

            eligibility = get_loan_eligibility(score, income_range)

            # Create eligibility summary table
            eligibility_df = pd.DataFrame({
                'Loan Type': ['🏠 Home Loan', '👤 Personal Loan', '💳 Credit Card'],
                'Eligibility': [eligibility['home_loan']['eligibility'], 
                               eligibility['personal_loan']['eligibility'], 
                               eligibility['credit_card']['eligibility']],
                'Interest Rate / Limit': [eligibility['home_loan']['rate'], 
                                        eligibility['personal_loan']['rate'], 
                                        eligibility['credit_card']['limit']]
            })

            st.dataframe(eligibility_df, use_container_width=True, hide_index=True)

            # Loan amount estimator
            st.markdown("### 💰 Estimated Loan Amounts")

            col1, col2, col3 = st.columns(3)

            # Simple loan amount estimation based on income and score
            income_multipliers = {
                "Below 3 Lakhs": 2.5,
                "3-5 Lakhs": 4.0,
                "5-10 Lakhs": 7.0,
                "Above 10 Lakhs": 12.0
            }

            base_multiplier = income_multipliers[income_range]

            if score >= 750:
                multiplier = base_multiplier * 1.2
            elif score >= 700:
                multiplier = base_multiplier * 1.0
            elif score >= 650:
                multiplier = base_multiplier * 0.8
            else:
                multiplier = base_multiplier * 0.5

            # Estimate income midpoint
            income_estimates = {
                "Below 3 Lakhs": 2.5,
                "3-5 Lakhs": 4.0,
                "5-10 Lakhs": 7.5,
                "Above 10 Lakhs": 15.0
            }

            estimated_income = income_estimates[income_range]
            max_loan = estimated_income * multiplier

            with col1:
                st.metric("🏠 Home Loan", f"₹{max_loan:.1f} Lakhs", "Up to 80% LTV")

            with col2:
                personal_loan = min(max_loan * 0.3, 25)  # Cap at 25 lakhs
                st.metric("👤 Personal Loan", f"₹{personal_loan:.1f} Lakhs", "No Collateral")

            with col3:
                cc_limit = min(estimated_income * 3, 10)  # Cap at 10 lakhs
                st.metric("💳 Credit Card", f"₹{cc_limit:.1f} Lakhs", "Combined Limit")

        with tab4:
            st.markdown('<h2 class="sub-header">🎯 Score Simulator</h2>', unsafe_allow_html=True)

            st.markdown("### What-If Analysis")
            st.markdown("See how changes to your credit behavior could affect your score:")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Scenario: Improve Payment History")
                new_ph = st.slider("New Payment History %", payment_history, 100, payment_history+10, key="ph_sim")

                sim_score1, _ = calculate_enhanced_cibil_score(
                    new_ph, credit_utilization, credit_history_years,
                    credit_mix, recent_inquiries, total_accounts, outstanding_debt,
                    total_credit_limit, income_range, employment_type, late_payments,
                    settled_accounts
                )

                score_change1 = sim_score1 - score
                st.success(f"New Score: {sim_score1} ({score_change1:+d} points)")

            with col2:
                st.markdown("#### Scenario: Reduce Credit Utilization")
                new_cu = st.slider("New Credit Utilization %", 5, credit_utilization, max(5, credit_utilization-10), key="cu_sim")

                sim_score2, _ = calculate_enhanced_cibil_score(
                    payment_history, new_cu, credit_history_years,
                    credit_mix, recent_inquiries, total_accounts, outstanding_debt,
                    total_credit_limit, income_range, employment_type, late_payments,
                    settled_accounts
                )

                score_change2 = sim_score2 - score
                st.success(f"New Score: {sim_score2} ({score_change2:+d} points)")

            # Combined scenario
            st.markdown("#### Combined Scenario")
            combined_score, _ = calculate_enhanced_cibil_score(
                new_ph, new_cu, credit_history_years,
                credit_mix, max(0, recent_inquiries-1), total_accounts, outstanding_debt,
                total_credit_limit, income_range, employment_type, max(0, late_payments-1),
                settled_accounts
            )

            combined_change = combined_score - score
            st.info(f"With combined improvements: **{combined_score}** ({combined_change:+d} points)")

        with tab5:
            st.markdown('<h2 class="sub-header">📚 Credit Education</h2>', unsafe_allow_html=True)

            # Educational content
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 💡 CIBIL Score Basics")
                st.markdown("""
                **Score Ranges:**
                - 750-900: Excellent (Best rates)
                - 700-749: Good (Competitive rates)  
                - 650-699: Fair (Higher rates)
                - Below 650: Poor (Difficult approval)

                **Key Benefits of Good Score:**
                - Lower interest rates (save ₹1-3 lakhs on home loan)
                - Faster loan approvals
                - Higher credit limits
                - Premium credit cards
                - Better negotiating power
                """)

            with col2:
                st.markdown("### 📊 Factor Importance")
                st.markdown("""
                **Payment History (35%):**
                - Most important factor
                - Pay all bills on time
                - Avoid defaults and settlements

                **Credit Utilization (30%):**
                - Keep below 30% (ideally under 10%)
                - Pay off balances monthly
                - Don't close old cards

                **Credit History (15%):**
                - Longer history is better
                - Keep old accounts active
                - Average age matters
                """)

            # Myths and facts
            with st.expander("🔍 Common Credit Score Myths"):
                st.markdown("""
                **Myth:** Checking your credit score hurts it  
                **Fact:** Soft inquiries (by you) don't affect your score

                **Myth:** Closing credit cards improves your score  
                **Fact:** Closing cards can increase utilization ratio and hurt your score

                **Myth:** Income directly affects credit score  
                **Fact:** Income doesn't directly impact score, but affects loan eligibility

                **Myth:** Paying minimum amount is sufficient  
                **Fact:** High balances hurt your utilization ratio even with timely payments
                """)

            # Action plan
            st.markdown("### 🎯 30-60-90 Day Action Plan")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("""
                **Next 30 Days:**
                - Check credit report for errors
                - Set up autopay for all bills
                - Pay down credit card balances
                - Don't apply for new credit
                """)

            with col2:
                st.markdown("""
                **Next 60 Days:**
                - Dispute any errors found
                - Keep utilization below 30%
                - Make all payments on time
                - Monitor score monthly
                """)

            with col3:
                st.markdown("""
                **Next 90 Days:**
                - Maintain low balances
                - Consider becoming authorized user
                - Keep old accounts open
                - Review and optimize credit mix
                """)

        # Additional insights
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 Utilization Impact", f"{credit_utilization}%", 
                     "Keep below 30%" if credit_utilization > 30 else "Good!")

        with col2:
            credit_age_months = credit_history_years * 12
            st.metric("📅 Credit Age", f"{credit_age_months} months", 
                     "Build longer history" if credit_age_months < 60 else "Good!")

        with col3:
            inquiry_impact = "High" if recent_inquiries > 5 else "Medium" if recent_inquiries > 2 else "Low"
            st.metric("🔍 Inquiry Impact", f"{recent_inquiries} inquiries", inquiry_impact)

        with col4:
            accounts_status = "Good" if 3 <= total_accounts <= 8 else "Optimize"
            st.metric("🏦 Account Mix", f"{total_accounts} accounts", accounts_status)

    # Information section
    st.markdown("---")
    st.markdown("### ℹ️ About This Calculator")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **✨ Features:**
        - Enhanced calculation algorithm
        - 12+ input parameters
        - Interactive visualizations
        - Personalized improvement tips
        - Loan eligibility checker
        """)

    with col2:
        st.markdown("""
        **🎯 Benefits:**
        - Accurate score estimation
        - Detailed factor analysis
        - Improvement roadmap
        - What-if simulations
        - Educational content
        """)

    with col3:
        st.markdown("""
        **⚠️ Disclaimers:**
        - Estimates based on general factors
        - Actual scores may vary
        - Regular monitoring recommended
        - Consult credit counselor if needed
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    <p>💡 This calculator provides estimates based on industry-standard factors. Actual CIBIL scores may vary.</p>
    <p>📞 For credit counseling and dispute resolution, contact CIBIL directly or consult a financial advisor.</p>
    <p>🔄 Check your official CIBIL score regularly through authorized channels.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
