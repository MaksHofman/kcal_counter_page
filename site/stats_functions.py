import sqlite3
from datetime import datetime, timedelta
from models import User


def account_creation_date_generation() -> datetime:
    return datetime.now()


# Get user's streaks by email
def get_streaks_by_email(email):
    user = User.query.filter_by(email=email).first()

    if user:
        return user.best_streak, user.current_streak, user.days_when_on_site
    else:
        return None, None, None

# This function gets all the necessary info about account creation
def get_account_creation_info(email):
    account_created_date_str, account_created_date = get_account_created_date(email)
    days_from_account_creation = get_days_from_account_creation(account_created_date)
    return account_created_date_str, days_from_account_creation


def get_account_created_date(email):
    user = User.query.filter_by(email=email).first()
    if user and user.account_created_date:
        account_created_date_str = user.account_created_date.strftime("%d.%m.%y")
        return account_created_date_str, user.account_created_date
    else:
        return None, None


def get_days_from_account_creation(account_created_date):
    if not account_created_date:
        return None

    return (datetime.now().date() - account_created_date).days
