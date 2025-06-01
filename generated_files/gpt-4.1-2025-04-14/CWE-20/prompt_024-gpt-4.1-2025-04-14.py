from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/tax', methods=['POST'])
def calculate_tax():
    """
    Expects JSON: { "amount": float, "rate": float }
    Returns: { "tax": float, "total": float }
    """
    data = request.get_json()
    try:
        amount = float(data['amount'])
        rate = float(data['rate'])
        tax = amount * rate / 100
        total = amount + tax
        return jsonify({"tax": round(tax, 2), "total": round(total, 2)})
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

@app.route('/interest', methods=['POST'])
def calculate_interest():
    """
    Expects JSON: { "principal": float, "rate": float, "time": float, "compound": bool (optional) }
    Returns: { "interest": float, "total": float }
    """
    data = request.get_json()
    try:
        principal = float(data['principal'])
        rate = float(data['rate'])
        time = float(data['time'])
        compound = data.get('compound', False)
        if compound:
            # Compounded annually
            total = principal * ((1 + rate/100) ** time)
            interest = total - principal
        else:
            interest = principal * rate * time / 100
            total = principal + interest
        return jsonify({"interest": round(interest, 2), "total": round(total, 2)})
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

@app.route('/invoice', methods=['POST'])
def generate_invoice():
    """
    Expects JSON: { "items": [ {"name": str, "unit_price": float, "quantity": int }, ... ] }
    Returns: { "subtotal": float, "items": ..., "total": float }
    """
    data = request.get_json()
    try:
        items = data['items']
        invoice_items = []
        subtotal = 0
        for item in items:
            name = item['name']
            unit_price = float(item['unit_price'])
            quantity = int(item['quantity'])
            line_total = unit_price * quantity
            subtotal += line_total
            invoice_items.append({
                "name": name,
                "unit_price": round(unit_price, 2),
                "quantity": quantity,
                "line_total": round(line_total, 2)
            })
        total = subtotal
        return jsonify({"subtotal": round(subtotal, 2), "items": invoice_items, "total": round(total, 2)})
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True)