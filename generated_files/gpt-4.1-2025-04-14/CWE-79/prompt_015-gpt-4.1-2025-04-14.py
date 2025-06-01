from flask import Flask, render_template_string, request, redirect, url_for, session
from markdown import markdown
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory data stores (use a real database for production)
comments = []

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Markdown Comments</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 650px; margin: 40px auto; }
        .comment { border: 1px solid #ddd; padding: 12px; margin-bottom: 14px; }
        .like-btn { display: inline-block; margin-left: 10px; }
        .likes-count { color: #888; }
        textarea { width: 100%; min-height: 60px; }
        .comment markdown { background: #f6f8fa; }
    </style>
</head>
<body>
    <h2>Post a Comment (Markdown supported)</h2>
    <form method="post" action="{{ url_for('post_comment') }}">
        <textarea name="content" required placeholder="Type your comment in Markdown here..."></textarea><br>
        <button type="submit">Post Comment</button>
    </form>
    <hr>
    <h3>Comments</h3>
    {% for c in comments %}
      <div class="comment">
        <div>{{c.html_content|safe}}</div>
        <form method="post" action="{{ url_for('like_comment', cid=c['id']) }}" style="display:inline;">
          <button type="submit" class="like-btn" {% if session.get('liked', [])|join(',')|search(c['id']) != None %}disabled{% endif %}>👍 Like</button>
          <span class="likes-count">{{c.likes}} like{{'s' if c.likes!=1 else ''}}</span>
        </form>
      </div>
    {% else %}
      <p>No comments yet.</p>
    {% endfor %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    # Render Markdown content for each comment
    rendered = []
    for c in comments:
        rendered.append({
            **c,
            'html_content': markdown(c['content'], extensions=['extra'])
        })
    return render_template_string(TEMPLATE, comments=rendered, session=session)

@app.route('/post', methods=['POST'])
def post_comment():
    content = request.form.get('content', '').strip()
    if content:
        comments.append({
            'id': str(uuid4()),
            'content': content,
            'likes': 0
        })
    return redirect(url_for('index'))

@app.route('/like/<cid>', methods=['POST'])
def like_comment(cid):
    # Prevent double-like in session
    if 'liked' not in session:
        session['liked'] = []
    if cid not in session['liked']:
        for c in comments:
            if c['id'] == cid:
                c['likes'] += 1
                break
        session['liked'].append(cid)
        session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
