from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Email Composer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background: #fafbfc; }
        form { padding: 20px; background: #fff; border: 1px solid #ddd; border-radius: 4px; max-width: 600px; margin-bottom: 30px;}
        .preview {padding: 20px; background: #f8f8f8; border: 1px solid #cce; border-radius: 4px; max-width: 600px;}
        label { display:block; font-weight:bold; margin-top:12px;}
        input, textarea { width:100%; font-size:1em; margin-top: 3px;}
        textarea { resize: vertical; min-height: 100px;}
        .preview-title {font-weight:bold; margin-bottom: 10px;}
    </style>
</head>
<body>
    <h2>Write Your Email</h2>
    <form method="post" id="email-form">
        <label>To:</label>
        <input type="email" name="to" id="to" required value="{{to or ''}}">
        <label>Subject:</label>
        <input type="text" name="subject" id="subject" required value="{{subject or ''}}">
        <label>Body:</label>
        <textarea name="body" id="body" required>{{body or ''}}</textarea>
        <button type="submit" style="margin-top:15px;">Submit / Preview</button>
    </form>

    {% if submitted %}
    <div class="preview">
        <div class="preview-title">Live Email Preview:</div>
        <b>To:</b> {{to}}<br>
        <b>Subject:</b> {{subject}}<br><br>
        <div>{{body | nl2br}}</div>
    </div>
    {% endif %}

    <script>
        // Optional: Autosubmit form for live preview (optional, can be removed for submit-only mode)
        let timeout = null;
        document.getElementById('email-form').addEventListener('input', function(){
            if(timeout) clearTimeout(timeout);
            timeout = setTimeout(function(){
                document.getElementById('email-form').submit();
            }, 650); // Wait a bit before autosubmitting
        });
    </script>
</body>
</html>
'''

@app.template_filter('nl2br')
def nl2br_filter(s):
    return (s or '').replace('\n', '<br>')

@app.route('/', methods=['GET', 'POST'])
def index():
    to = subject = body = ''
    submitted = False
    if request.method == 'POST':
        to = request.form.get('to', '')
        subject = request.form.get('subject', '')
        body = request.form.get('body', '')
        submitted = True
    return render_template_string(HTML, to=to, subject=subject, body=body, submitted=submitted)

if __name__ == '__main__':
    app.run(debug=True)