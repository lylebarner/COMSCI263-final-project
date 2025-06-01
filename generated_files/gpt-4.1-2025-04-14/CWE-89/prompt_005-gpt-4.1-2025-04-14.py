from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    to_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Auth decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    # Create an account for user
    account = Account(balance=0.0, user_id=user.id)
    db.session.add(account)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'})

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    session['user_id'] = user.id
    return jsonify({'message': 'Logged in successfully'})

# User logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id')
    return jsonify({'message': 'Logged out'})

# Transfer money between accounts
@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.json
    from_id = data['from_account_id']
    to_id = data['to_account_id']
    amount = float(data['amount'])
    user_id = session['user_id']

    from_account = Account.query.filter_by(id=from_id, user_id=user_id).first()
    to_account = Account.query.filter_by(id=to_id).first()
    if not from_account or not to_account:
        return jsonify({'error': 'Invalid account'}), 400
    if from_account.balance < amount or amount <= 0:
        return jsonify({'error': 'Insufficient funds or invalid amount'}), 400

    from_account.balance -= amount
    to_account.balance += amount

    transaction = Transaction(
        from_account_id=from_id,
        to_account_id=to_id,
        amount=amount
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Transfer complete'})

# Get account balances
@app.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    user_id = session['user_id']
    accounts = Account.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': acc.id, 'balance': acc.balance} for acc in accounts])

# Get transactions for user's accounts
@app.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    user_id = session['user_id']
    accounts = Account.query.filter_by(user_id=user_id).all()
    account_ids = [acc.id for acc in accounts]
    transactions = Transaction.query.filter(
        (Transaction.from_account_id.in_(account_ids)) | (Transaction.to_account_id.in_(account_ids))
    ).order_by(Transaction.timestamp.desc()).all()
    return jsonify([
        {
            'id': t.id,
            'from_account_id': t.from_account_id,
            'to_account_id': t.to_account_id,
            'amount': t.amount,
            'timestamp': t.timestamp.isoformat()
        } for t in transactions
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)