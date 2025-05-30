from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Post {self.id} by {self.username}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        new_post = Post(username=username, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/filter', methods=['GET'])
def filter_posts():
    username = request.args.get('username', '')
    posts = Post.query.filter(Post.username.contains(username)).all()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
