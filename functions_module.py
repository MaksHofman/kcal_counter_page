import sqlite3
from datetime import datetime, timedelta
import re

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
