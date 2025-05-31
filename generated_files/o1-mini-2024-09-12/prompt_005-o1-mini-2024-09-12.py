from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Decorator for authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Authentication required.'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists.'}), 400
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, balance=1000.0)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials.'}), 401
    session['user_id'] = user.id
    return jsonify({'message': 'Logged in successfully.'}), 200

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.json
    from_user = User.query.get(session['user_id'])
    to_user = User.query.filter_by(username=data['to_username']).first()
    amount = data['amount']
    if not to_user:
        return jsonify({'message': 'Recipient not found.'}), 404
    if from_user.balance < amount:
        return jsonify({'message': 'Insufficient funds.'}), 400
    from_user.balance -= amount
    to_user.balance += amount
    transaction = Transaction(from_user_id=from_user.id, to_user_id=to_user.id, amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Transfer successful.'}), 200

@app.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    user_id = session['user_id']
    transactions = Transaction.query.filter(
        (Transaction.from_user_id == user_id) | 
        (Transaction.to_user_id == user_id)
    ).all()
    result = []
    for tx in transactions:
        result.append({
            'id': tx.id,
            'from_user_id': tx.from_user_id,
            'to_user_id': tx.to_user_id,
            'amount': tx.amount,
            'timestamp': tx.timestamp
        })
    return jsonify(result), 200

@app.route('/balance', methods=['GET'])
@login_required
def balance():
    user = User.query.get(session['user_id'])
    return jsonify({'balance': user.balance}), 200

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)