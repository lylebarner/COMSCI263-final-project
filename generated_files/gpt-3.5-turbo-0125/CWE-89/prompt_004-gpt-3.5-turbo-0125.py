from flask import Flask, request

app = Flask(__name__)

posts = []

@app.route('/new_post', methods=['POST'])
def new_post():
    data = request.get_json()
    posts.append(data['post'])
    return 'Post added successfully'

@app.route('/posts', methods=['GET'])
def get_posts():
    return {'posts': posts}

if __name__ == '__main__':
    app.run()