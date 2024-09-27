import sqlite3
from datetime import datetime, timedelta, date

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from models import db, User, Progress


def get_date_now() -> datetime:
    return datetime.now()


def get_kcal_goal_from_db(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.goal
    return None


def get_progress_update(email: str, progress_type: str) -> tuple[list, list]:
    user = User.query.filter_by(email=email).first()
    if user:
        progress_records = Progress.query.filter_by(user_id=user.email, progress_type=progress_type).order_by(Progress.progress_update_date.asc()).all()

        output_int = [record.progress_update for record in progress_records]
        output_date = [record.progress_update_date.strftime('%Y-%m-%d') for record in progress_records]
        return output_int, output_date
    return [], []


def add_new_record_to_progress(email, int_record, type_record):
    user = User.query.filter_by(email=email).first()
    if user:
        today = date.today()

        existing_progress = Progress.query.filter_by(user_id=user.email,
                                                     progress_type=type_record,
                                                     progress_update_date=today).first()

        if existing_progress:
            existing_progress.progress_update = float(int_record)

        else:
            new_progress = Progress(
                user_id=user.email,
                progress_update=float(int_record),
                progress_update_date=get_date_now(),
                progress_type=type_record
            )
            db.session.add(new_progress)
        db.session.commit()


def calculate_bmr(weight, height, age, gender):
    if not all([weight, height, age, gender]):
        return 0
    
    weight = int(weight)
    age = int(age)
    height = int(height)
    """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation"""
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        # raise ValueError("Gender not recognized. Use 'male' or 'female'.")
        # if gender is not set yet return 0
        return 0
    return int(round(bmr, 0))


def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure (TDEE)"""

    if bmr == 0:
        return 'Not available yet. Visit <a href="/my_page">My Page</a> to update your account'

    activity_factors = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'super active': 1.9
    }

    if activity_level not in activity_factors:
        raise ValueError(
            "Activity level not recognized. Choose from 'sedentary', 'lightly active', 'moderately active', 'very active', 'super active'.")

    tdee = bmr * activity_factors[activity_level]
    return int(round(tdee, 0))


def calculate_bulking_calories(tdee, bulking_percentage):
    """Calculate calories for bulking phase"""
    bulking_calories = tdee + (tdee * bulking_percentage)
    return bulking_calories


def calculate_cutting_calories(tdee, cutting_percentage):
    """Calculate calories for cutting phase"""
    cutting_calories = tdee - (tdee * cutting_percentage)
    return cutting_calories


def kcal_calkulator(mass, height, age):
    print(mass, height, age)


if __name__ == "__main__":
    output_int, output_date = get_progress_update("qw.qw@gmail.com", "mass")
    make_graf_out_of_progress(output_int, output_date, "mass")
    print(output_int + output_date)
