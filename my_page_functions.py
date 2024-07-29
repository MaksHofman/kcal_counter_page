import sqlite3

def update_user_by_email(username, email, gender, age, height, mass, activity_level):
    conn = sqlite3.connect('website.db')
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
