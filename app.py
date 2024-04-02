from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__, static_url_path='/static')

registered_users = {}


app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Dummy user data (replace with your actual user authentication mechanism)
users = {
    'qw': 'qw',
    'zx': 'zx'
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            # Store user data (in this example, just in a dictionary)
            registered_users[username] = password
            return redirect(url_for('login'))
        else:
            return "Passwords do not match. Please try again."
    print(registered_users)
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('user_page'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/sign_out')
def sign_out():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/progress')
def progress():
    # Logic for progress page
    return render_template('progress.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/kcal_calculator')
def kcal_calculator():
    return render_template('kcal_calculator.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/user_page')
def user_page():
    if 'logged_in' in session:
        return render_template('user_page.html')
    else:
        return redirect(url_for('login'))


# Repeat this pattern for other user pages like progress, stats, etc.

if __name__ == '__main__':
    app.run(debug=True)
