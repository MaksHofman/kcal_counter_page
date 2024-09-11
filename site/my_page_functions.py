from flask import session
from models import db, User


def update_user_by_email(username, email, gender, age, height, mass, activity_level):
    user = User.query.filter_by(email=email).first()

    if user:
        user.username = username
        user.gender = gender
        user.age = age
        user.height = height
        user.mass = mass
        user.activity_level = activity_level

        db.session.commit()
    else:
        raise ValueError("User not found with the provided email")


def update_session_for_my_page(username, gender, age, height, mass, activity_level):
    session['username'] = username
    session['gender'] = gender
    session['age'] = age
    session['height'] = height
    session['mass'] = mass
    session['activity_level'] = activity_level
