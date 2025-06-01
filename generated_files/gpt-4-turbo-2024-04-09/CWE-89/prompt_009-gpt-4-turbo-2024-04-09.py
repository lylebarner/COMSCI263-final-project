from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/filter', methods=['POST'])
def filter_users():
    email = request.form.get('email')
    role = request.form.get('role')
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')

    query = User.query
    if email:
        query = query.filter(User.email.ilike(f'%{email}%'))
    if role:
        query = query.filter_by(role=role)
    if from_date:
        query = query.filter(User.registration_date >= datetime.strptime(from_date, '%Y-%m-%d'))
    if to_date:
        query = query.filter(User.registration_date <= datetime.strptime(to_date, '%Y-%m-%d'))
    
    users = query.all()
    return render_template('index.html', users=users)

@app.route('/create', methods=['POST'])
def create_user():
    email = request.form['email']
    role = request.form['role']
    new_user = User(email=email, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
</head>
<body>
    <h1>User Management</h1>
    <form method="post" action="/create">
        <input type="text" name="email" placeholder="Enter Email" required>
        <input type="text" name="role" placeholder="Enter Role" required>
        <button type="submit">Add User</button>
    </form>
    <hr>
    <form method="post" action="/filter">
        <input type="text" name="email" placeholder="Search by Email">
        <input type="text" name="role" placeholder="Search by Role">
        <input type="date" name="from_date">
        <input type="date" name="to_date">
        <button type="submit">Filter</button>
    </form>
    <table border="1">
        <tr>
            <th>Email</th>
            <th>Role</th>
            <th>Registration Date</th>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.registration_date }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>