from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_content = request.form['email_content']
        return render_template('preview.html', email_content=email_content)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)