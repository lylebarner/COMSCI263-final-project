from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    email_content = ""
    if request.method == 'POST':
        email_content = request.form.get('email_content', '')
    return render_template('index.html', email_content=email_content)

if __name__ == '__main__':
    app.run(debug=True)
