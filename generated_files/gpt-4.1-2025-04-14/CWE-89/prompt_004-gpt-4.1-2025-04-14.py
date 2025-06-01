from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

db.create_all()

TEMPLATE = '''
<!doctype html>
<title>Simple Flask Forum</title>
<h1>Flask Forum</h1>

<form method="get" action="/">
    <input name="filter" placeholder="Filter by username or text" value="{{request.args.get('filter', '')}}">
    <button type="submit">Filter</button>
    <a href="{{url_for('home')}}">Clear</a>
</form>
<br>
<form method="post" action="/">
    <input name="username" placeholder="Your name" required>
    <br>
    <textarea name="content" placeholder="Your post" required></textarea>
    <br>
    <button type="submit">Post</button>
</form>
<hr>
{% for post in posts %}
    <div style="border:1px solid #ccc; padding:10px; margin:10px 0;">
        <strong>{{ post.username }}</strong><br>
        {{ post.content }}
    </div>
{% else %}
    <em>No posts yet.</em>
{% endfor %}
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username'].strip()
        content = request.form['content'].strip()
        if username and content:
            db.session.add(Post(username=username, content=content))
            db.session.commit()
        return redirect(url_for('home'))

    filter_query = request.args.get('filter', '').strip()
    posts = Post.query.order_by(Post.id.desc())
    if filter_query:
        posts = posts.filter(
            db.or_(
                Post.username.ilike(f"%{filter_query}%"),
                Post.content.ilike(f"%{filter_query}%")
            )
        )
    posts = posts.all()
    return render_template_string(TEMPLATE, posts=posts, request=request)

if __name__ == '__main__':
    app.run(debug=True)