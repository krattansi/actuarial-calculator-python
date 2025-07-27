# Comprehensive Actuarial Calculator (Python) 🧮

A complete calculator built in Python that performs essential actuarial and finance computations. These functions include time value of money, annuities, bond pricing, loan amortization schedules, and retirement planning, complete with exportable CSVs and visualizations. All features are deployed in a convenient Streamlit web app for easy use.

## 📌 Features

- Time Value of Money (PV, FV, Rate, Periods with growth chart)  
- Annuity Calculator: Immediate, Due, Growing, and Deferred (PV/FV)  
- Bond Pricing: PV of coupons and face value as well as Modified and Macaulay durations with user-defined YTM  
- Loan Amortization: Full monthly schedule saved to CSV with accompanying charts  
- Retirement Planner: Simulates future retirement fund growth and 4% rule withdrawals with accompanying charts
- Dynamic financial visualizations using `matplotlib`  
- CSV export for loan amortization schedules
- Modern and interactive front-end using `streamlit`

## 🧮 Calculations Included

- **TVM**: Supports compound interest on different compounding frequencies, can calculate FV, PV, rate, or # of periods
- **Annuities**:
  - Annuity Immediate & Due: PV and FV formulas with compounding
  - Growing Annuities: Supports PV and FV with differing growth and interest rates  
  - Deferred Annuities: Calculates PV and FV with pre-retirement deferral period  
- **Bond Pricing**: Discounts fixed-rate coupons and face value using periodic YTM  
- **Loans**: Monthly payment schedule with monthly payment, split interest/principal payments, and balance
- **Retirement**: Combines compound growth of current savings + monthly contributions and calculates responsible withdrawals using the 4% rule

## 📊 Visualizations

- TVM value vs. time growth chart (PV or FV)  
- Loan amortization:
  - Interest vs principal per payment
  - Declining balance chart  
- Retirement planner: Tracks yearly savings accumulation until retirement  

## 💼 Why This Project?

As an actuarial science student, I built this calculator to strengthen my skills in financial and actuarial mathematics while expanding my proficiency in Python. This tool provides quick, intuitive access to key calculations and financial instruments used frequently in the actuarial field, especially within ALM.
