import math
import csv
import matplotlib.pyplot as plt


# TVM
def tvm_calculator():
    print("\n--- TIME VALUE OF MONEY ---")
    print("What would you like to calculate?")
    print("1. Future Value (FV)")
    print("2. Present Value (PV)")
    print("3. Interest Rate (r)")
    print("4. Number of periods (n)")

    calc_type = input("Choose calculation type (1-4): ")

    if calc_type == "1":  # Calculate FV
        P = float(input("Enter present value (P): $"))
        r = float(input("Enter annual interest rate (in %, e.g. 5): ")) / 100
        n = int(input("Enter number of years: "))
        m = int(input("Compounding frequency per year (e.g. 1, 2, 12): "))

        FV = P * (1 + r / m) ** (n * m)
        print(f"Future Value after {n} years: ${FV:,.2f}")

        # Generate chart
        create_tvm_chart(P, r, n, m, "FV")

    elif calc_type == "2":  # Calculate PV
        FV = float(input("Enter future value (FV): $"))
        r = float(input("Enter annual interest rate (in %, e.g. 5): ")) / 100
        n = int(input("Enter number of years: "))
        m = int(input("Compounding frequency per year (e.g. 1, 2, 12): "))

        P = FV / (1 + r / m) ** (n * m)
        print(f"Present Value: ${P:,.2f}")

        # Generate chart
        create_tvm_chart(P, r, n, m, "PV")

    elif calc_type == "3":  # Calculate rate
        P = float(input("Enter present value (P): $"))
        FV = float(input("Enter future value (FV): $"))
        n = int(input("Enter number of years: "))
        m = int(input("Compounding frequency per year (e.g. 1, 2, 12): "))

        r = m * ((FV / P) ** (1 / (n * m)) - 1)
        print(f"Required annual interest rate: {r * 100:.4f}%")

    elif calc_type == "4":  # Calculate time
        P = float(input("Enter present value (P): $"))
        FV = float(input("Enter future value (FV): $"))
        r = float(input("Enter annual interest rate (in %, e.g. 5): ")) / 100
        m = int(input("Compounding frequency per year (e.g. 1, 2, 12): "))

        n = math.log(FV / P) / (m * math.log(1 + r / m))
        print(f"Time required: {n:.2f} years")

    else:
        print("Invalid choice.")


def create_tvm_chart(P, r, n, m, calc_type): # Create TVM Chart
    years = []
    values = []

    for year in range(n + 1):
        if calc_type == "FV": # FV chart
            value = P * (1 + r / m) ** (year * m)
        else:  # PV chart
            FV = P * (1 + r / m) ** (n * m)
            value = FV / (1 + r / m) ** (year * m)

        years.append(year)
        values.append(value)

    plt.figure(figsize=(10, 6))
    plt.plot(years, values, 'b-', linewidth=2, marker='o')
    plt.title(f'Time Value of Money - {calc_type} Growth')
    plt.xlabel('Years')
    plt.ylabel('Value ($)')
    plt.grid(True, alpha=0.3)
    plt.ticklabel_format(style='plain', axis='y')

    # Make y-axis labels $
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    plt.tight_layout()
    plt.show()


# Annuity Calcs
def annuity_calculator():
    print("\n--- ANNUITY CALCULATOR ---")
    print("1. Annuity Immediate")
    print("2. Annuity Due")
    print("3. Growing Annuity")
    print("4. Deferred Annuity")

    annuity_type = input("Choose annuity type (1-4): ")

    print("\nWhat would you like to calculate?")
    print("1. Present Value (PV)")
    print("2. Future Value (FV)")

    calc_choice = input("Choose calculation (1-2): ")

    if annuity_type == "1":  # Annuity Immediate
        immediate_annuity(calc_choice)
    elif annuity_type == "2":  # Annuity Due
        due_annuity(calc_choice)
    elif annuity_type == "3":  # Growing Annuity
        growing_annuity(calc_choice)
    elif annuity_type == "4":  # Deferred Annuity
        deferred_annuity(calc_choice)
    else:
        print("Invalid choice.")


def immediate_annuity(calc_choice): # PV/FV for Immediate
    PMT = float(input("Enter payment per period: $"))
    r = float(input("Interest rate per period (in %, e.g. 6): ")) / 100
    n = int(input("Number of periods: "))

    if calc_choice == "1":  # Present Value
        pv = PMT * ((1 - (1 + r) ** -n) / r)
        print(f"Present Value of Immediate Annuity: ${pv:,.2f}")
    elif calc_choice == "2":  # Future Value
        fv = PMT * (((1 + r) ** n - 1) / r)
        print(f"Future Value of Immediate Annuity: ${fv:,.2f}")
    else:
        print("Invalid choice.")


def due_annuity(calc_choice): # PV/FV for Due
    PMT = float(input("Enter payment per period: $"))
    r = float(input("Interest rate per period (in %, e.g. 6): ")) / 100
    n = int(input("Number of periods: "))

    if calc_choice == "1":  # Present Value
        pv = PMT * ((1 - (1 + r) ** -n) / r) * (1 + r)
        print(f"Present Value of Annuity Due: ${pv:,.2f}")
    elif calc_choice == "2":  # Future Value
        fv = PMT * (((1 + r) ** n - 1) / r) * (1 + r)
        print(f"Future Value of Annuity Due: ${fv:,.2f}")
    else:
        print("Invalid choice.")


def growing_annuity(calc_choice): # PV/FV for Growing
    PMT = float(input("Enter initial payment: $"))
    r = float(input("Interest rate per period (in %, e.g. 6): ")) / 100
    g = float(input("Growth rate per period (in %, e.g. 3): ")) / 100
    n = int(input("Number of periods: "))

    if calc_choice == "1":  # Present Value
        if r == g:
            pv = n * PMT / (1 + r)
        else:
            pv = PMT * (1 - ((1 + g) / (1 + r)) ** n) / (r - g)
        print(f"Present Value of Growing Annuity: ${pv:,.2f}")
    elif calc_choice == "2":  # Future Value
        if r == g:
            fv = n * PMT * (1 + r) ** (n - 1)
        else:
            fv = PMT * (((1 + r) ** n - (1 + g) ** n) / (r - g))
        print(f"Future Value of Growing Annuity: ${fv:,.2f}")
    else:
        print("Invalid choice.")


def deferred_annuity(calc_choice): # PV/FV for Deferred
    PMT = float(input("Enter payment per period: $"))
    r = float(input("Interest rate per period (in %, e.g. 6): ")) / 100
    n = int(input("Number of payment periods: "))
    m = int(input("Number of deferral periods: "))

    if calc_choice == "1":  # Present Value
        # PV of immediate annuity discounted back by deferral period
        pv_immediate = PMT * ((1 - (1 + r) ** -n) / r)
        pv = pv_immediate / (1 + r) ** m
        print(f"Present Value of Deferred Annuity: ${pv:,.2f}")
    elif calc_choice == "2":  # Future Value
        # FV of annuity immediate, compounded forward by m deferral periods
        fv_immediate = PMT * (((1 + r) ** n - 1) / r)
        fv = fv_immediate * ((1 + r) ** m)
        print(f"Future Value of Deferred Annuity: ${fv:,.2f}")
    else:
        print("Invalid choice.")

# Bond Calcs
def bond_pricing():
    print("\n--- BOND PRICING ---")
    face_value = float(input("Enter face value: $"))
    coupon_rate = float(input("Enter annual coupon rate (in %, e.g. 5): ")) / 100
    years = int(input("Enter years to maturity: "))
    ytm = float(input("Enter yield to maturity (in %, e.g. 4): ")) / 100
    frequency = int(input("Coupon payments per year (1=annual, 2=semi-annual): "))

    # Calculate coupon
    coupon_payment = (face_value * coupon_rate) / frequency
    periods = years * frequency
    period_rate = ytm / frequency

    # Calculate PV of coupons
    pv_coupons = coupon_payment * ((1 - (1 + period_rate) ** -periods) / period_rate)

    # Calculate PV of face value
    pv_face = face_value / (1 + period_rate) ** periods

    # Bond price
    bond_price = pv_coupons + pv_face

    # Calculate Macaulay Duration
    macaulay_duration = 0
    for t in range(1, periods + 1):
        if t < periods:  # Coupon payments
            cash_flow = coupon_payment
        else:  # Final payment (coupon + face value)
            cash_flow = coupon_payment + face_value

        pv_cash_flow = cash_flow / (1 + period_rate) ** t
        weighted_time = (t / frequency) * pv_cash_flow
        macaulay_duration += weighted_time

    macaulay_duration = macaulay_duration / bond_price

    # Calculate Modified Duration
    modified_duration = macaulay_duration / (1 + ytm / frequency)

    print(f"\nBond Price: ${bond_price:,.2f}")
    print(f"Present Value of Coupons: ${pv_coupons:,.2f}")
    print(f"Present Value of Face Value: ${pv_face:,.2f}")
    print(f"Macaulay Duration: {macaulay_duration:.4f} years")
    print(f"Modified Duration: {modified_duration:.4f} years")

# Loan Amortization Schedule
def loan_amortization():
    print("\n--- LOAN AMORTIZATION ---")
    principal = float(input("Enter loan amount: $"))
    annual_rate = float(input("Enter annual interest rate (in %, e.g. 6): ")) / 100
    years = int(input("Enter loan term in years: "))

    monthly_rate = annual_rate / 12
    n_payments = years * 12

    # Calculate PMT
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / (
                (1 + monthly_rate) ** n_payments - 1)

    print(f"Monthly Payment: ${monthly_payment:,.2f}")
    print(f"Total Payments: ${monthly_payment * n_payments:,.2f}")
    print(f"Total Interest: ${(monthly_payment * n_payments) - principal:,.2f}")

    # Generate amortization schedule
    generate_amortization_schedule(principal, monthly_rate, n_payments, monthly_payment)


def generate_amortization_schedule(principal, monthly_rate, n_payments, monthly_payment): # Loan Schedule and Charts
    schedule = []
    balance = principal

    for payment_num in range(1, n_payments + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment

        schedule.append({
            'Payment': payment_num,
            'Beginning Balance': round(balance + principal_payment, 2),
            'Monthly Payment': round(monthly_payment, 2),
            'Interest': round(interest_payment, 2),
            'Principal': round(principal_payment, 2),
            'Ending Balance': round(balance, 2)
        })

    # Save to CSV
    filename = "loan_amortization_.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=['Payment', 'Beginning Balance', 'Monthly Payment', 'Interest', 'Principal',
                                            'Ending Balance'])
        writer.writeheader()
        writer.writerows(schedule)

    print(f"Amortization schedule saved to {filename}")

    # Create chart showing principal vs interest over time
    create_amortization_chart(schedule)


def create_amortization_chart(schedule): # Loan Charts
    payments = [row['Payment'] for row in schedule]
    interest_payments = [row['Interest'] for row in schedule]
    principal_payments = [row['Principal'] for row in schedule]

    plt.figure(figsize=(12, 8))

    # Subplot 1: Principal vs Interest over time
    plt.subplot(2, 1, 1)
    plt.plot(payments, interest_payments, 'r-', label='Interest', linewidth=2)
    plt.plot(payments, principal_payments, 'b-', label='Principal', linewidth=2)
    plt.title('Principal vs Interest Payments Over Time')
    plt.xlabel('Payment Number')
    plt.ylabel('Payment Amount ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Subplot 2: Outstanding balance
    balances = [row['Ending Balance'] for row in schedule]
    plt.subplot(2, 1, 2)
    plt.plot(payments, balances, 'g-', linewidth=2)
    plt.title('Outstanding Loan Balance')
    plt.xlabel('Payment Number')
    plt.ylabel('Balance ($)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# Retirement Calculator
def retirement_planning():
    print("\n--- RETIREMENT PLANNING CALCULATOR ---")

    current_age = int(input("Enter current age: "))
    retirement_age = int(input("Enter planned retirement age: "))
    current_savings = float(input("Enter current retirement savings: $"))
    monthly_contribution = float(input("Enter monthly contribution: $"))
    annual_return = float(input("Enter expected annual return (in %, e.g. 7): ")) / 100

    years_to_retirement = retirement_age - current_age
    months_to_retirement = years_to_retirement * 12
    monthly_return = annual_return / 12

    # Future value of current savings
    fv_current = current_savings * (1 + annual_return) ** years_to_retirement

    # Future value of monthly contributions (annuity)
    fv_contributions = monthly_contribution * (((1 + monthly_return) ** months_to_retirement - 1) / monthly_return)

    total_retirement_funds = fv_current + fv_contributions

    print(f"\nRetirement Analysis:")
    print(f"Years to retirement: {years_to_retirement}")
    print(f"Future value of current savings: ${fv_current:,.2f}")
    print(f"Future value of contributions: ${fv_contributions:,.2f}")
    print(f"Total retirement funds: ${total_retirement_funds:,.2f}")

    # Calculate sustainable withdrawal (4% rule)
    annual_withdrawal = total_retirement_funds * 0.04
    monthly_withdrawal = annual_withdrawal / 12

    print(f"\nSustainable annual withdrawal (4% rule): ${annual_withdrawal:,.2f}")
    print(f"Sustainable monthly withdrawal: ${monthly_withdrawal:,.2f}")

    # Create retirement projection chart
    create_retirement_chart(current_age, retirement_age, current_savings, monthly_contribution, annual_return)


def create_retirement_chart(current_age, retirement_age, current_savings, monthly_contribution, annual_return): # Retirement Chart
    ages = []
    balances = []

    balance = current_savings
    monthly_return = annual_return / 12

    for age in range(current_age, retirement_age + 1):
        ages.append(age)
        balances.append(balance)

        # Add monthly contributions (if not at retirement age)
        if age < retirement_age:
            for month in range(12):
                balance = balance * (1 + monthly_return) + monthly_contribution

    plt.figure(figsize=(10, 6))
    plt.plot(ages, balances, 'g-', linewidth=2, marker='o')
    plt.title('Retirement Savings Growth Over Time')
    plt.xlabel('Age')
    plt.ylabel('Retirement Savings ($)')
    plt.grid(True, alpha=0.3)
    plt.ticklabel_format(style='plain', axis='y')

    # Format y-axis as $
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    plt.tight_layout()
    plt.show()

# Menu
def show_menu():
    print("\n" + "=" * 50)
    print("COMPREHENSIVE ACTUARIAL CALCULATOR")
    print("=" * 50)
    print("1. Time Value of Money")
    print("2. Annuity Calculator")
    print("3. Bond Pricing")
    print("4. Loan Amortization")
    print("5. Retirement Planning")
    print("6. Exit")
    print("=" * 50)


def main():
    print("Welcome to the Comprehensive Actuarial Calculator!")
    print("This tool provides various financial and actuarial calculations.")

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            tvm_calculator()
        elif choice == "2":
            annuity_calculator()
        elif choice == "3":
            bond_pricing()
        elif choice == "4":
            loan_amortization()
        elif choice == "5":
            retirement_planning()
        elif choice == "6":
            print("Thank you for using the Actuarial Calculator!")
            break
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    main()