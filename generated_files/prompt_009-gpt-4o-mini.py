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
