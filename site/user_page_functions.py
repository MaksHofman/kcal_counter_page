from datetime import datetime

from models import db, User, UserCalories


def get_goal_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user.goal


def add_user_calories_by_email(email, kcal_count):

    # Verify that the user exists
    user = User.query.filter_by(email=email).first()
    if user:
        new_calories_entry = UserCalories(
            user_email=email,
            kcal_count=kcal_count,
            entry_date=datetime.now().replace(microsecond=0),
        )

        db.session.add(new_calories_entry)
        db.session.commit()

def update_goal_by_email(email, goal):
    user = User.query.filter_by(email=email).first()

    if user:
        user.goal = goal
        db.session.commit()
    else:
        raise ValueError("User does not exist")
