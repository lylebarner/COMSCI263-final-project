from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/filter', methods=['POST'])
def filter_users():
    email = request.form.get('email')
    role = request.form.get('role')
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    
    query = User.query
    
    if email:
        query = query.filter(User.email.contains(email))
    if role:
        query = query.filter(User.role == role)
    if date_from:
        query = query.filter(User.registration_date >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(User.registration_date <= datetime.strptime(date_to, '%Y-%m-%d'))
    
    users = query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    email = request.form.get('email')
    role = request.form.get('role')
    new_user = User(email=email, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

**HTML Template (templates/index.html):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
</head>
<body>
    <h1>User Management</h1>
    <form action="/filter" method="POST">
        <input type="text" name="email" placeholder="Email">
        <input type="text" name="role" placeholder="Role">
        <input type="date" name="date_from">
        <input type="date" name="date_to">
        <button type="submit">Filter</button>
    </form>
    
    <h2>Add User</h2>
    <form action="/add_user" method="POST">
        <input type="email" name="email" required placeholder="Email">
        <input type="text" name="role" required placeholder="Role">
        <button type="submit">Add User</button>
    </form>
    
    <h2>User List</h2>
    <ul>
        {% for user in users %}
            <li>{{ user.email }} - {{ user.role }} - {{ user.registration_date }}</li>
        {% endfor %}
    </ul>
</body>
</html>