from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    filters = {}
    
    customer_name = request.args.get('customer_name')
    if customer_name:
        filters['customer_name'] = customer_name

    status = request.args.get('status')
    if status:
        filters['status'] = status

    min_amount = request.args.get('min_amount')
    if min_amount:
        filters['total_amount'] = min_amount

    query = Order.query
    
    for key, value in filters.items():
        query = query.filter(getattr(Order, key) == value)

    orders = query.all()
    results = [
        {
            'id': order.id,
            'customer_name': order.customer_name,
            'status': order.status,
            'total_amount': order.total_amount
        } for order in orders
    ]
    
    return jsonify(results)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)