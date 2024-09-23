from datetime import datetime, date, time, timedelta

from models import db, User, UserCalories

from history_functions import delete_kcal_from_history

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

        # Update user's streak
        update_streak(user)

        db.session.commit()


def get_calories_today_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        total_calories = db.session.query(db.func.sum(UserCalories.kcal_count)) \
            .filter(UserCalories.user_email == email) \
            .filter(db.func.date(UserCalories.entry_date) == date.today()) \
            .scalar()
        return total_calories if total_calories else 0
    else:
        raise ValueError("User does not exist")


def get_records_calories_today_by_email(email):
    return UserCalories.query.filter_by(user_email=email).filter(
        UserCalories.entry_date >= datetime.combine(date.today(), time.min),
        UserCalories.entry_date < datetime.combine(date.today(), time.max)
    ).order_by(UserCalories.entry_date.desc()).all()


def delete_calories_record_from_db(email, entry_id):
    record = calorie_record_owned_by_user(email, entry_id)
    if record:
        delete_kcal_from_history(email, record.kcal_count)
        db.session.delete(record)
        db.session.commit()
        return True
    return False


def update_goal_by_email(email, goal, goal_type):
    user = User.query.filter_by(email=email).first()

    if user:
        user.goal = goal
        user.goal_type = goal_type
        db.session.commit()
    else:
        raise ValueError("User does not exist")


def get_streak_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'current_streak': user.current_streak,
            'best_streak': user.best_streak
        }
    else:
        raise ValueError("User does not exist")


# Utility functions
def calorie_record_owned_by_user(email, entry_id):
    return UserCalories.query.filter_by(id=entry_id, user_email=email).first()


def update_streak(user):
    today = date.today()

    if user.last_day_user_checked_site == today:
        return

    if user.last_day_user_checked_site == today - timedelta(days=1):
        user.current_streak += 1
    else:
        user.current_streak = 1

    if user.current_streak > user.best_streak:
        user.best_streak = user.current_streak

    user.days_when_on_site += 1

    user.last_day_user_checked_site = today
