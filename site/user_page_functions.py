from datetime import datetime, date

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


def get_calories_today_by_email(email):
    today = date.today()

    user = User.query.filter_by(email=email).first()
    if user:
        total_calories = db.session.query(db.func.sum(UserCalories.kcal_count)) \
            .filter(UserCalories.user_email == email) \
            .filter(db.func.date(UserCalories.entry_date) == today) \
            .scalar()
        return total_calories if total_calories else 0
    else:
        raise ValueError("User does not exist")


def update_goal_by_email(email, goal):
    user = User.query.filter_by(email=email).first()

    if user:
        user.goal = goal
        db.session.commit()
    else:
        raise ValueError("User does not exist")
