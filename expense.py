import streamlit as st
import datetime

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, date):
        self.expenses.append({"amount": amount, "category": category, "date": date})

    def total_expenses(self):
        return sum(exp["amount"] for exp in self.expenses)

    def monthly_expenses(self, year, month):
        return sum(exp["amount"] for exp in self.expenses if exp["date"].year == year and exp["date"].month == month)

    def expense_summary_by_category(self):
        summary = {}
        for exp in self.expenses:
            summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]
        return summary

    def budget_analysis(self, monthly_budget):
        today = datetime.date.today()
        current_month_expense = self.monthly_expenses(today.year, today.month)
        if current_month_expense > monthly_budget:
            return f"Over budget by {current_month_expense - monthly_budget:.2f}"
        else:
            return f"Within budget. Remaining: {monthly_budget - current_month_expense:.2f}"


# --- Streamlit App ---
st.title("💰 Expense Tracking and Budgeting App")

# Initialize tracker
tracker = ExpenseTracker()

# Session state for persistence
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

tracker.expenses = st.session_state["expenses"]

# --- Add Expense Form ---
with st.form(key="expense_form"):
    amount = st.number_input("Expense Amount", min_value=0.0, format="%.2f")
    category = st.text_input("Category")
    date = st.date_input("Date", datetime.date.today())
    submit_button = st.form_submit_button(label="Add Expense")

    if submit_button:
        tracker.add_expense(amount, category, date)
        st.success("Expense added successfully!")

# --- Summary ---
st.subheader("📊 Expense Summary by Category")
summary = tracker.expense_summary_by_category()
for cat, amt in summary.items():
    st.write(f"{cat}: {amt:.2f}")

st.subheader("💵 Total Expenses")
st.write(f"{tracker.total_expenses():.2f}")

st.subheader("📈 Budget Analysis")
monthly_budget = st.number_input("Enter your monthly budget", min_value=0.0, format="%.2f")
if monthly_budget > 0:
    st.write(tracker.budget_analysis(monthly_budget))

st.subheader("📝 All Expenses")
for exp in sorted(tracker.expenses, key=lambda x: x['date'], reverse=True):
    st.write(f"{exp['date']} - {exp['category']}: {exp['amount']:.2f}")
