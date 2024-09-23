from datetime import datetime, date, time, timedelta

from sqlalchemy import func, desc

from models import db, User, UserCalories


def get_history_by_email(email):

    user = User.query.filter_by(email=email).first()

    if not user:
        return []

    return db.session.query(
        func.DATE(UserCalories.entry_date).label('date'),
        func.sum(UserCalories.kcal_count).label('calories'),
        User.goal).join(User, User.email == UserCalories.user_email).filter(UserCalories.user_email == email).group_by(
        func.DATE(UserCalories.entry_date), User.goal).order_by(desc(func.DATE(UserCalories.entry_date))).all()
