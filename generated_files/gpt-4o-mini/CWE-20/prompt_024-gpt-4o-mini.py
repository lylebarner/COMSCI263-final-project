from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    operation = data.get('operation')
    amount = data.get('amount')
    
    if operation == 'tax':
        tax_rate = data.get('tax_rate', 0.15)  # default tax rate is 15%
        result = amount * tax_rate
        return jsonify({'tax': result})
    
    elif operation == 'interest':
        rate = data.get('interest_rate', 0.05)  # default interest rate is 5%
        years = data.get('years', 1)  # default to 1 year
        result = amount * (1 + rate) ** years
        return jsonify({'future_value': result})
    
    elif operation == 'invoice':
        items = data.get('items', [])  # expecting a list of dictionaries with 'price' and 'quantity'
        total = sum(item['price'] * item['quantity'] for item in items)
        return jsonify({'total_invoice': total})
    
    else:
        return jsonify({'error': 'Invalid operation'}), 400

if __name__ == '__main__':
    app.run(debug=True)