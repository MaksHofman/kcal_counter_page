import sqlite3
from datetime import datetime, timedelta
import time
import os
database_path = 'site/database_tmp/website.db'
database_dir = '/database_tmp/'
def generacjia_daty_utowrzeniakonta() -> datetime:
    return datetime.now()

def creating_db():
    db_dir = os.path.dirname(database_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    def connect_to_db():
        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        return c, conn

    def creating_db_users(c, conn):

        # creating main table(currently place holder)
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL UNIQUE,
        email TEXT PRIMARY KEY NOT NULL UNIQUE,
        password TEXT NOT NULL,
        mass INTEGER,
        age INTEGER,
        height INTEGER,
        gender TEXT,
        goal TEXT,
        account_created_date DATE,
        activity_level TEXT,
        best_streak INTEGER,
        current_streak INTEGER,
        days_when_on_site INTEGER,
        added_produckts INTEGER,
        pr_chest INTEGER,
        last_day_user_checked_site DATE
       )
        ''')
        conn.commit()

    def creating_test_data(c, conn):

        c.execute('''
        INSERT INTO users (username, email, password, mass, age, height)
        VALUES ('qw','amogus@gmail.com', 'qw', 50, 20, 180)
        ''')
        c.execute('''
        INSERT INTO users (username, email, password)
        VALUES ('zx','ams@gmal.pl', 'zx')
        ''')



    def creating_db_products(c, conn):
            # creating products table(currently place holder)
            # prdukty to powina byc wartosc na 100g
            # jednostki to kcal i g
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            company TEXT NOT NULL,
            shop TEXT NOT NULL,
            mass INTEGER NOT NULL,
            energy_value FLOAT NOT NULL,
            fat FLOAT NOT NULL,
            saturated_fat FLOAT NOT NULL,
            carbohydrates FLOAT NOT NULL,
            sugars FLOAT NOT NULL,
            fiber FLOAT NOT NULL,
            proteins FLOAT NOT NULL,
            salts FLOAT NOT NULL,
            rating FLOAT NOT NULL
            )
            ''')
        conn.commit()
    def products_table_test_data_init(c, conn):
        c.execute('''
            INSERT INTO products (name, company, shop, mass, energy_value, fat, saturated_fat, carbohydrates, sugars, fiber, proteins, salts, rating)
            VALUES ('Lód Tripple Joy BLUEBERRY','Marletto', 'Biedronka', 76, 377, 25, 17, 35, 31, 0.5, 3.1, 0.1, 9.0)
            ''')
        c.execute('''
            INSERT INTO products (name, company, shop, mass, energy_value, fat, saturated_fat, carbohydrates, sugars, fiber, proteins, salts, rating)
            VALUES ('Lód w rożku o smaku JAGODA','Marletto', 'Biedronka', 94, 292, 12, 8.9, 43, 34, 0.5, 3.5, 0.14, 9.8)
            ''')
        conn.commit()

    def progress_table_creation(c, conn):
        c.execute('''
                   CREATE TABLE IF NOT EXISTS progress (
                    user_id TEXT,
                    progress_update INTEGER NOT NULL,
                    progress_update_date DATE NOT NULL,
                    progress_type TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users)
                   ''')
        conn.commit()

    def add_test_progress(c, conn):
        czas = generacjia_daty_utowrzeniakonta()
        c.execute(f'''
            INSERT INTO progress (user_id, progress_update,progress_update_date, progress_type)
            VALUES ("qw.qw@gmail.com", 25, "{czas}", 'mass')
            ''')
        conn.commit()
        time.sleep(10)
        czas = generacjia_daty_utowrzeniakonta()
        c.execute(f'''
            INSERT INTO progress (user_id, progress_update,progress_update_date, progress_type)
            VALUES ("qw.qw@gmail.com", 40, "{czas}", 'mass')
            ''')
        conn.commit()
        time.sleep(10)
        czas = generacjia_daty_utowrzeniakonta()
        c.execute(f'''
            INSERT INTO progress (user_id, progress_update,progress_update_date, progress_type)
            VALUES ("qw.qw@gmail.com", 60, "{czas}", 'mass')
            ''')
        conn.commit()
    def db_test_query(c, conn):
        c.execute('SELECT * FROM products')
        rows = c.fetchall()
        for row in rows:
            print(row)

    if __name__ == '__main__':
        c,conn = connect_to_db()
        creating_db_users(c,conn)
        #c.execute('''
        #INSERT INTO users (username,email, password, mass, age)
        #VALUES ('kerry','kerry.com@gmail.pl', 'zx', 60, 20)
        #''')
        #conn.commit()
        creating_test_data(c,conn)
        creating_db_products(c, conn)
        products_table_test_data_init(c, conn)
        progress_table_creation(c, conn)
        db_test_query(c,conn)
        add_test_progress(c, conn)
        print("koniec")
        conn.close()

if __name__ == '__main__':
    creating_db()