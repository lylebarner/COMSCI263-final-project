from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# --- Database Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

# --- Templates ---
dashboard_tmpl = """
<!doctype html>
<title>Admin Dashboard</title>
<h1>User Management Dashboard</h1>
<form method="get" action="{{ url_for('dashboard') }}">
    <input type="text" name="email" placeholder="Email" value="{{ request.args.get('email', '') }}">
    <input type="text" name="role" placeholder="Role" value="{{ request.args.get('role', '') }}">
    <input type="date" name="registration_date" value="{{ request.args.get('registration_date', '') }}">
    <button type="submit">Filter</button>
    <a href="{{ url_for('dashboard') }}">Reset</a>
</form>
<br>
<a href="{{ url_for('create_user') }}">Add New User</a>
<table border=1 cellpadding=4>
    <tr><th>ID</th><th>Email</th><th>Role</th><th>Registration Date</th><th>Actions</th></tr>
    {% for user in users %}
    <tr>
        <td>{{ user.id }}</td>
        <td>{{ user.email }}</td>
        <td>{{ user.role }}</td>
        <td>{{ user.registration_date.strftime('%Y-%m-%d') }}</td>
        <td>
            <a href="{{ url_for('edit_user', user_id=user.id) }}">Edit</a>
            <a href="{{ url_for('delete_user', user_id=user.id) }}" onclick="return confirm('Delete user?')">Delete</a>
        </td>
    </tr>
    {% else %}
    <tr><td colspan="5">No users found.</td></tr>
    {% endfor %}
</table>
"""

user_form_tmpl = """
<!doctype html>
<title>{{ 'Edit' if user else 'Create' }} User</title>
<h1>{{ 'Edit' if user else 'Create' }} User</h1>
<form method="post">
    <label>Email: <input type="email" name="email" value="{{ user.email if user else '' }}" required></label><br>
    <label>Role: <input type="text" name="role" value="{{ user.role if user else '' }}" required></label><br>
    <label>Registration Date: <input type="date" name="registration_date" value="{{ user.registration_date.strftime('%Y-%m-%d') if user else '' }}" required></label><br>
    <button type="submit">Save</button>
    <a href="{{ url_for('dashboard') }}">Cancel</a>
</form>
"""

# --- Routes ---

@app.route('/admin')
def dashboard():
    query = User.query

    email = request.args.get('email')
    role = request.args.get('role')
    reg_date = request.args.get('registration_date')

    if email:
        query = query.filter(User.email.contains(email))
    if role:
        query = query.filter(User.role.contains(role))
    if reg_date:
        try:
            date_obj = datetime.strptime(reg_date, '%Y-%m-%d').date()
            query = query.filter(User.registration_date == date_obj)
        except ValueError:
            flash('Invalid date format', 'danger')

    users = query.order_by(User.id.desc()).all()
    return render_template_string(dashboard_tmpl, users=users)

@app.route('/admin/user/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        email = request.form['email'].strip()
        role = request.form['role'].strip()
        reg_date = request.form['registration_date']
        try:
            reg_dt = datetime.strptime(reg_date, '%Y-%m-%d').date()
            user = User(email=email, role=role, registration_date=reg_dt)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template_string(user_form_tmpl, user=None)

@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        try:
            user.email = request.form['email'].strip()
            user.role = request.form['role'].strip()
            user.registration_date = datetime.strptime(request.form['registration_date'], '%Y-%m-%d').date()
            db.session.commit()
            flash('User updated.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template_string(user_form_tmpl, user=user)

@app.route('/admin/user/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('dashboard'))

# --- CLI to create db for first run ---
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database initialized.')

if __name__ == '__main__':
    app.run(debug=True)