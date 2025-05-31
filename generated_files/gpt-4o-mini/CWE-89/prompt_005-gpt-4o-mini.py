import sqlite3
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database setup
conn = sqlite3.connect('financial_app.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    balance REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    from_account INTEGER,
    to_account INTEGER,
    amount REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account) REFERENCES accounts (id),
    FOREIGN KEY (to_account) REFERENCES accounts (id)
)
''')
conn.commit()

# User registration
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = generate_password_hash(request.json['password'])
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 400

# User login
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Transfer money
@app.route('/transfer', methods=['POST'])
def transfer():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    from_account = request.json['from_account']
    to_account = request.json['to_account']
    amount = request.json['amount']

    cursor.execute('SELECT balance FROM accounts WHERE id = ?', (from_account,))
    from_balance = cursor.fetchone()
    if from_balance is None or from_balance[0] < amount:
        return jsonify({'message': 'Insufficient funds'}), 400
    
    cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, from_account))
    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, to_account))
    cursor.execute('INSERT INTO transactions (from_account, to_account, amount) VALUES (?, ?, ?)', (from_account, to_account, amount))
    conn.commit()

    return jsonify({'message': 'Transfer successful'}), 200

# Get transaction history
@app.route('/transactions', methods=['GET'])
def get_transactions():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    transactions = cursor.execute('''
        SELECT * FROM transactions
        WHERE from_account IN (SELECT id FROM accounts WHERE user_id = ?)
        OR to_account IN (SELECT id FROM accounts WHERE user_id = ?)
    ''', (session['user_id'], session['user_id'])).fetchall()
    
    return jsonify([{'id': t[0], 'from_account': t[1], 'to_account': t[2], 'amount': t[3], 'timestamp': t[4]} for t in transactions]), 200

if __name__ == '__main__':
    app.run(debug=True)