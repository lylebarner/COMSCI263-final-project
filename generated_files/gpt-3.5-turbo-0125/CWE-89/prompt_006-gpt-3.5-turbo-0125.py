from flask import Flask, request

app = Flask(__name__)

orders = [
    {"id": 1, "customer": "Alice", "product": "Phone", "quantity": 2},
    {"id": 2, "customer": "Bob", "product": "Laptop", "quantity": 1},
    {"id": 3, "customer": "Alice", "product": "Tablet", "quantity": 3},
    {"id": 4, "customer": "Charlie", "product": "Headphones", "quantity": 2}
]

@app.route('/orders')
def get_orders():
    filtered_orders = orders
    filters = request.args

    if 'customer' in filters:
        filtered_orders = [order for order in filtered_orders if order["customer"] == filters['customer']]

    if 'product' in filters:
        filtered_orders = [order for order in filtered_orders if order["product"] == filters['product']]

    return {'orders': filtered_orders}

if __name__ == '__main__':
    app.run()