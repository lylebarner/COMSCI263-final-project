from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

# Define Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(100))
    status = db.Column(db.String(20))
    total_amount = db.Column(db.Float)
    order_date = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "customer": self.customer,
            "status": self.status,
            "total_amount": self.total_amount,
            "order_date": self.order_date.isoformat() if self.order_date else None,
        }

# Example route: GET /orders?customer=John&status=shipped&min_amount=50&start_date=2024-01-01
@app.route('/orders', methods=['GET'])
def get_orders():
    query = Order.query

    # Flexible filters from URL parameters
    customer = request.args.get('customer')
    if customer:
        query = query.filter(Order.customer.ilike(f"%{customer}%"))

    status = request.args.get('status')
    if status:
        query = query.filter(Order.status == status)
    
    min_amount = request.args.get('min_amount', type=float)
    if min_amount is not None:
        query = query.filter(Order.total_amount >= min_amount)

    max_amount = request.args.get('max_amount', type=float)
    if max_amount is not None:
        query = query.filter(Order.total_amount <= max_amount)
    
    start_date = request.args.get('start_date')
    if start_date:
        query = query.filter(Order.order_date >= start_date)
    
    end_date = request.args.get('end_date')
    if end_date:
        query = query.filter(Order.order_date <= end_date)
    
    orders = query.all()
    return jsonify([order.to_dict() for order in orders])

# Initialize the database (for demo use only)
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)