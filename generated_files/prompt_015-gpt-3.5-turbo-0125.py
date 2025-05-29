from flask import Flask, request, render_template

app = Flask(__name__)
comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form['comment']
        comments.append({'text': comment, 'likes': 0})
    return render_template('index.html', comments=comments)

@app.route('/like/<int:comment_id>', methods=['POST'])
def like(comment_id):
    comments[comment_id]['likes'] += 1
    return 'Liked!'

if __name__ == '__main__':
    app.run()