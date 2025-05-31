# app.py
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

# Routes
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    email = request.args.get('email', '')
    role = request.args.get('role', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = User.query

    if email:
        query = query.filter(User.email.like(f"%{email}%"))
    if role:
        query = query.filter(User.role == role)
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(User.registration_date >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(User.registration_date <= end)
        except ValueError:
            pass

    users = query.all()
    roles = db.session.query(User.role).distinct().all()
    roles = [r[0] for r in roles]

    return render_template('admin_dashboard.html', users=users, roles=roles, 
                           email=email, role=role, start_date=start_date, end_date=end_date)

@app.route('/admin/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        user = User(email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect('/admin')
    return render_template('create_user.html')

@app.route('/admin/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

```html
<!-- templates/admin_dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        form {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Admin Dashboard</h1>
    <form method="get" action="/admin">
        <label for="email">Email:</label>
        <input type="text" id="email" name="email" value="{{ email }}">
        
        <label for="role">Role:</label>
        <select id="role" name="role">
            <option value="">All</option>
            {% for r in roles %}
            <option value="{{ r }}" {% if r == role %}selected{% endif %}>{{ r }}</option>
            {% endfor %}
        </select>
        
        <label for="start_date">Registration Date From:</label>
        <input type="date" id="start_date" name="start_date" value="{{ start_date }}">
        
        <label for="end_date">To:</label>
        <input type="date" id="end_date" name="end_date" value="{{ end_date }}">
        
        <button type="submit">Filter</button>
    </form>
    <a href="/admin/create">Create New User</a>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Email</th>
                <th>Role</th>
                <th>Registration Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td>{{ user.registration_date.strftime('%Y-%m-%d') }}</td>
                <td>
                    <form method="post" action="/admin/delete/{{ user.id }}" onsubmit="return confirm('Are you sure you want to delete this user?');">
                        <button type="submit">Delete</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5">No users found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

```html
<!-- templates/create_user.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Create User</title>
</head>
<body>
    <h1>Create New User</h1>
    <form method="post" action="/admin/create">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>
        
        <label for="role">Role:</label>
        <input type="text" id="role" name="role" required><br><br>
        
        <button type="submit">Create</button>
    </form>
    <a href="/admin">Back to Dashboard</a>
</body>
</html>
```

```bash
# requirements.txt
Flask
Flask_SQLAlchemy