from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    url = ''
    if request.method == 'POST':
        url = request.form['url']
    return render_template('index.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)
