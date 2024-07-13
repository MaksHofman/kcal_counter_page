from flask import Flask, render_template, redirect, url_for, request, session
from stats_functions import *
from login_register import *
from kcal_functions import *
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

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
            username, mass, age, height, email, gender, activity_level = get_user_from_db(login)
            session['username'] = username
            session['mass'] = mass
            session['age'] = age
            session['height'] = height
            session['email'] = email
            session['gender'] = gender
            session['activity_level'] = activity_level
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
        ttde = calculate_tdee(calculate_bmr(session.get('mass'), session.get('age'), session.get('height'), session.get('gender')), activity_level=session.get('activity_level'))
        return render_template('stats.html',
                               account_created_date=account_created_date,
                               days_from_account_creation=days_from_account_creation,
                               best_streak=best_streak,
                               current_streak=current_streak,
                               days_when_on_site=days_when_on_site, ttde=ttde)
    else:
        return redirect(url_for('login'))

@app.route('/kcal_calculator')
def kcal_calculator():
    return render_template('kcal_calculator.html')


@app.route('/my_page')
def my_page():
    username = session['username']
    email = session['email']
    gender = session['gender']
    age = session['age']
    height = session['height']
    mass = session['mass']
    activity_level = session['activity_level']
    return render_template('my_page.html',
                           username=username,
                           email=email,
                           gender=gender,
                           age=age,
                           height=height,
                           mass=mass,
                           activity_level=activity_level)

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

if __name__ == '__main__':
    app.run(debug=True)

