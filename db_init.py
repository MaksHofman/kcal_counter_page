import sqlite3

def creating_db():
    def connect_to_db():
        conn = sqlite3.connect('website.db')
        c = conn.cursor()
        return c, conn

    def creating_db_placeholder(c, conn):

        # creating main table(currently place holder)
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        mass INTEGER,
        age INTEGER,
        height INTEGER)
        ''')
        conn.commit()

    def creating_test_data(c, conn):
        c.execute('''
        INSERT INTO users (username, password, mass, age, height)
        VALUES ('qw', 'qw', 50, 20, 180)
        ''')
        c.execute('''
        INSERT INTO users (username, password)
        VALUES ('zx', 'zx')
        ''')
        conn.commit()

    def db_test_query(c, conn):
        c.execute('SELECT * FROM users')
        rows = c.fetchall()
        for row in rows:
            print(row)

    if __name__ == '__main__':
        c,conn = connect_to_db()
        creating_db_placeholder(c,conn)
        creating_test_data(c,conn)
        db_test_query(c,conn)
        conn.close()

if __name__ == '__main__':
    creating_db()