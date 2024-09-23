from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    mass = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=True)
    goal = db.Column(db.String, nullable=True)
    goal_type = db.Column(db.String, nullable=True)
    account_created_date = db.Column(db.Date, nullable=True)
    activity_level = db.Column(db.String, nullable=True)
    best_streak = db.Column(db.Integer, nullable=True)
    current_streak = db.Column(db.Integer, nullable=True)
    days_when_on_site = db.Column(db.Integer, nullable=True)
    added_products = db.Column(db.Integer, nullable=True)
    pr_chest = db.Column(db.Integer, nullable=True)
    last_day_user_checked_site = db.Column(db.Date, nullable=True)

    # Relationships
    progress = db.relationship('Progress', backref='user', lazy=True)
    user_calories = db.relationship('UserCalories', backref='user', lazy=True)
    calories_history = db.relationship('CaloriesHistory', backref='user', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    company = db.Column(db.String, nullable=False)
    shop = db.Column(db.String, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    energy_value = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    saturated_fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    sugars = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    salts = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)


class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)
    progress_update = db.Column(db.Integer, nullable=False)
    progress_update_date = db.Column(db.Date, nullable=False)
    progress_type = db.Column(db.String, nullable=False)


class UserCalories(db.Model):
    __tablename__ = 'user_calories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)
    kcal_count = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)


class CaloriesHistory(db.Model):
    __tablename__ = 'calories_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)
    kcal_count = db.Column(db.Integer, nullable=False)
    goal = db.Column(db.String, nullable=False)
    goal_type = db.Column(db.String, nullable=True)
    entry_date = db.Column(db.Date, nullable=False)
