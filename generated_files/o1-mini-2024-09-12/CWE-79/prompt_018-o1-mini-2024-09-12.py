from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory storage for user bio
user_data = {
    'bio': 'This is your bio. Click edit to change it.'
}

# Template for the profile page
profile_template = """
<!doctype html>
<html>
<head>
    <title>User Profile</title>
</head>
<body>
    <h1>User Profile</h1>
    <p><strong>Bio:</strong> {{ bio }}</p>
    <a href="{{ url_for('edit_bio') }}">Edit Bio</a>
</body>
</html>
"""

# Template for the edit bio form
edit_bio_template = """
<!doctype html>
<html>
<head>
    <title>Edit Bio</title>
</head>
<body>
    <h1>Edit Your Bio</h1>
    <form method="post">
        <textarea name="bio" rows="5" cols="40">{{ bio }}</textarea><br><br>
        <input type="submit" value="Save">
    </form>
    <a href="{{ url_for('profile') }}">Back to Profile</a>
</body>
</html>
"""

@app.route('/')
def profile():
    bio = user_data.get('bio', '')
    return render_template_string(profile_template, bio=bio)

@app.route('/edit', methods=['GET', 'POST'])
def edit_bio():
    if request.method == 'POST':
        new_bio = request.form.get('bio', '')
        user_data['bio'] = new_bio
        return redirect(url_for('profile'))
    bio = user_data.get('bio', '')
    return render_template_string(edit_bio_template, bio=bio)

if __name__ == '__main__':
    app.run(debug=True)