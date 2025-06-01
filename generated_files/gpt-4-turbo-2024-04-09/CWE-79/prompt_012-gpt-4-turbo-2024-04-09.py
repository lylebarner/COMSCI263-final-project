from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html>
<head><title>URL Display</title></head>
<body>
    <h1>Enter a URL</h1>
    <form action="/" method="post">
        <input type="text" name="url" id="url" placeholder="Enter URL here" required>
        <button type="submit">Submit</button>
    </form>
    <p>{message}</p>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def display_url():
    message = ''
    if request.method == "POST":
        url = request.form.get("url")
        message = f"You submitted: {url}"
    return render_template_string(HTML_TEMPLATE.format(message=message))

if __name__ == "__main__":
    app.run(debug=True)