from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

# Admin Panel Routes
@app.route('/admin/users/search', methods=['GET'])
def search_users():
    username = request.args.get('username')
    email = request.args.get('email')
    filters = []
    
    if username:
        filters.append(User.username.ilike(f'%{username}%'))
    if email:
        filters.append(User.email.ilike(f'%{email}%'))
    
    users = User.query.filter(or_(*filters)).all() if filters else User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@app.route('/admin/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    content = request.args.get('content')
    filters = []
    
    if title:
        filters.append(Post.title.ilike(f'%{title}%'))
    if content:
        filters.append(Post.content.ilike(f'%{content}%'))
    
    posts = Post.query.filter(or_(*filters)).all() if filters else Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id} for post in posts])

# Create the database
@app.before_first_request
def create_tables():
    db.create_all()

# Main route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)