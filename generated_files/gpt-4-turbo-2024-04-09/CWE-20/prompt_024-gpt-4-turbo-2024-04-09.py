from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_tax(amount, tax_rate):
    return amount * (tax_rate / 100)

def calculate_interest(principal, rate, time):
    return principal * (rate / 100) * time

def calculate_invoice(subtotals, tax_rate):
    total = sum(subtotals)
    tax_amount = calculate_tax(total, tax_rate)
    return total + tax_amount

@app.route('/tax', methods=['POST'])
def tax():
    data = request.get_json()
    amount = data.get('amount')
    tax_rate = data.get('tax_rate')
    if amount is None or tax_rate is None:
        return "Invalid input", 400
    result = calculate_tax(amount, tax_rate)
    return jsonify({'result': result})

@app.route('/interest', methods=['POST'])
def interest():
    data = request.get_json()
    principal = data.get('principal')
    rate = data.get('rate')
    time = data.get('time')
    if principal is None or rate is None or time is None:
        return "Invalid input", 400
    result = calculate_interest(principal, rate, time)
    return jsonify({'result': result})

@app.route('/invoice', methods=['POST'])
def invoice():
    data = request.get_json()
    subtotals = data.get('subtotals')
    tax_rate = data.get('tax_rate')
    if not subtotals or tax_rate is None:
        return "Invalid input", 400
    result = calculate_invoice(subtotals, tax_rate)
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
