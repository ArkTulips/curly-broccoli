import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_calendar import calendar
import uuid

# Enhanced ExpenseTracker Class
class EnhancedExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, description, date, payment_method="Cash"):
        self.expenses.append({
            "amount": amount, 
            "category": category, 
            "description": description,
            "date": date,
            "payment_method": payment_method,
            "month": date.strftime("%Y-%m"),
            "year": date.year,
            "weekday": date.strftime("%A")
        })

    def total_expenses(self):
        return sum(exp["amount"] for exp in self.expenses)

    def monthly_expenses(self, year, month):
        return sum(exp["amount"] for exp in self.expenses 
                  if exp["date"].year == year and exp["date"].month == month)

    def daily_expenses(self, date):
        return sum(exp["amount"] for exp in self.expenses 
                  if exp["date"] == date)

    def expense_summary_by_category(self):
        summary = {}
        for exp in self.expenses:
            summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]
        return summary

    def expense_summary_by_month(self):
        summary = {}
        for exp in self.expenses:
            month_key = exp["month"]
            summary[month_key] = summary.get(month_key, 0) + exp["amount"]
        return summary

    def expense_summary_by_payment_method(self):
        summary = {}
        for exp in self.expenses:
            method = exp["payment_method"]
            summary[method] = summary.get(method, 0) + exp["amount"]
        return summary

    def get_top_expenses(self, n=5):
        sorted_expenses = sorted(self.expenses, key=lambda x: x["amount"], reverse=True)
        return sorted_expenses[:n]

    def budget_analysis(self, monthly_budget):
        today = datetime.date.today()
        current_month_expense = self.monthly_expenses(today.year, today.month)

        if current_month_expense > monthly_budget:
            return f"⚠️ Over budget by ₹{current_month_expense - monthly_budget:.2f}", "danger"
        else:
            remaining = monthly_budget - current_month_expense
            percentage_used = (current_month_expense / monthly_budget) * 100 if monthly_budget > 0 else 0
            return f"✅ Within budget. Remaining: ₹{remaining:.2f} ({percentage_used:.1f}% used)", "success"

    def get_expenses_df(self):
        if not self.expenses:
            return pd.DataFrame()
        return pd.DataFrame(self.expenses)

    def get_weekly_expenses(self):
        weekly_summary = {}
        for exp in self.expenses:
            week_start = exp["date"] - datetime.timedelta(days=exp["date"].weekday())
            week_key = week_start.strftime("%Y-%m-%d")
            weekly_summary[week_key] = weekly_summary.get(week_key, 0) + exp["amount"]
        return weekly_summary

# Streamlit App Configuration
st.set_page_config(
    page_title="💰 Enhanced Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .expense-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize the Enhanced Expense Tracker
if 'enhanced_tracker' not in st.session_state:
    st.session_state.enhanced_tracker = EnhancedExpenseTracker()

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'goals' not in st.session_state:
    st.session_state.goals = {}

# Load expenses from session state
st.session_state.enhanced_tracker.expenses = st.session_state.expenses

# App Title
st.markdown('<h1 class="main-header">💰 Enhanced Expense Tracker & Budget Manager</h1>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox("Choose a page:", [
    "🏠 Dashboard", 
    "➕ Add Expense", 
    "📅 Calendar View",
    "📈 Analytics", 
    "🎯 Budget Goals",
    "📋 All Expenses"
])

# Predefined categories with emojis
CATEGORIES = [
    "🍽️ Food & Dining", "🚗 Transportation", "🏠 Housing", "🛍️ Shopping",
    "💊 Healthcare", "🎬 Entertainment", "📚 Education", "💼 Business",
    "🏋️ Fitness", "🎁 Gifts", "💳 Bills & Utilities", "💰 Investment",
    "🧥 Clothing", "✈️ Travel", "🔧 Maintenance", "📱 Technology",
    "🎨 Hobbies", "🐕 Pet Care", "💄 Personal Care", "📦 Other"
]

PAYMENT_METHODS = ["💳 Credit Card", "💰 Cash", "🏦 Debit Card", "📱 Digital Wallet", "💸 Bank Transfer", "📄 Check"]

# Dashboard Page
if page == "🏠 Dashboard":
    st.header("📊 Financial Overview")

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_exp = st.session_state.enhanced_tracker.total_expenses()
        st.metric("💸 Total Expenses", f"₹{total_exp:.2f}")

    with col2:
        today = datetime.date.today()
        current_month_exp = st.session_state.enhanced_tracker.monthly_expenses(today.year, today.month)
        st.metric("📅 This Month", f"₹{current_month_exp:.2f}")

    with col3:
        daily_exp = st.session_state.enhanced_tracker.daily_expenses(today)
        st.metric("📆 Today", f"₹{daily_exp:.2f}")

    with col4:
        expense_count = len(st.session_state.enhanced_tracker.expenses)
        st.metric("📊 Total Transactions", expense_count)

    # Quick Budget Analysis
    if st.session_state.goals.get('monthly_budget'):
        monthly_budget = st.session_state.goals['monthly_budget']
        analysis, status = st.session_state.enhanced_tracker.budget_analysis(monthly_budget)

        if status == "danger":
            st.error(analysis)
        else:
            st.success(analysis)

        # Budget Progress Bar
        progress = min(current_month_exp / monthly_budget, 1.0) if monthly_budget > 0 else 0
        st.progress(progress)

    # Recent Expenses
    st.subheader("🕐 Recent Expenses")
    if st.session_state.enhanced_tracker.expenses:
        recent_expenses = sorted(st.session_state.enhanced_tracker.expenses, 
                               key=lambda x: x['date'], reverse=True)[:5]
        for exp in recent_expenses:
            st.markdown(f"""
            <div class="expense-card">
                <strong>{exp['category']}</strong> - ₹{exp['amount']:.2f}<br>
                <small>{exp['description']} | {exp['date']} | {exp['payment_method']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No expenses recorded yet. Add your first expense to get started!")

# Add Expense Page
elif page == "➕ Add Expense":
    st.header("➕ Add New Expense")

    with st.form("enhanced_expense_form"):
        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input("💰 Amount (₹)", min_value=0.01, format="%.2f", step=0.01)
            category = st.selectbox("📂 Category", CATEGORIES)
            payment_method = st.selectbox("💳 Payment Method", PAYMENT_METHODS)

        with col2:
            description = st.text_input("📝 Description")
            expense_date = st.date_input("📅 Date", datetime.date.today())

        # Tags and Notes
        tags = st.text_input("🏷️ Tags (comma-separated)", placeholder="groceries, weekly, essential")
        notes = st.text_area("📋 Additional Notes", placeholder="Optional notes about this expense...")

        # Receipt Upload
        receipt = st.file_uploader("📎 Upload Receipt (Optional)", type=['jpg', 'jpeg', 'png', 'pdf'])

        submitted = st.form_submit_button("➕ Add Expense", type="primary")

        if submitted and amount > 0 and category and description:
            st.session_state.enhanced_tracker.add_expense(
                amount, category, description, expense_date, payment_method
            )
            st.session_state.expenses = st.session_state.enhanced_tracker.expenses
            st.success(f"✅ Added ₹{amount:.2f} expense for {category}")
            st.balloons()

# Calendar View Page
elif page == "📅 Calendar View":
    st.header("📅 Daily Expense Calendar")

    if not st.session_state.enhanced_tracker.expenses:
        st.warning("No expenses to display. Add some expenses first!")
    else:
        # Prepare calendar events
        calendar_events = []
        for exp in st.session_state.enhanced_tracker.expenses:
            calendar_events.append({
                "title": f"{exp['category']}: ₹{exp['amount']:.2f}",
                "start": exp['date'].strftime("%Y-%m-%d"),
                "color": "#FF6B6B" if exp['amount'] > 100 else "#4ECDC4",
                "extendedProps": {
                    "description": exp['description'],
                    "amount": exp['amount'],
                    "category": exp['category']
                }
            })

        # Calendar options
        calendar_options = {
            "editable": True,
            "selectable": True,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridMonth,dayGridWeek,listWeek"
            },
            "initialView": "dayGridMonth",
            "height": 650
        }

        # Generate unique key for calendar
        if "calendar_key" not in st.session_state:
            st.session_state.calendar_key = str(uuid.uuid4())

        # Display calendar
        calendar_state = calendar(
            events=calendar_events,
            options=calendar_options,
            custom_css="""
                .fc-event {
                    font-size: 12px;
                    border-radius: 5px;
                }
                .fc-daygrid-event {
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }
            """,
            key=st.session_state.calendar_key
        )

        # Display selected date information
        if calendar_state.get("dateClick"):
            selected_date = datetime.datetime.strptime(
                calendar_state["dateClick"]["dateStr"], "%Y-%m-%d"
            ).date()

            st.subheader(f"📅 Expenses for {selected_date}")

            day_expenses = [exp for exp in st.session_state.enhanced_tracker.expenses 
                          if exp['date'] == selected_date]

            if day_expenses:
                total_day = sum(exp['amount'] for exp in day_expenses)
                st.metric("Daily Total", f"₹{total_day:.2f}")

                for exp in day_expenses:
                    st.write(f"• **{exp['category']}**: ₹{exp['amount']:.2f} - {exp['description']}")
            else:
                st.info("No expenses recorded for this date.")

# Analytics Page
elif page == "📈 Analytics":
    st.header("📈 Expense Analytics & Insights")

    if not st.session_state.enhanced_tracker.expenses:
        st.warning("No data available for analysis. Add some expenses first!")
    else:
        df = st.session_state.enhanced_tracker.get_expenses_df()

        # Analysis tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Category Analysis", "📅 Time Trends", "💳 Payment Methods", "🔍 Insights"])

        with tab1:
            st.subheader("📊 Expenses by Category")

            category_summary = st.session_state.enhanced_tracker.expense_summary_by_category()

            if category_summary:
                # Pie Chart
                fig_pie = px.pie(
                    values=list(category_summary.values()),
                    names=list(category_summary.keys()),
                    title="Expense Distribution by Category",
                    height=500
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

                # Bar Chart
                fig_bar = px.bar(
                    x=list(category_summary.keys()),
                    y=list(category_summary.values()),
                    title="Category-wise Spending",
                    labels={'x': 'Category', 'y': 'Amount (₹)'}
                )
                fig_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)

        with tab2:
            st.subheader("📅 Spending Trends Over Time")

            # Monthly trends
            monthly_summary = st.session_state.enhanced_tracker.expense_summary_by_month()

            if monthly_summary:
                fig_line = px.line(
                    x=list(monthly_summary.keys()),
                    y=list(monthly_summary.values()),
                    title="Monthly Spending Trend",
                    labels={'x': 'Month', 'y': 'Amount (₹)'}
                )
                st.plotly_chart(fig_line, use_container_width=True)

                # Weekly analysis
                weekly_summary = st.session_state.enhanced_tracker.get_weekly_expenses()
                if len(weekly_summary) > 1:
                    fig_weekly = px.bar(
                        x=list(weekly_summary.keys()),
                        y=list(weekly_summary.values()),
                        title="Weekly Spending Pattern",
                        labels={'x': 'Week Starting', 'y': 'Amount (₹)'}
                    )
                    st.plotly_chart(fig_weekly, use_container_width=True)

        with tab3:
            st.subheader("💳 Payment Method Analysis")

            payment_summary = st.session_state.enhanced_tracker.expense_summary_by_payment_method()

            if payment_summary:
                fig_donut = go.Figure(data=[go.Pie(
                    labels=list(payment_summary.keys()),
                    values=list(payment_summary.values()),
                    hole=.3
                )])
                fig_donut.update_layout(
                    title="Payment Method Distribution",
                    annotations=[dict(text='Payment<br>Methods', x=0.5, y=0.5, font_size=16, showarrow=False)]
                )
                st.plotly_chart(fig_donut, use_container_width=True)

        with tab4:
            st.subheader("🔍 Smart Insights")

            # Top expenses
            top_expenses = st.session_state.enhanced_tracker.get_top_expenses()
            if top_expenses:
                st.write("💸 **Highest Expenses:**")
                for i, exp in enumerate(top_expenses, 1):
                    st.write(f"{i}. {exp['category']}: ₹{exp['amount']:.2f} - {exp['description']}")

            # Category insights
            category_summary = st.session_state.enhanced_tracker.expense_summary_by_category()
            if category_summary:
                highest_category = max(category_summary, key=category_summary.get)
                st.info(f"💡 **Insight**: Your highest spending category is **{highest_category}** with ₹{category_summary[highest_category]:.2f}")

                # Average per category
                avg_per_category = {cat: amount/len([e for e in st.session_state.enhanced_tracker.expenses if e['category'] == cat]) 
                                  for cat, amount in category_summary.items()}
                highest_avg_category = max(avg_per_category, key=avg_per_category.get)
                st.info(f"📊 **Average Insight**: **{highest_avg_category}** has the highest average expense of ₹{avg_per_category[highest_avg_category]:.2f} per transaction")

# Budget Goals Page
elif page == "🎯 Budget Goals":
    st.header("🎯 Budget Goals & Limits")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Monthly Budget")
        monthly_budget = st.number_input(
            "Set Monthly Budget (₹)", 
            min_value=0.0, 
            value=st.session_state.goals.get('monthly_budget', 1000.0),
            step=50.0
        )

        if st.button("💾 Save Monthly Budget"):
            st.session_state.goals['monthly_budget'] = monthly_budget
            st.success(f"Monthly budget set to ₹{monthly_budget:.2f}")

        # Category-wise budgets
        st.subheader("📂 Category Budgets")
        selected_category = st.selectbox("Select Category for Budget", CATEGORIES)
        category_budget = st.number_input(f"Budget for {selected_category} (₹)", min_value=0.0, step=10.0)

        if st.button("💾 Save Category Budget"):
            if 'category_budgets' not in st.session_state.goals:
                st.session_state.goals['category_budgets'] = {}
            st.session_state.goals['category_budgets'][selected_category] = category_budget
            st.success(f"Budget for {selected_category} set to ₹{category_budget:.2f}")

    with col2:
        st.subheader("🎯 Savings Goals")
        savings_goal = st.number_input(
            "Monthly Savings Target (₹)", 
            min_value=0.0, 
            value=st.session_state.goals.get('savings_goal', 500.0),
            step=25.0
        )

        if st.button("💾 Save Savings Goal"):
            st.session_state.goals['savings_goal'] = savings_goal
            st.success(f"Savings goal set to ₹{savings_goal:.2f}")

        # Daily spending limit
        st.subheader("📆 Daily Spending Limit")
        daily_limit = st.number_input(
            "Daily Spending Limit (₹)", 
            min_value=0.0, 
            value=st.session_state.goals.get('daily_limit', 50.0),
            step=5.0
        )

        if st.button("💾 Save Daily Limit"):
            st.session_state.goals['daily_limit'] = daily_limit
            st.success(f"Daily spending limit set to ₹{daily_limit:.2f}")

    # Goals Overview
    if st.session_state.goals:
        st.subheader("📋 Current Goals Overview")

        today = datetime.date.today()
        current_month_exp = st.session_state.enhanced_tracker.monthly_expenses(today.year, today.month)
        daily_exp = st.session_state.enhanced_tracker.daily_expenses(today)

        # Monthly budget progress
        if 'monthly_budget' in st.session_state.goals:
            monthly_budget = st.session_state.goals['monthly_budget']
            monthly_progress = min(current_month_exp / monthly_budget, 1.0) if monthly_budget > 0 else 0
            st.metric(
                "📅 Monthly Budget Progress", 
                f"₹{current_month_exp:.2f} / ₹{monthly_budget:.2f}",
                f"{monthly_progress*100:.1f}% used"
            )
            st.progress(monthly_progress)

        # Daily limit check
        if 'daily_limit' in st.session_state.goals:
            daily_limit = st.session_state.goals['daily_limit']
            if daily_exp > daily_limit:
                st.error(f"⚠️ Today's spending (₹{daily_exp:.2f}) exceeds daily limit (₹{daily_limit:.2f})")
            else:
                st.success(f"✅ Today's spending (₹{daily_exp:.2f}) is within daily limit (₹{daily_limit:.2f})")

# All Expenses Page
elif page == "📋 All Expenses":
    st.header("📋 All Expenses")

    if not st.session_state.enhanced_tracker.expenses:
        st.info("No expenses recorded yet.")
    else:
        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            category_filter = st.multiselect("Filter by Category", CATEGORIES)

        with col2:
            payment_filter = st.multiselect("Filter by Payment Method", PAYMENT_METHODS)

        with col3:
            date_range = st.date_input("Date Range", value=(
                min(exp['date'] for exp in st.session_state.enhanced_tracker.expenses),
                max(exp['date'] for exp in st.session_state.enhanced_tracker.expenses)
            ))

        # Filter expenses
        filtered_expenses = st.session_state.enhanced_tracker.expenses

        if category_filter:
            filtered_expenses = [exp for exp in filtered_expenses if exp['category'] in category_filter]

        if payment_filter:
            filtered_expenses = [exp for exp in filtered_expenses if exp['payment_method'] in payment_filter]

        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_expenses = [exp for exp in filtered_expenses 
                               if start_date <= exp['date'] <= end_date]

        # Display filtered expenses
        if filtered_expenses:
            df = pd.DataFrame(filtered_expenses)
            df = df.sort_values('date', ascending=False)

            st.dataframe(
                df[['date', 'category', 'description', 'amount', 'payment_method']],
                use_container_width=True
            )

            # Summary of filtered data
            st.subheader("📊 Filtered Summary")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Amount", f"₹{sum(exp['amount'] for exp in filtered_expenses):.2f}")

            with col2:
                st.metric("Number of Transactions", len(filtered_expenses))

            with col3:
                avg_amount = sum(exp['amount'] for exp in filtered_expenses) / len(filtered_expenses)
                st.metric("Average Amount", f"₹{avg_amount:.2f}")
        else:
            st.warning("No expenses match the current filters.")

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Use the calendar view to track daily spending patterns and the analytics page for deeper insights!")
