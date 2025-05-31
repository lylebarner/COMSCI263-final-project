from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store comments in a list
comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            comments.append(comment)  # Add comment to the list
            return redirect(url_for('index'))  # Redirect to the same page
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
