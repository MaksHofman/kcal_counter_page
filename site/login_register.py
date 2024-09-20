from datetime import date, datetime, timedelta
from models import db, User
import re

__login_check = r'^[A-Za-z]+$'
__password_check = r'^[A-Za-z0-9]+$'

def get_user_from_db(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.username, user.mass, user.age, user.height, user.email, user.gender, user.activity_level
    else:
        return None, None, None, None, None, None, None

def anti_sql_injection_login_check(login, password) -> bool:
    if re.match(__login_check, login) and re.match(__password_check, password):
        return True
    else:
        return False

# Checks if an email is already in use
def check_email_exists(email: str) -> bool:
    return User.query.filter_by(email=email).first() is not None


# Checks if login credentials are correct
def checking_if_login_correct(login: str, password: str) -> bool:
    user = User.query.filter_by(username=login, password=password).first()
    return user is not None


# Adds a user to the database
def add_user_to_db(username: str, email: str, password: str, creation_date: datetime) -> bool:
    try:
        if not check_email_exists(email):
            new_user = User(username=username, email=email, password=password, account_created_date=creation_date)
            user_streak_init(new_user)
            db.session.add(new_user)
            db.session.commit()
            print("User added successfully")
            return True
        else:
            print("Email already exists")
            return False
    except Exception as e:
        db.session.rollback()
        print(f"Error adding user to DB: {e}")
        return False


# Utility functions
def check_if_email_correct(email: str) -> bool:
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None


def user_streak_init(user):
    user.best_streak = 1
    user.current_streak = 1
    user.days_when_on_site = 1
    user.last_day_user_checked_site = date.today()
