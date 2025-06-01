from flask import Flask, render_template_string, request

app = Flask(__name__)

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Email HTML Preview</title>
</head>
<body>
    <h2>Write HTML Email Content</h2>
    <form method="post">
        <textarea name="html_content" rows="10" cols="50"></textarea><br>
        <input type="submit" value="Preview">
    </form>
    {% if html_content %}
        <h3>Preview:</h3>
        <div style="border: 1px solid #000; padding: 10px;">
            {{ html_content|safe }}
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    html_content = ""
    if request.method == 'POST':
        html_content = request.form['html_content']
    return render_template_string(html_form, html_content=html_content)

if __name__ == '__main__':
    app.run(debug=True)