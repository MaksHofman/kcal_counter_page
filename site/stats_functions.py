import sqlite3
from datetime import datetime, timedelta
import re

def generacjia_daty_utowrzeniakonta() -> datetime:
    return datetime.now()

# Get user's streaks by email
def get_streaks_by_email(email):
    conn = sqlite3.connect('../database/website.db')
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
    conn = sqlite3.connect('../database/website.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT account_created_date FROM users WHERE email = "{email}";')
    output = cursor.fetchall()
    conn.close()
    account_created_date = datetime.strptime(output[0][0], '%Y-%m-%d %H:%M:%S.%f')
    account_created_date_str = account_created_date.strftime("%d.%m.%y")
    return account_created_date_str, account_created_date

def get_days_from_account_creation(account_created_date):
    return (datetime.now() - account_created_date).days
