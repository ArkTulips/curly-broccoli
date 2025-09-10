def calculate_tax(income):
    tax = 0

    if income <= 1200000:
        tax = 0
    elif income <= 800000:
        tax = (income - 400000) * 0.05
    elif income <= 1200000:
        tax = (400000 * 0.05) + (income - 800000) * 0.10
    elif income <= 1600000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (income - 1200000) * 0.15
    elif income <= 2000000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (income - 1600000) * 0.20
    elif income <= 2400000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (income - 2000000) * 0.25
    else:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (400000 * 0.25) + (
                    income - 2400000) * 0.30

    return tax


def format_currency(amount):
    return "₹{:,.2f}".format(amount)


def main():
    print("Income Tax Calculator")
    print("=" * 30)

    try:
        income = float(input("Enter your annual income in INR: "))

        if income < 0:
            print("Income cannot be negative!")
            return
        tax_amount = calculate_tax(income)
        net_income = income - tax_amount


        print("\n" + "=" * 50)
        print("TAX CALCULATION RESULTS")
        print("=" * 50)
        print(f"Original Income: {format_currency(income)}")
        print(f"Tax Payable:     {format_currency(tax_amount)}")
        print(f"Net Income:      {format_currency(net_income)}")
        print("=" * 50)

        if income > 0:
            tax_percentage = (tax_amount / income) * 100
            print(f"Effective Tax Rate: {tax_percentage:.2f}%")

    except ValueError:
        print("Please enter a valid number!")
if _name_ == "_main_":
    main()
