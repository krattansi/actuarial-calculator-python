import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go
import numpy as np


def show_footer():  # Footer
    st.markdown("---")
    st.markdown(
        "Made by Kazim Rattansi | Honors Actuarial Science Student at St. John's University")


def show_homepage():  # Homepage
    st.title("Actuarial Calculator 🧮")
    st.markdown("""
    This powerful tool helps you perform a variety of financial and actuarial calculations with ease. 
    Whether you're planning for retirement, evaluating bonds, or analyzing loans, we've got you covered!
    ### Available Calculators:
    - **Time Value of Money ⏳**: Calculate FV, PV, periodic payments, interest rates, or time periods with visualizations and sensitivity analysis.
    - **Annuity Calculator 💰**: Analyze the PV and FV immediate, due, growing, or deferred annuities with sensitivity analysis.
    - **Bond Pricing 💵**: Determine bond prices and durations with sensitivity analysis.
    - **Loan Amortization 🏦**: Generate detailed csv loan schedules and visualize payments.
    - **Retirement Planning 🌴**: Project your retirement savings and withdrawal strategy with visualizations and sensitivity analysis.
    Select a calculator from the sidebar to get started!
    """)
    show_footer()


def create_sensitivity_analysis(base_value, shock_range, calculation_function, title,
                                # Sensitivity Analysis
                                xlabel="Interest Rate Shock (%)", ylabel="Value ($)"):
    shocked_values = [calculation_function(shock) for shock in shock_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=shock_range * 100, y=shocked_values,
                             mode='lines', line=dict(color='red', width=2)))

    fig.update_layout(
        title_text=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        yaxis_tickprefix='$', yaxis_tickformat=',.0f')
    st.plotly_chart(fig, use_container_width=True)


def tvm_calculator():  # TVM Calculator
    st.title("Actuarial Calculator 🧮")
    st.header("Time Value of Money Calculator ⏳")
    col1, col2 = st.columns([1, 1])
    with col1:
        calc_type = st.selectbox("Choose calculation type:", [
            "Future Value (FV)",
            "Present Value (PV)",
            "Interest Rate (r)",
            "Number of periods (n)"
        ])

        use_payment = st.checkbox("Include periodic payments")
        PMT = 0.0
        payment_at_beginning = False
        if use_payment:
            PMT = st.number_input("Enter payment amount per period: $",
                                  min_value=0.0, value=100.0)
            payment_at_beginning = st.selectbox("Payment timing:", [
                                                "End of period", "Beginning of period"]) == "Beginning of period"

        if calc_type == "Future Value (FV)":
            PV = st.number_input(
                "Enter present value (PV): $", min_value=0.0, value=1000.0)
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
            PV = st.number_input(
                "Enter present value (PV): $", min_value=0.0, value=1000.0)
            FV = st.number_input("Enter future value (FV): $",
                                 min_value=0.0, value=2000.0)
            n = st.number_input("Enter number of years:",
                                min_value=1, value=5, step=1)
            m = st.number_input(
                "Compounding frequency per year (e.g. 1, 2, 12):", min_value=1, value=12, step=1)
            calc_button = st.button("Calculate Rate")
        elif calc_type == "Number of periods (n)":
            PV = st.number_input(
                "Enter present value (PV): $", min_value=0.0, value=1000.0)
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
                FV = PV * (1 + r/m) ** (n*m) + (PMT * ((1 + r/m) ** (n*m) - 1) / (r/m) * (1 + r/m)
                                                if payment_at_beginning else PMT * ((1 + r/m) ** (n*m) - 1) / (r/m)) if use_payment else PV * (1 + r/m) ** (n*m)
                st.success(f"Future Value after {n} years: ${FV:,.2f}")
            elif calc_type == "Present Value (PV)":
                PV = FV / (1 + r/m) ** (n*m) - (PMT * ((1 + r/m) ** (n*m) - 1) / (r/m) / (1 + r/m) ** (n*m) * (1 + r/m)
                                                if payment_at_beginning else PMT * ((1 + r/m) ** (n*m) - 1) / (r/m) / (1 + r/m) ** (n*m)) if use_payment else FV / (1 + r/m) ** (n*m)
                st.success(f"Present Value: ${PV:,.2f}")
            elif calc_type == "Interest Rate (r)":
                if use_payment:
                    total_periods = n * m

                    def f(x): return PV * (1 + x) ** total_periods + PMT * ((1 + x) ** total_periods - 1) / x * (1 + x) - \
                        FV if payment_at_beginning else PV * \
                        (1 + x) ** total_periods + PMT * \
                        ((1 + x) ** total_periods - 1) / x - FV

                    def df(x): return PV * total_periods * (1 + x) ** (total_periods - 1) + PMT * (
                        total_periods * x * (1 + x) ** (total_periods - 1) - ((1 + x) ** total_periods - 1)) / (x ** 2)
                    x = 0.05 / m
                    for _ in range(20):
                        x_new = x - f(x) / df(x)
                        if abs(x_new - x) < 1e-8:
                            break
                        x = x_new
                    r = x * m
                else:
                    r = m * ((FV / PV) ** (1 / (n * m)) - 1)
                st.success(f"Required annual interest rate: {r * 100:.4f}%")
            elif calc_type == "Number of periods (n)":
                if use_payment:
                    period_rate = r / m

                    def f(n_periods): return PV * (1 + period_rate) ** n_periods + PMT * ((1 + period_rate) ** n_periods - 1) / period_rate * (1 + period_rate) - \
                        FV if payment_at_beginning else PV * (1 + period_rate) ** n_periods + PMT * (
                            (1 + period_rate) ** n_periods - 1) / period_rate - FV
                    low, high = 1, 1000
                    while high - low > 0.01:
                        mid = (low + high) / 2
                        if f(mid) < 0:
                            low = mid
                        else:
                            high = mid
                    n = low / m
                else:
                    n = math.log(FV / PV) / (m * math.log(1 + r / m))
                st.success(f"Time required: {n:.2f} years")

    if calc_button and calc_type in ["Future Value (FV)", "Present Value (PV)"]:
        st.markdown("---")
        if calc_type == "Future Value (FV)":
            create_tvm_chart(PV, r, n, m, "FV",
                             PMT if use_payment else 0, payment_at_beginning)
            create_sensitivity_analysis(
                r, np.linspace(-0.03, 0.03, 21),
                lambda shock: PV * (1 + (r+shock)/m) ** (n*m) + (PMT * ((1 + (r+shock)/m) ** (n*m) - 1) / ((r+shock)/m) * (1 + (r+shock)/m)
                                                                 if payment_at_beginning else PMT * ((1 + (r+shock)/m) ** (n*m) - 1) / ((r+shock)/m)) if use_payment else PV * (1 + (r+shock)/m) ** (n*m),
                f'Interest Rate Sensitivity Analysis - Future Value',
                "Interest Rate Shock (%)", "Future Value ($)"
            )
        else:
            create_tvm_chart(FV, r, n, m, "PV",
                             PMT if use_payment else 0, payment_at_beginning)
            create_sensitivity_analysis(
                r, np.linspace(-0.03, 0.03, 21),
                lambda shock: FV / (1 + (r+shock)/m) ** (n*m) - (PMT * ((1 + (r+shock)/m) ** (n*m) - 1) / ((r+shock)/m) / (1 + (r+shock)/m) ** (n*m) * (1 + (r+shock)/m)
                                                                 if payment_at_beginning else PMT * ((1 + (r+shock)/m) ** (n*m) - 1) / ((r+shock)/m) / (1 + (r+shock)/m) ** (n*m)) if use_payment else FV / (1 + (r+shock)/m) ** (n*m),
                f'Interest Rate Sensitivity Analysis - Present Value',
                "Interest Rate Shock (%)", "Present Value ($)"
            )
    show_footer()


def create_tvm_chart(value, r, n, m, calc_type, PMT=0, payment_at_beginning=False):
    years = []
    values = []
    for year in range(n + 1):
        if calc_type == "FV":
            result = value * (1 + r/m) ** (year*m) + (PMT * ((1 + r/m) ** (year*m) - 1) / (r/m) * (1 + r/m)
                                                      if payment_at_beginning else PMT * ((1 + r/m) ** (year*m) - 1) / (r/m)) if PMT > 0 else value * (1 + r/m) ** (year*m)
        else:
            result = value / (1 + r/m) ** (year*m) - (PMT * ((1 + r/m) ** (year*m) - 1) / (r/m) / (1 + r/m) ** (year*m) * (1 + r/m)
                                                      if payment_at_beginning else PMT * ((1 + r/m) ** (year*m) - 1) / (r/m) / (1 + r/m) ** (year*m)) if PMT > 0 else value / (1 + r/m) ** (year*m)
        years.append(year)
        values.append(result)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=values, mode='lines+markers',
                             line=dict(color='blue', width=2)))

    fig.update_layout(
        title_text=f'Time Value of Money - {calc_type} Growth',
        xaxis_title='Years',
        yaxis_title='Value ($)',
        yaxis_tickprefix='$', yaxis_tickformat=',.0f')
    st.plotly_chart(fig, use_container_width=True)


def annuity_calculator():  # Annuity Calculator
    st.title("Actuarial Calculator 🧮")
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

        # Common inputs
        PMT = st.number_input("Enter payment per period: $",
                              min_value=0.0, value=1000.0)
        r = st.number_input(
            "Interest rate per period (in %, e.g. 6): ", min_value=0.0, value=6.0) / 100
        n = st.number_input("Number of periods:",
                            min_value=1, value=10, step=1)

        # Type-specific inputs
        if annuity_type == "Growing Annuity":
            g = st.number_input(
                "Growth rate per period (in %, e.g. 3): ", min_value=0.0, value=3.0) / 100
        elif annuity_type == "Deferred Annuity":
            m = st.number_input("Number of deferral periods:",
                                min_value=0, value=5, step=1)

        calc_button = st.button("Calculate")
    with col2:
        if calc_button:
            if annuity_type == "Annuity Immediate":
                result = PMT * \
                    ((1 - (1 + r) ** -n) / r) if calc_choice == "PV" else PMT * \
                    (((1 + r) ** n - 1) / r)
                st.success(
                    f"{'Present' if calc_choice == 'PV' else 'Future'} Value of Immediate Annuity: ${result:,.2f}")
            elif annuity_type == "Annuity Due":
                result = PMT * ((1 - (1 + r) ** -n) / r) * (
                    1 + r) if calc_choice == "PV" else PMT * (((1 + r) ** n - 1) / r) * (1 + r)
                st.success(
                    f"{'Present' if calc_choice == 'PV' else 'Future'} Value of Annuity Due: ${result:,.2f}")
            elif annuity_type == "Growing Annuity":
                if calc_choice == "PV":
                    result = n * PMT / (1 + r) if r == g else PMT * \
                        (1 - ((1 + g) / (1 + r)) ** n) / (r - g)
                else:
                    result = n * PMT * \
                        (1 + r) ** (n - 1) if r == g else PMT * \
                        (((1 + r) ** n - (1 + g) ** n) / (r - g))
                st.success(
                    f"{'Present' if calc_choice == 'PV' else 'Future'} Value of Growing Annuity: ${result:,.2f}")
            elif annuity_type == "Deferred Annuity":
                if calc_choice == "PV":
                    pv_immediate = PMT * ((1 - (1 + r) ** -n) / r)
                    result = pv_immediate / (1 + r) ** m
                else:
                    fv_immediate = PMT * (((1 + r) ** n - 1) / r)
                    result = fv_immediate * ((1 + r) ** m)
                st.success(
                    f"{'Present' if calc_choice == 'PV' else 'Future'} Value of Deferred Annuity: ${result:,.2f}")

    if calc_button:
        st.markdown("---")
        if annuity_type == "Annuity Immediate":
            def sensitivity_func(shock): return PMT * ((1 - (1 + r + shock) ** -n) / (
                r + shock)) if calc_choice == "PV" else PMT * (((1 + r + shock) ** n - 1) / (r + shock))
            title = f'Interest Rate Sensitivity Analysis - Immediate Annuity {calc_choice}'
        elif annuity_type == "Annuity Due":
            def sensitivity_func(shock): return PMT * ((1 - (1 + r + shock) ** -n) / (r + shock)) * (
                1 + r + shock) if calc_choice == "PV" else PMT * (((1 + r + shock) ** n - 1) / (r + shock)) * (1 + r + shock)
            title = f'Interest Rate Sensitivity Analysis - Annuity Due {calc_choice}'
        elif annuity_type == "Growing Annuity":
            if calc_choice == "PV":
                def sensitivity_func(shock): return n * PMT / (1 + r + shock) if r + \
                    shock == g else PMT * (1 - ((1 + g) / (1 + r + shock)) ** n) / (r + shock - g)
            else:
                def sensitivity_func(shock): return n * PMT * (1 + r + shock) ** (n - 1) if r + \
                    shock == g else PMT * (((1 + r + shock) ** n - (1 + g) ** n) / (r + shock - g))
            title = f'Interest Rate Sensitivity Analysis - Growing Annuity {calc_choice}'
        elif annuity_type == "Deferred Annuity":
            if calc_choice == "PV":
                def sensitivity_func(shock): return (
                    PMT * ((1 - (1 + r + shock) ** -n) / (r + shock))) / (1 + r + shock) ** m
            else:
                def sensitivity_func(shock): return (
                    PMT * (((1 + r + shock) ** n - 1) / (r + shock))) * (1 + r + shock) ** m
            title = f'Interest Rate Sensitivity Analysis - Deferred Annuity {calc_choice}'

        create_sensitivity_analysis(
            r, np.linspace(-0.03, 0.03, 21),
            sensitivity_func,
            title,
            "Interest Rate Shock (%)",
            f"{calc_choice} Value ($)"
        )
    show_footer()


def bond_pricing():  # Bond Pricing
    st.title("Actuarial Calculator 🧮")
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

            macaulay_duration = sum((t / frequency) * (coupon_payment if t < periods else coupon_payment +
                                    face_value) / (1 + period_rate) ** t for t in range(1, periods + 1)) / bond_price
            modified_duration = macaulay_duration / (1 + ytm / frequency)

            st.success(f"Bond Price: ${bond_price:,.2f}")
            st.write(f"Present Value of Coupons: ${pv_coupons:,.2f}")
            st.write(f"Present Value of Face Value: ${pv_face:,.2f}")
            st.write(f"Macaulay Duration: {macaulay_duration:.4f} years")
            st.write(f"Modified Duration: {modified_duration:.4f} years")

            if abs(bond_price - face_value) < 0.01:
                st.info("The bond is selling at par.")
            elif bond_price > face_value:
                st.info("The bond is selling at a premium.")
            else:
                st.info("The bond is selling at a discount.")

    if calc_button:
        st.markdown("---")
        create_sensitivity_analysis(
            ytm, np.linspace(-0.03, 0.03, 21),
            lambda shock: ((face_value * coupon_rate) / frequency) * ((1 - (1 + (ytm + shock) / frequency) ** -(years * frequency)
                                                                       ) / ((ytm + shock) / frequency)) + face_value / (1 + (ytm + shock) / frequency) ** (years * frequency),
            'Bond Price Sensitivity to Interest Rate Changes',
            "Interest Rate Shock (%)",
            "Bond Price ($)"
        )
    show_footer()


def loan_amortization():  # Loan Amortization
    st.title("Actuarial Calculator 🧮")
    st.header("Loan Amortization 🏦")
    col1, col2 = st.columns([1, 1])
    with col1:
        principal = st.number_input(
            "Enter loan amount: $", min_value=0.0, value=100000.0)
        annual_rate = st.number_input(
            "Enter annual interest rate (in %, e.g. 6): ", min_value=0.0, value=6.0) / 100
        years = st.number_input(
            "Enter loan term in years:", min_value=1, value=30, step=1)
        extra_payment = st.number_input(
            "Enter extra monthly payment (optional): $", min_value=0.0, value=0.0)
        calc_button = st.button("Calculate")
    with col2:
        if calc_button:
            monthly_rate = annual_rate / 12
            n_payments = years * 12
            monthly_payment = principal * \
                (monthly_rate * (1 + monthly_rate) ** n_payments) / \
                ((1 + monthly_rate) ** n_payments - 1)
            total_monthly_payment = monthly_payment + extra_payment

            if extra_payment > 0:
                balance, payment_num = principal, 0
                while balance > 0 and payment_num < 1000:
                    payment_num += 1
                    interest_payment = balance * monthly_rate
                    principal_payment = min(
                        total_monthly_payment - interest_payment, balance)
                    balance -= principal_payment

                time_to_pay_off_years = payment_num / 12
                time_saved_years = years - time_to_pay_off_years

                st.success(f"Monthly Payment (base): ${monthly_payment:,.2f}")
                st.success(
                    f"Total Monthly Payment (with extra): ${total_monthly_payment:,.2f}")
                st.write(f"Time to Pay Off: {time_to_pay_off_years:.2f} years")
                st.write(f"Time Saved: {time_saved_years:.2f} years")
                st.write(
                    f"Total Payments: ${total_monthly_payment * payment_num:,.2f}")
                st.write(
                    f"Total Interest: ${(total_monthly_payment * payment_num) - principal:,.2f}")
            else:
                st.success(f"Monthly Payment: ${monthly_payment:,.2f}")
                st.write(
                    f"Total Payments: ${monthly_payment * n_payments:,.2f}")
                st.write(
                    f"Total Interest: ${(monthly_payment * n_payments) - principal:,.2f}")

    if calc_button:
        st.markdown("---")
        schedule = generate_amortization_schedule_with_extra(
            principal, monthly_rate, n_payments, monthly_payment, extra_payment) if extra_payment > 0 else generate_amortization_schedule(
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
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        ending_balance = balance - principal_payment
        schedule.append({
            'Payment': payment_num,
            'Beginning Balance': round(balance, 2),
            'Monthly Payment': round(monthly_payment, 2),
            'Interest': round(interest, 2),
            'Principal': round(principal_payment, 2),
            'Ending Balance': round(ending_balance, 2)
        })
        balance = ending_balance
    return schedule


def generate_amortization_schedule_with_extra(principal, monthly_rate, n_payments, monthly_payment, extra_payment):
    schedule, balance, total_payment, payment_num = [
    ], principal, monthly_payment + extra_payment, 0

    while balance > 0 and payment_num < 1000:
        payment_num += 1
        interest_payment = balance * monthly_rate
        principal_payment = min(total_payment - interest_payment, balance)
        balance -= principal_payment

        # Adjusted last PMT
        if balance < 0.01:
            principal_payment += balance
            total_payment = interest_payment + principal_payment
            balance = 0

        schedule.append({
            'Payment': payment_num,
            'Beginning Balance': round(balance + principal_payment, 2),
            'Monthly Payment': round(total_payment, 2),
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

    # Chart 1: Principal vs Interest
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=payments, y=interest_payments,
                              mode='lines', name='Interest', line=dict(color='red', width=2)))
    fig1.add_trace(go.Scatter(x=payments, y=principal_payments,
                              mode='lines', name='Principal', line=dict(color='blue', width=2)))
    fig1.update_layout(title_text='Principal vs Interest Payments Over Time',
                       xaxis_title='Payment Number', yaxis_title='Payment Amount ($)')
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Outstanding Balance
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=payments, y=balances,
                              mode='lines', name='Balance', line=dict(color='green', width=2)))
    fig2.update_layout(title_text='Outstanding Loan Balance',
                       xaxis_title='Payment Number', yaxis_title='Balance ($)')
    st.plotly_chart(fig2, use_container_width=True)


def retirement_planning():  # Retirement Planning
    st.title("Actuarial Calculator 🧮")
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

        create_sensitivity_analysis(
            annual_return, np.linspace(-0.05, 0.05, 21),
            lambda shock: current_savings * (1 + annual_return + shock) ** (retirement_age - current_age) +
            monthly_contribution * (((1 + (annual_return + shock) / 12) ** (
                (retirement_age - current_age) * 12) - 1) / ((annual_return + shock) / 12)),
            'Retirement Funds Sensitivity to Return Rate Changes',
            "Return Rate Shock (%)",
            "Total Retirement Funds ($)"
        )
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
            for _ in range(12):
                balance = balance * (1 + monthly_return) + monthly_contribution

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ages, y=balances, mode='lines+markers',
                             line=dict(color='green', width=2)))
    fig.update_layout(
        title_text='Retirement Savings Growth Over Time',
        xaxis_title='Age',
        yaxis_title='Retirement Savings ($)',
        yaxis_tickprefix='$', yaxis_tickformat=',.0f')
    st.plotly_chart(fig, use_container_width=True)


def main():  # Main App
    st.set_page_config(page_title="Actuarial Calculator",
                       page_icon="📊", layout="wide")
    menu = ["Home 🏠",
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
