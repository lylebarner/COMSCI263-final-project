from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)

@app.route('/orders', methods=['GET'])
def get_orders():
    query = Order.query
    customer_name = request.args.get('customer_name')
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)
    date = request.args.get('date')

    if customer_name:
        query = query.filter(Order.customer_name == customer_name)
    if min_amount is not None:
        query = query.filter(Order.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Order.amount <= max_amount)
    if date:
        query = query.filter(Order.date == date)

    orders = query.all()
    return jsonify([{'id': order.id, 'customer_name': order.customer_name, 'amount': order.amount, 'date': order.date} for order in orders])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)