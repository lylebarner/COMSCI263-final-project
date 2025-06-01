from flask import Flask, request, redirect, render_template_string, url_for

app = Flask(__name__)

# In-memory user data
user_data = {
    'username': 'john_doe',
    'bio': 'This is your bio. Click "Edit" to change it.'
}

PROFILE_TEMPLATE = '''
<!doctype html>
<title>Profile Page</title>
<h1>Profile: {{ username }}</h1>
<p><strong>Bio:</strong></p>
<p>{{ bio }}</p>
<a href="{{ url_for('edit_bio') }}">Edit Bio</a>
'''

EDIT_TEMPLATE = '''
<!doctype html>
<title>Edit Bio</title>
<h1>Edit Bio for {{ username }}</h1>
<form method="post">
    <textarea name="bio" rows="8" cols="60">{{ bio }}</textarea><br>
    <input type="submit" value="Save">
    <a href="{{ url_for('profile') }}">Cancel</a>
</form>
'''

@app.route('/')
def profile():
    return render_template_string(
        PROFILE_TEMPLATE,
        username=user_data['username'],
        bio=user_data['bio']
    )

@app.route('/edit', methods=['GET', 'POST'])
def edit_bio():
    if request.method == 'POST':
        new_bio = request.form.get('bio', '')
        user_data['bio'] = new_bio
        return redirect(url_for('profile'))
    return render_template_string(
        EDIT_TEMPLATE,
        username=user_data['username'],
        bio=user_data['bio']
    )

if __name__ == '__main__':
    app.run(debug=True)