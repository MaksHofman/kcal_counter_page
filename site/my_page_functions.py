import sqlite3

from flask import session


def update_user_by_email(username, email, gender, age, height, mass, activity_level, database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Define the SQL update query
    update_query = '''
    UPDATE users
    SET username = ?, gender = ?, age = ?, height = ?, mass = ?, activity_level = ?
    WHERE email = ?
    '''

    # Execute the query with the provided parameters
    cursor.execute(update_query, (username, gender, age, height, mass, activity_level, email))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def update_session_for_my_page(username, gender, age, height, mass, activity_level):
    session['username'] = username
    session['gender'] = gender
    session['age'] = age
    session['height'] = height
    session['mass'] = mass
    session['activity_level'] = activity_level