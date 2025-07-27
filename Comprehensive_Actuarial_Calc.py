import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt


def show_footer():  # Footer
    st.markdown("---")
    st.markdown(
        "Made by Kazim Rattansi | Honors Actuarial Science Student at St. John's University")


def show_homepage():  # Homepage
    st.title("Comprehensive Actuarial Calculator 🧮")
    st.markdown("""
    This powerful tool helps you perform a variety of financial and actuarial calculations with ease. 
    Whether you're planning for retirement, evaluating bonds, or analyzing loans, we've got you covered!

    ### Available Calculators:
    - **Time Value of Money ⏳**: Calculate FV, PV, interest rates, or time periods with visualizations.
    - **Annuity Calculator 💰**: Analyze the PV and FV immediate, due, growing, or deferred annuities.
    - **Bond Pricing 💵**: Determine bond prices and durations.
    - **Loan Amortization 🏦**: Generate detailed csv loan schedules and visualize payments.
    - **Retirement Planning 🌴**: Project your retirement savings and withdrawal strategy.

    Select a calculator from the sidebar to get started!
    """)
    show_footer()


def tvm_calculator():  # TVM Calculator
    st.title("Comprehensive Actuarial Calculator 🧮")
    st.header("Time Value of Money Calculator ⏳")
    col1, col2 = st.columns([1, 1])

    with col1:
        calc_type = st.selectbox("Choose calculation type:", [
            "Future Value (FV)",
            "Present Value (PV)",
            "Interest Rate (r)",
            "Number of periods (n)"
        ])

        if calc_type == "Future Value (FV)":
            PV = st.number_input("Enter present value (PV): $",
                                min_value=0.0, value=1000.0)
            r = st.number_input(
                "Enter annual interest rate (in %, e.g. 5): ", min_value=0.0, value=5.0) / 100
            n = st.number_input("Enter number of years:",
                                min_value=1, value=5, step=1)
            m = st.number_input(
                "Compounding frequency per year (e.g. 1, 2, 12):", min_value=1, value=12, step=1)
            calc_button = st.button("Calculate FV")
        elif calc_type == "Present Value (PV)":
            FV = st.number_input("Enter future value (FV): $",
                                 min_value=0.0, value=1000.0)
            r = st.number_input(
                "Enter annual interest rate (in %, e.g. 5): ", min_value=0.0, value=5.0) / 100
            n = st.number_input("Enter number of years:",
                                min_value=1, value=5, step=1)
            m = st.number_input(
                "Compounding frequency per year (e.g. 1, 2, 12):", min_value=1, value=12, step=1)
            calc_button = st.button("Calculate PV")
        elif calc_type == "Interest Rate (r)":
            PV = st.number_input("Enter present value (PV): $",
                                min_value=0.0, value=1000.0)
            FV = st.number_input("Enter future value (FV): $",
                                 min_value=0.0, value=2000.0)
            n = st.number_input("Enter number of years:",
                                min_value=1, value=5, step=1)
            m = st.number_input(
                "Compounding frequency per year (e.g. 1, 2, 12):", min_value=1, value=12, step=1)
            calc_button = st.button("Calculate Rate")
        elif calc_type == "Number of periods (n)":
            PV = st.number_input("Enter present value (PV): $",
                                min_value=0.0, value=1000.0)
            FV = st.number_input("Enter future value (FV): $",
                                 min_value=0.0, value=2000.0)
            r = st.number_input(
                "Enter annual interest rate (in %, e.g. 5): ", min_value=0.0, value=5.0) / 100
            m = st.number_input(
                "Compounding frequency per year (e.g. 1, 2, 12):", min_value=1, value=12, step=1)
            calc_button = st.button("Calculate Time")

    with col2:
        if calc_button:
            if calc_type == "Future Value (FV)":
                FV = PV * (1 + r / m) ** (n * m)
                st.success(f"Future Value after {n} years: ${FV:,.2f}")
            elif calc_type == "Present Value (PV)":
                PV = FV / (1 + r / m) ** (n * m)
                st.success(f"Present Value: ${PV:,.2f}")
            elif calc_type == "Interest Rate (r)":
                r = m * ((FV / PV) ** (1 / (n * m)) - 1)
                st.success(f"Required annual interest rate: {r * 100:.4f}%")
            elif calc_type == "Number of periods (n)":
                n = math.log(FV / PV) / (m * math.log(1 + r / m))
                st.success(f"Time required: {n:.2f} years")

    if calc_button and calc_type in ["Future Value (FV)", "Present Value (PV)"]:
        st.markdown("---")
        if calc_type == "Future Value (FV)":
            create_tvm_chart(PV, r, n, m, "FV")
        else:
            create_tvm_chart(FV, r, n, m, "PV")

    show_footer()


def create_tvm_chart(value, r, n, m, calc_type):
    years = []
    values = []

    for year in range(n + 1):
        if calc_type == "FV":
            result = value * (1 + r / m) ** (year * m)
        else:
            result = value / (1 + r / m) ** (year * m)
        years.append(year)
        values.append(result)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, values, 'b-', linewidth=2, marker='o')
    ax.set_title(f'Time Value of Money - {calc_type} Growth')
    ax.set_xlabel('Years')
    ax.set_ylabel('Value ($)')
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    plt.tight_layout()
    st.pyplot(fig)


def annuity_calculator():  # Annuity Calculator
    st.title("Comprehensive Actuarial Calculator 🧮")
    st.header("Annuity Calculator 💰")
    col1, col2 = st.columns([1, 1])

    with col1:
        annuity_type = st.selectbox("Choose annuity type:", [
            "Annuity Immediate",
            "Annuity Due",
            "Growing Annuity",
            "Deferred Annuity"
        ])
        calc_choice = st.selectbox("Choose calculation:", [
            "Present Value (PV)", "Future Value (FV)"])

        if annuity_type == "Annuity Immediate":
            PMT = st.number_input(
                "Enter payment per period: $", min_value=0.0, value=1000.0)
            r = st.number_input(
                "Interest rate per period (in %, e.g. 6): ", min_value=0.0, value=6.0) / 100
            n = st.number_input("Number of periods:",
                                min_value=1, value=10, step=1)
            calc_button = st.button("Calculate")
        elif annuity_type == "Annuity Due":
            PMT = st.number_input(
                "Enter payment per period: $", min_value=0.0, value=1000.0)
            r = st.number_input(
                "Interest rate per period (in %, e.g. 6): ", min_value=0.0, value=6.0) / 100
            n = st.number_input("Number of periods:",
                                min_value=1, value=10, step=1)
            calc_button = st.button("Calculate")
        elif annuity_type == "Growing Annuity":
            PMT = st.number_input("Enter initial payment: $",
                                  min_value=0.0, value=1000.0)
            r = st.number_input(
                "Interest rate per period (in %, e.g. 6): ", min_value=0.0, value=6.0) / 100
            g = st.number_input(
                "Growth rate per period (in %, e.g. 3): ", min_value=0.0, value=3.0) / 100
            n = st.number_input("Number of periods:",
                                min_value=1, value=10, step=1)
            calc_button = st.button("Calculate")
        elif annuity_type == "Deferred Annuity":
            PMT = st.number_input(
                "Enter payment per period: $", min_value=0.0, value=1000.0)
            r = st.number_input(
                "Interest rate per period (in %, e.g. 6): ", min_value=0.0, value=6.0) / 100
            n = st.number_input("Number of payment periods:",
                                min_value=1, value=10, step=1)
            m = st.number_input("Number of deferral periods:",
                                min_value=0, value=5, step=1)
            calc_button = st.button("Calculate")

    with col2:
        if calc_button:
            if annuity_type == "Annuity Immediate":
                if calc_choice == "Present Value (PV)":
                    pv = PMT * ((1 - (1 + r) ** -n) / r)
                    st.success(
                        f"Present Value of Immediate Annuity: ${pv:,.2f}")
                elif calc_choice == "Future Value (FV)":
                    fv = PMT * (((1 + r) ** n - 1) / r)
                    st.success(
                        f"Future Value of Immediate Annuity: ${fv:,.2f}")
            elif annuity_type == "Annuity Due":
                if calc_choice == "Present Value (PV)":
                    pv = PMT * ((1 - (1 + r) ** -n) / r) * (1 + r)
                    st.success(f"Present Value of Annuity Due: ${pv:,.2f}")
                elif calc_choice == "Future Value (FV)":
                    fv = PMT * (((1 + r) ** n - 1) / r) * (1 + r)
                    st.success(f"Future Value of Annuity Due: ${fv:,.2f}")
            elif annuity_type == "Growing Annuity":
                if calc_choice == "Present Value (PV)":
                    if r == g:
                        pv = n * PMT / (1 + r)
                    else:
                        pv = PMT * (1 - ((1 + g) / (1 + r)) ** n) / (r - g)
                    st.success(f"Present Value of Growing Annuity: ${pv:,.2f}")
                elif calc_choice == "Future Value (FV)":
                    if r == g:
                        fv = n * PMT * (1 + r) ** (n - 1)
                    else:
                        fv = PMT * (((1 + r) ** n - (1 + g) ** n) / (r - g))
                    st.success(f"Future Value of Growing Annuity: ${fv:,.2f}")
            elif annuity_type == "Deferred Annuity":
                if calc_choice == "Present Value (PV)":
                    pv_immediate = PMT * ((1 - (1 + r) ** -n) / r)
                    pv = pv_immediate / (1 + r) ** m
                    st.success(
                        f"Present Value of Deferred Annuity: ${pv:,.2f}")
                elif calc_choice == "Future Value (FV)":
                    fv_immediate = PMT * (((1 + r) ** n - 1) / r)
                    fv = fv_immediate * ((1 + r) ** m)
                    st.success(f"Future Value of Deferred Annuity: ${fv:,.2f}")

    show_footer()


def bond_pricing():  # Bond Pricing
    st.title("Comprehensive Actuarial Calculator 🧮")
    st.header("Bond Pricing 💵")
    col1, col2 = st.columns([1, 1])

    with col1:
        face_value = st.number_input(
            "Enter face value: $", min_value=0.0, value=1000.0)
        coupon_rate = st.number_input(
            "Enter annual coupon rate (in %, e.g. 5): ", min_value=0.0, value=5.0) / 100
        years = st.number_input(
            "Enter years to maturity:", min_value=1, value=10, step=1)
        ytm = st.number_input(
            "Enter yield to maturity (in %, e.g. 4): ", min_value=0.0, value=4.0) / 100
        frequency = st.number_input(
            "Coupon payments per year (1=annual, 2=semi-annual):", min_value=1, value=2, step=1)
        calc_button = st.button("Calculate")

    with col2:
        if calc_button:
            coupon_payment = (face_value * coupon_rate) / frequency
            periods = years * frequency
            period_rate = ytm / frequency

            pv_coupons = coupon_payment * \
                         ((1 - (1 + period_rate) ** -periods) / period_rate)
            pv_face = face_value / (1 + period_rate) ** periods
            bond_price = pv_coupons + pv_face

            macaulay_duration = 0
            for t in range(1, periods + 1):
                if t < periods:
                    cash_flow = coupon_payment
                else:
                    cash_flow = coupon_payment + face_value
                pv_cash_flow = cash_flow / (1 + period_rate) ** t
                weighted_time = (t / frequency) * pv_cash_flow
                macaulay_duration += weighted_time
            macaulay_duration = macaulay_duration / bond_price
            modified_duration = macaulay_duration / (1 + ytm / frequency)

            st.success(f"Bond Price: ${bond_price:,.2f}")
            st.write(f"Present Value of Coupons: ${pv_coupons:,.2f}")
            st.write(f"Present Value of Face Value: ${pv_face:,.2f}")
            st.write(f"Macaulay Duration: {macaulay_duration:.4f} years")
            st.write(f"Modified Duration: {modified_duration:.4f} years")

    show_footer()


def loan_amortization():  # Loan Amortization
    st.title("Comprehensive Actuarial Calculator 🧮")
    st.header("Loan Amortization 🏦")
    col1, col2 = st.columns([1, 1])

    with col1:
        principal = st.number_input(
            "Enter loan amount: $", min_value=0.0, value=100000.0)
        annual_rate = st.number_input(
            "Enter annual interest rate (in %, e.g. 6): ", min_value=0.0, value=6.0) / 100
        years = st.number_input(
            "Enter loan term in years:", min_value=1, value=30, step=1)
        calc_button = st.button("Calculate")

    with col2:
        if calc_button:
            monthly_rate = annual_rate / 12
            n_payments = years * 12
            monthly_payment = principal * \
                              (monthly_rate * (1 + monthly_rate) ** n_payments) / \
                              ((1 + monthly_rate) ** n_payments - 1)

            st.success(f"Monthly Payment: ${monthly_payment:,.2f}")
            st.write(f"Total Payments: ${monthly_payment * n_payments:,.2f}")
            st.write(
                f"Total Interest: ${(monthly_payment * n_payments) - principal:,.2f}")

    if calc_button:
        st.markdown("---")
        schedule = generate_amortization_schedule(
            principal, monthly_rate, n_payments, monthly_payment)
        df = pd.DataFrame(schedule)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Amortization Schedule as CSV",
            data=csv,
            file_name="loan_amortization.csv",
            mime="text/csv"
        )

        create_amortization_chart(schedule)

    show_footer()


def generate_amortization_schedule(principal, monthly_rate, n_payments, monthly_payment):
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

    return schedule


def create_amortization_chart(schedule):
    payments = [row['Payment'] for row in schedule]
    interest_payments = [row['Interest'] for row in schedule]
    principal_payments = [row['Principal'] for row in schedule]
    balances = [row['Ending Balance'] for row in schedule]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.plot(payments, interest_payments, 'r-', label='Interest', linewidth=2)
    ax1.plot(payments, principal_payments, 'b-',
             label='Principal', linewidth=2)
    ax1.set_title('Principal vs Interest Payments Over Time')
    ax1.set_xlabel('Payment Number')
    ax1.set_ylabel('Payment Amount ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(payments, balances, 'g-', linewidth=2)
    ax2.set_title('Outstanding Loan Balance')
    ax2.set_xlabel('Payment Number')
    ax2.set_ylabel('Balance ($)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)


def retirement_planning():  # Retirement Planning
    st.title("Comprehensive Actuarial Calculator 🧮")
    st.header("Retirement Planning Calculator 🌴")
    col1, col2 = st.columns([1, 1])

    with col1:
        current_age = st.number_input(
            "Enter current age:", min_value=0, value=30, step=1)
        retirement_age = st.number_input(
            "Enter planned retirement age:", min_value=0, value=65, step=1)
        current_savings = st.number_input(
            "Enter current retirement savings: $", min_value=0.0, value=10000.0)
        monthly_contribution = st.number_input(
            "Enter monthly contribution: $", min_value=0.0, value=500.0)
        annual_return = st.number_input(
            "Enter expected annual return (in %, e.g. 7): ", min_value=0.0, value=7.0) / 100
        calc_button = st.button("Calculate")

    with col2:
        if calc_button:
            years_to_retirement = retirement_age - current_age
            months_to_retirement = years_to_retirement * 12
            monthly_return = annual_return / 12

            fv_current = current_savings * \
                         (1 + annual_return) ** years_to_retirement
            fv_contributions = monthly_contribution * \
                               (((1 + monthly_return) ** months_to_retirement - 1) / monthly_return)
            total_retirement_funds = fv_current + fv_contributions
            annual_withdrawal = total_retirement_funds * 0.04
            monthly_withdrawal = annual_withdrawal / 12

            st.success("Retirement Analysis:")
            st.write(f"Years to retirement: {years_to_retirement}")
            st.write(f"Future value of current savings: ${fv_current:,.2f}")
            st.write(
                f"Future value of contributions: ${fv_contributions:,.2f}")
            st.write(f"Total retirement funds: ${total_retirement_funds:,.2f}")
            st.write(
                f"Sustainable annual withdrawal (4% rule): ${annual_withdrawal:,.2f}")
            st.write(
                f"Sustainable monthly withdrawal: ${monthly_withdrawal:,.2f}")

    if calc_button:
        st.markdown("---")
        create_retirement_chart(current_age, retirement_age,
                                current_savings, monthly_contribution, annual_return)

    show_footer()


def create_retirement_chart(current_age, retirement_age, current_savings, monthly_contribution, annual_return):
    ages = []
    balances = []
    balance = current_savings
    monthly_return = annual_return / 12

    for age in range(current_age, retirement_age + 1):
        ages.append(age)
        balances.append(balance)
        if age < retirement_age:
            for month in range(12):
                balance = balance * (1 + monthly_return) + monthly_contribution

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ages, balances, 'g-', linewidth=2, marker='o')
    ax.set_title('Retirement Savings Growth Over Time')
    ax.set_xlabel('Age')
    ax.set_ylabel('Retirement Savings ($)')
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    plt.tight_layout()
    st.pyplot(fig)


def main():  # Main App
    st.set_page_config(page_title="Actuarial Calculator",
                       page_icon="📊", layout="wide")
    menu = [
        "Home 🏠",
        "Time Value of Money ⏳",
        "Annuity Calculator 💰",
        "Bond Pricing 💵",
        "Loan Amortization 🏦",
        "Retirement Planning 🌴"
    ]
    choice = st.sidebar.selectbox("Select Calculator", menu)

    if choice == "Home 🏠":
        show_homepage()
    elif choice == "Time Value of Money ⏳":
        tvm_calculator()
    elif choice == "Annuity Calculator 💰":
        annuity_calculator()
    elif choice == "Bond Pricing 💵":
        bond_pricing()
    elif choice == "Loan Amortization 🏦":
        loan_amortization()
    elif choice == "Retirement Planning 🌴":
        retirement_planning()


if __name__ == "__main__":
    main()
