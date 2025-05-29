from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for user profiles
user_profiles = {}

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if request.method == 'POST':
        bio = request.form.get('bio')
        user_profiles[username] = bio  # Store the bio in memory
        return redirect(url_for('profile', username=username))
    
    bio = user_profiles.get(username, '')  # Retrieve the bio if it exists
    return render_template('profile.html', username=username, bio=bio)

@app.route('/edit/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    bio = user_profiles.get(username, '')
    if request.method == 'POST':
        bio = request.form.get('bio')
        user_profiles[username] = bio  # Update the bio in memory
        return redirect(url_for('profile', username=username))
    
    return render_template('edit_profile.html', username=username, bio=bio)

if __name__ == '__main__':
    app.run(debug=True)
```

**HTML templates:**

1. `profile.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ username }}'s Profile</title>
</head>
<body>
    <h1>{{ username }}'s Profile</h1>
    <p>Bio: {{ bio }}</p>
    <a href="{{ url_for('edit_profile', username=username) }}">Edit Bio</a>
</body>
</html>
```

2. `edit_profile.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit {{ username }}'s Bio</title>
</head>
<body>
    <h1>Edit Bio for {{ username }}</h1>
    <form method="POST">
        <textarea name="bio" rows="4" cols="50">{{ bio }}</textarea><br>
        <input type="submit" value="Save">
    </form>
    <a href="{{ url_for('profile', username=username) }}">Back to Profile</a>
</body>
</html>