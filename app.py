from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__, static_url_path='/static')

registered_users = {}

#conn = sqlite3.connect('website.db')
#cursor = conn.cursor()

app.secret_key = 'your_secret_key'  # Change this to a secure secret key

#Funkcjia zwraca z bazy danych wiadomosci o userze. (napisana do placeholder bazy bedzie trzeba zmiecnic)
def get_user_from_db(username):
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT username, mass, age, height FROM users WHERE username = "{username}";')
    output = cursor.fetchall()
    conn.close()
    return output[0][0], output[0][1], output[0][2], output[0][3]



#Funkcjia laczy sie z serwerm. Sprawdza czy haslo i login pasuja i zwraca boolowska wartosc
def checking_if_login_correct(login: str, password: str) -> bool:
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    if password != None:
        cursor.execute(f'SELECT CASE WHEN EXISTS (SELECT 1 FROM users WHERE username="{login}" AND password="{password}") THEN 1 ELSE 0 END;')
        output = cursor.fetchall()
    else:
        cursor.execute(f'SELECT CASE WHEN EXISTS (SELECT 1 FROM users WHERE username="{login}") THEN 1 ELSE 0 END;')
        output = cursor.fetchall()
    conn.close()
    if output[0][0] == 1:
        return True
    else:
        return False
#dodaje uzytkownika i sprawdza czy uzytkownik sie stworzyl w bazie danych
def dodaj_uzytkownika_do_db(login: str, email: str, password: str) -> bool:
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username,email,password) VALUES ('{login}','{email}', '{password}');")
    conn.commit()
    conn.close()
    if checking_if_login_correct(login, password):
        return True
    else:
        return False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if checking_if_login_correct(login, password) or checking_if_login_correct(login, None):
            return render_template('register.html', wrong_register='Account already exists')
        else:
            if password == confirm_password:
                czy_sie_udalo = dodaj_uzytkownika_do_db(login,email, password)
                if czy_sie_udalo:
                    return redirect(url_for('login'))
                else:
                    return "Wystompil blad w logowaniu"
            else:
                return render_template('register.html', wrong_register='Passwords do not match. Please try again.')
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        if checking_if_login_correct(login, password):
            session['logged_in'] = True
            username, mass, age, height = get_user_from_db(login)
            session['username'] = username
            session['mass'] = mass
            session['age'] = age
            session['height'] = height
            return redirect(url_for('user_page'))
        else:
            wrong_login = "Wrong username or password"
            return render_template('login.html', wrong_login=wrong_login)
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
        username = session['username']
        return render_template('user_page.html', username=username)
    else:
        return redirect(url_for('login'))


# Repeat this pattern for other user pages like progress, stats, etc.

if __name__ == '__main__':
    app.run(debug=True)

