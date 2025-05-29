from flask import Flask, request, render_template

app = Flask(__name__)

comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form['comment']
        comments.append(comment)
    
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)