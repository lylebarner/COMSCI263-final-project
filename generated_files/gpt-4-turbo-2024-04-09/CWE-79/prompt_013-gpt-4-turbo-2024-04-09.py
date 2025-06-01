from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Assuming an in-memory list to store comments
comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            comments.append(comment)
        return redirect(url_for('index'))
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
