from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markdown import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)

db.create_all()

@app.route('/')
def index():
    comments = Comment.query.all()
    return render_template('index.html', comments=comments)

@app.route('/post_comment', methods=['POST'])
def post_comment():
    content = request.form['content']
    new_comment = Comment(content=content)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/like_comment/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.template_filter('markdown')
def markdown_filter(text):
    return markdown(text)

if __name__ == '__main__':
    app.run(debug=True)
