from datetime import datetime, date, time, timedelta

from sqlalchemy import func, desc

from models import db, User, UserCalories, CaloriesHistory


def update_today_history(email, kcal_count):
    today = date.today()
    user = User.query.filter_by(email=email).first()

    if not user:
        return

    goal = user.goal if user.goal else 0

    entry_to_change = CaloriesHistory.query.filter_by(user_email=user.email, entry_date=today).first()

    if not entry_to_change:
        add_new_today_history_by_email(email, kcal_count, goal)
        db.session.commit()
        return

    try:
        kcal_count = int(kcal_count)
    except ValueError:
        return

    entry_to_change.kcal_count += kcal_count
    db.session.commit()


def update_today_history_goal(email, new_goal):
    today = date.today()
    user = User.query.filter_by(email=email).first()

    if not user:
        return

    entry_to_change = CaloriesHistory.query.filter_by(user_email=user.email, entry_date=today).first()

    if not entry_to_change:
        add_new_today_history_by_email(email, 0, new_goal)
    else:
        entry_to_change.goal = new_goal

    db.session.commit()


# To be reworked
def get_history_by_email(email):
    user = User.query.filter_by(email=email).first()

    if not user:
        return []

    return CaloriesHistory.query.filter_by(user_email=email).order_by(desc(CaloriesHistory.entry_date)).all()


# Utility functions
def add_new_today_history_by_email(email, kcal_count, user_goal):
    new_record = CaloriesHistory(user_email=email, kcal_count=kcal_count, goal=user_goal, entry_date=date.today())
    db.session.add(new_record)
    db.session.commit()
