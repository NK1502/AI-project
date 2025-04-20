import os
from flask import Flask, render_template, request

app = Flask(__name__)

def generate_strategy(data):
    income = float(data['income'])
    expenses = float(data['expenses'])
    loan_amount = float(data['loan_amount'])
    loan_duration = int(data['loan_duration'])
    interest_rate = float(data['interest_rate'])

    disposable_income = income - expenses
    monthly_emi = (loan_amount * (1 + (interest_rate / 100))) / (loan_duration * 12)

    strategy = []

    if disposable_income <= 0:
        strategy.append("Your expenses are more than your income. Consider reducing expenses or increasing income.")
    elif monthly_emi > disposable_income:
        strategy.append("EMI exceeds your disposable income. Consider extending loan duration or refinancing.")
    else:
        strategy.append(f"Based on your data, your monthly EMI would be ₹{monthly_emi:.2f}.")
        if disposable_income > monthly_emi * 2:
            strategy.append("You can opt for a higher EMI to repay faster and save on interest.")
        elif disposable_income > monthly_emi:
            strategy.append("You're in a good position to follow a regular EMI schedule.")
        else:
            strategy.append("Maintain a buffer and stick to the minimum EMI plan.")

    # Indian government schemes
    strategy.append("Check out Indian Government Schemes like:")
    strategy.append("- Vidya Lakshmi Portal (https://www.vidyalakshmi.co.in)")
    strategy.append("- Dr. Ambedkar Central Sector Scheme for Interest Subsidy")
    strategy.append("- SBI Scholar Loan, HDFC Credila, etc.")

    return strategy

@app.route('/', methods=['GET', 'POST'])
def index():
    strategy = None
    if request.method == 'POST':
        form_data = request.form
        strategy = generate_strategy(form_data)
    return render_template('index.html', strategy=strategy)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT not set
    app.run(host='0.0.0.0', port=port)

