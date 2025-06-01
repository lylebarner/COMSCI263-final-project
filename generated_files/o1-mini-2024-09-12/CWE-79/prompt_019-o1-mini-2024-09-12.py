# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    html_content = ''
    if request.method == 'POST':
        html_content = request.form.get('email_content', '')
    return render_template('index.html', html_content=html_content)

if __name__ == '__main__':
    app.run(debug=True)
