from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

registered_users = {}

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            # Store user data (in this example, just in a dictionary)
            registered_users[username] = password
            return "Registration successful!"
        else:
            return "Passwords do not match. Please try again."

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)