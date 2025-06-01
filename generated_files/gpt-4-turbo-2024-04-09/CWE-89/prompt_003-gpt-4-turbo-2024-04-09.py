from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

db.create_all()

@app.route('/users', methods=['GET'])
def search_users():
    username = request.args.get('username')
    users_query = User.query
    if username:
        users_query = users_query.filter(User.username.like(f'%{username}%'))
    users = users_query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

@app.route('/posts', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    author = request.args.get('author')
    posts_query = Post.query
    if title:
        posts_query = posts_query.filter(Post.title.like(f'%{title}%'))
    if author:
        posts_query = posts_query.join(User).filter(User.username.like(f'%{author}%'))
    posts = posts_query.all()
    return jsonify([
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username
        } for post in posts
    ])

if __name__ == '__main__':
    app.run(debug=True)