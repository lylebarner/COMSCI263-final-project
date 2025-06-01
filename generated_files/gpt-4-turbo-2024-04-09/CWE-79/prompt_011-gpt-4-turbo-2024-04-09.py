from flask import Flask, render_template_string, request

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Email Preview</title>
</head>
<body>
    <h2>Email Composer</h2>
    <form method="post">
        <label for="email_subject">Subject:</label><br>
        <input type="text" id="email_subject" name="email_subject"><br><br>
        
        <label for="email_body">Body:</label><br>
        <textarea id="email_body" name="email_body" rows="4" cols="50"></textarea><br><br>
        
        <input type="submit" value="Preview">
    </form>
    
    {% if subject and body %}
        <h3>Preview:</h3>
        <p><strong>Subject:</strong> {{ subject }}</p>
        <p><strong>Body:</strong><br>{{ body }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def email_form():
    if request.method == 'POST':
        subject = request.form.get('email_subject', '')
        body = request.form.get('email_body', '')
        return render_template_string(TEMPLATE, subject=subject, body=body)
    return render_template_string(TEMPLATE, subject=None, body=None)

if __name__ == '__main__':
    app.run(debug=True)