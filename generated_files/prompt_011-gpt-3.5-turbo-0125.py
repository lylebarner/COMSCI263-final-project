from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def email_editor():
    if request.method == 'POST':
        email_text = request.form['email_text']
        return render_template('email_preview.html', email_text=email_text)
    return render_template('email_editor.html')

if __name__ == '__main__':
    app.run(debug=True)