from flask import Flask, render_template_string, request, Markup

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Email HTML Editor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .form-section, .preview-section { margin-bottom: 30px; }
        textarea { width: 100%%; height: 220px; font-family: monospace; font-size: 15px; }
        .preview-section { border: 1px solid #ccc; padding: 18px; background: #fafafa; }
        label { font-weight: bold; margin-bottom: 10px; display: block; }
    </style>
</head>
<body>
    <h2>Email HTML Editor with Live Preview</h2>
    <form method="post" class="form-section">
        <label for="email_html">Write your email in HTML:</label>
        <textarea id="email_html" name="email_html" placeholder="&lt;h1&gt;Hello!&lt;/h1&gt;&#10;This is your email body.">{{ email_html|default('') }}</textarea>
        <br><br>
        <button type="submit">Preview Email</button>
    </form>
    <div class="preview-section">
        <h3>Live Email Preview:</h3>
        <div style="background:white; padding:12px; border:1px solid #e0e0e0;">
            {{ preview_html|safe }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def email_editor():
    email_html = ''
    preview_html = ''
    if request.method == 'POST':
        email_html = request.form.get('email_html', '')
        preview_html = Markup(email_html)  # Mark safe to render raw HTML
    return render_template_string(TEMPLATE, email_html=email_html, preview_html=preview_html)

if __name__ == "__main__":
    app.run(debug=True)
