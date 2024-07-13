from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
from datetime import datetime, timedelta
import re
app = Flask(__name__, static_url_path='/static')

registered_users = {}

#conn = sqlite3.connect('website.db')
#cursor = conn.cursor()

app.secret_key = 'your_secret_key'  # Change this to a secure secret key

#Funkcjia zwraca z bazy danych wiadomosci o userze. (napisana do placeholder bazy bedzie trzeba zmiecnic)
def get_user_from_db(username):
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT username, mass, age, height, email FROM users WHERE username = "{username}";')
    output = cursor.fetchall()
    conn.close()
    return output[0][0], output[0][1], output[0][2], output[0][3], output[0][4]

#funkcjia sprawdza czy mail juz jest uwzywany
def check_email_exists(email: str) -> bool:
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT CASE WHEN EXISTS (SELECT 1 FROM users WHERE email="{email}") THEN 1 ELSE 0 END;')
    output = cursor.fetchall()
    conn.close()
    if output[0][0] == 1:
        return True
    else:
        return False

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
def dodaj_uzytkownika_do_db(login: str, email: str, password: str, creation_date:datetime) -> bool:
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username,email,password,account_created_date) VALUES ('{login}','{email}', '{password}','{creation_date}');")
    conn.commit()
    conn.close()
    if checking_if_login_correct(login, password):
        return True
    else:
        return False

def check_if_email_correct(email:str) -> bool:
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, email):
        return True
    else:
        return False

def generacjia_daty_utowrzeniakonta() -> datetime:
    return datetime.now()

# Get user's streaks by email
def get_streaks_by_email(email):
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT best_streak, current_streak, days_when_on_site FROM users WHERE email = "{email}";')
    output = cursor.fetchall()
    conn.close()
    return output[0][0], output[0][1], output[0][2]

def get_account_creation_info(email):
    account_created_date_str, account_created_date = get_account_created_date(email)
    days_from_account_creation = get_days_from_account_creation(account_created_date)
    return account_created_date_str, days_from_account_creation

def get_account_created_date(email):
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT account_created_date FROM users WHERE email = "{email}";')
    output = cursor.fetchall()
    conn.close()
    account_created_date = datetime.strptime(output[0][0], '%Y-%m-%d %H:%M:%S.%f')
    account_created_date_str = account_created_date.strftime("%d.%m.%y")
    return account_created_date_str, account_created_date

def get_days_from_account_creation(account_created_date):
    return (datetime.now() - account_created_date).days

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register(confirm_password=None):
    if request.method == 'POST':
        login = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        #wczytanie z pamieci loginu przed errorem
        if login == "" and session.get('inputed_username') != None:
            login = session.get('inputed_username')
        else:
            session['inputed_username'] = login

        inputed_username = login
        #wczytanie z pamieci emaila przed errorem
        if email == "" and session.get('inputed_email') != None:
            email = session.get('inputed_email')
        else:
            session['inputed_email'] = email

        if check_if_email_correct(email):
            inputed_mail = email
        else:
            return render_template('register.html', inputed_username=inputed_username, inputed_mail="Email", wrong_register="Email is incorrect")
        if checking_if_login_correct(login, None):
            return render_template('register.html',inputed_username="Username", inputed_mail="Email", wrong_register='Account already exists')
        elif check_email_exists(email):
            return render_template('register.html',inputed_username=inputed_username, wrong_register='Email already exists')
        else:
            if password == confirm_password:
                czy_sie_udalo = dodaj_uzytkownika_do_db(login, email, password, generacjia_daty_utowrzeniakonta())
                if czy_sie_udalo:
                    return redirect(url_for('login'))
                else:
                    return "Wystompil blad w logowaniu"
            else:
                return render_template('register.html', inputed_username=inputed_username, inputed_mail=inputed_mail, wrong_register='Passwords do not match. Please try again.')
    return render_template('register.html',inputed_username="Username", inputed_mail="Email")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        if checking_if_login_correct(login, password):
            session['logged_in'] = True
            username, mass, age, height, email = get_user_from_db(login)
            session['username'] = username
            session['mass'] = mass
            session['age'] = age
            session['height'] = height
            session['email'] = email
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
    if 'logged_in' in session:
        email = session['email']

        account_created_date, days_from_account_creation = get_account_creation_info(email)
        best_streak, current_streak, days_when_on_site = get_streaks_by_email(email)
        return render_template('stats.html',
                               account_created_date=account_created_date,
                               days_from_account_creation=days_from_account_creation,
                               best_streak=best_streak,
                               current_streak=current_streak,
                               days_when_on_site=days_when_on_site)
    else:
        return redirect(url_for('login'))

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

