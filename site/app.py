import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from models import db, User, Product, Progress
from db_init import database_path
from kcal_functions import *
from login_register import *
from my_page_functions import *
from stats_functions import *
from user_page_functions import *
from history_functions import *

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def home():
    print(database_path)
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register(confirm_password=None):
    if request.method == 'POST':
        login = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        #wczytanie z pamieci loginu przed errorem
        if login == "" and session.get('input_username') != None:
            login = session.get('input_username')
        else:
            session['input_username'] = login

        input_username = login
        #wczytanie z pamieci emaila przed errorem
        if email == "" and session.get('input_email') != None:
            email = session.get('input_email')
        else:
            session['input_email'] = email

        if check_if_email_correct(email):
            input_mail = email
        else:
            return render_template('register.html', input_username=input_username, input_mail="Email",
                                   wrong_register="Email is incorrect")
        if checking_if_login_correct(login, None):
            return render_template('register.html', input_username="Username", input_mail="Email",
                                   wrong_register='Account already exists')
        elif check_email_exists(email):
            return render_template('register.html', input_username=input_username,
                                   wrong_register='Email already exists')
        else:
            if password == confirm_password:
                was_successful = add_user_to_db(login, email, password, account_creation_date_generation())
                if was_successful:
                    return redirect(url_for('login'))
                else:
                    return "An error occurred during login"
            else:
                return render_template('register.html', input_username=input_username, input_mail=input_mail,
                                       wrong_register='Passwords do not match. Please try again.')
    return render_template('register.html', input_username="Username", input_mail="Email")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        if checking_if_login_correct(login, password) and anti_sql_injection_login_check(login, password):
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


@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if 'logged_in' in session:
        email = session.get('email')

        if request.method == 'POST':
            new_progress_int = request.form['inputNumber']
            new_progress_type = request.form['selectOptions']
            add_new_record_to_progress(email, new_progress_int, new_progress_type)

        return render_template('progress.html')
    else:
        return redirect(url_for('login'))


@app.route('/progress_data', methods=['GET'])
def get_progress_data():
    if 'logged_in' in session:
        email = session.get('email')
        progress_type = request.args.get('progress_type', 'mass')

        output_int, output_date = get_progress_update(email, progress_type)

        return jsonify({
            'data': output_int,
            'labels': output_date
        })
    else:
        return jsonify({'error': 'Not logged in'}), 401



@app.route('/stats')
def stats():
    if 'logged_in' in session:
        email = session.get('email')

        account_created_date, days_from_account_creation = get_account_creation_info(email)
        best_streak, current_streak, days_when_on_site = get_streaks_by_email(email)
        ttde = calculate_tdee(
            calculate_bmr(session.get('mass'), session.get('height'), session.get('age'), session.get('gender')),
            activity_level=session.get('activity_level'))
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
    if 'logged_in' in session:
        bmr = calculate_bmr(session.get('mass'), session.get('height'), session.get('age'), session.get('gender'))
        ttde = calculate_tdee(bmr, activity_level=session.get('activity_level'))
        daily_goal_holder = get_kcal_goal_from_db(session.get('email'))
        kcal_goal = daily_goal_holder
        return render_template('kcal_calculator.html', bmr=bmr, ttde=ttde, kcal_goal=kcal_goal)
    else:
        return redirect(url_for('login'))


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


@app.route('/update_user', methods=['POST'])
def update_user():
    email = session['email']

    if email:
        username = request.form.get('username')
        gender = request.form.get('gender')
        age = request.form.get('age')
        height = request.form.get('height')
        mass = request.form.get('mass')
        activity_level = request.form.get('activity_level')

        # Update the user in the database
        update_user_by_email(username, email, gender, age, height, mass, activity_level)

        # Update the session with the new data
        update_session_for_my_page(username, gender, age, height, mass, activity_level)

        return redirect(url_for('my_page'))
    else:
        return redirect(url_for('login'))


@app.route('/history')
def history():
    if 'logged_in' in session:
        email = session.get('email')

        history_records = get_history_by_email(email)

        return render_template('history.html', history_records=history_records)
    else:
        return redirect(url_for('login'))


@app.route('/user_page')
def user_page():
    if 'logged_in' in session:
        username = session['username']
        email = session['email']

        caloric_goal = get_goal_by_email(email) if get_goal_by_email(email) else "Not set"
        calories_today = get_calories_today_by_email(email)
        calories_today_records = get_records_calories_today_by_email(email)

        return render_template(
            'user_page.html',
            username=username,
            goal=caloric_goal,
            calories=calories_today,
            calories_records=calories_today_records
        )
    else:
        return redirect(url_for('login'))


@app.route('/update_goal', methods=['POST'])
def update_goal():
    if 'logged_in' in session:
        email = session['email']
        new_goal = request.form.get('goal')
        goal_type = request.form.get('goal_type')

        if goal_type not in ["bulk", "cut"]:
            return redirect(url_for('user_page'))

        if email and new_goal and goal_type:
            update_goal_by_email(email, new_goal, goal_type)
            update_today_history_goal(email, new_goal, goal_type)
            return redirect(url_for('user_page'))
        else:
            return "An error occurred. Please try again."
    else:
        return redirect(url_for('login'))


@app.route('/add_user_calories', methods=['POST'])
def add_user_calories():
    if 'logged_in' in session:
        email = session['email']
        kcal_count = request.form.get('kcal_count')

        if email and kcal_count:
            add_user_calories_by_email(email, kcal_count)
            update_today_history(email, kcal_count)
            return redirect(url_for('user_page'))
        else:
            return "An error occurred while adding calories. Please try again."
    else:
        return redirect(url_for('login'))


@app.route('/delete_calories/<int:entry_id>', methods=['POST'])
def delete_calories(entry_id):
    if 'logged_in' in session:
        email = session['email']

        if email and entry_id:
            if delete_calories_record_from_db(email, entry_id):
                return redirect(url_for('user_page'))
            else:
                return "An error occurred. Please try again."
        return "An error occurred. Please try again."
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
