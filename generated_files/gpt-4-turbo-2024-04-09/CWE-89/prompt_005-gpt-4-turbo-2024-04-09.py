import sqlite3
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (id INTEGER PRIMARY KEY, user_id INTEGER, balance REAL,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, from_account INTEGER, to_account INTEGER,
                  amount REAL, FOREIGN KEY(from_account) REFERENCES accounts(id),
                  FOREIGN KEY(to_account) REFERENCES accounts(id))''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (data['username'], hashed_password))
    conn.commit()
    return jsonify({'message': 'Registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (auth.username,))
    user = c.fetchone()
    
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    if check_password_hash(user[2], auth.password):
        return jsonify({'message': 'Login successful'})
    else:
        return make_response('Could not verify', 403, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    amount = data['amount']
    from_account_id = data['from_account_id']
    to_account_id = data['to_account_id']
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    # Check if accounts exist and retrieve balances
    c.execute("SELECT balance FROM accounts WHERE id = ?", (from_account_id,))
    from_account_balance = c.fetchone()
    if from_account_balance is None:
        return jsonify({'message': 'From account does not exist'}), 400

    c.execute("SELECT balance FROM accounts WHERE id = ?", (to_account_id,))
    to_account_balance = c.fetchone()
    if to_account_balance is None:
        return jsonify({'message': 'To account does not exist'}), 400

    # Check sufficient funds
    if from_account_balance[0] < amount:
        return jsonify({'message': 'Insufficient funds'}), 400

    # Perform transfer
    new_from_balance = from_account_balance[0] - amount
    new_to_balance = to_account_balance[0] + amount
    c.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_from_balance, from_account_id))
    c.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_to_balance, to_account_id))
    c.execute("INSERT INTO transactions (from_account, to_account, amount) VALUES (?, ?, ?)",
              (from_account_id, to_account_id, amount))
    conn.commit()

    return jsonify({'message': 'Transfer successful'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)