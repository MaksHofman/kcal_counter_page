CREATE TABLE IF NOT EXISTS users (
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    mass INTEGER,
    age INTEGER,
    height INTEGER,
    gender TEXT,
    goal TEXT,
    account_created_date DATE,
    activity_level TEXT,
    best_streak INTEGER,
    current_streak INTEGER,
    days_when_on_site INTEGER,
    added_products INTEGER, 
    pr_chest INTEGER,
    last_day_user_checked_site DATE,
    PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL UNIQUE,
    company TEXT NOT NULL,
    shop TEXT NOT NULL,
    mass INTEGER NOT NULL,
    energy_value REAL NOT NULL, 
    fat REAL NOT NULL,
    saturated_fat REAL NOT NULL,
    carbohydrates REAL NOT NULL,
    sugars REAL NOT NULL,
    fiber REAL NOT NULL,
    proteins REAL NOT NULL,
    salts REAL NOT NULL,
    rating REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS progress (
    user_id TEXT,
    progress_update INTEGER NOT NULL,
    progress_update_date DATE NOT NULL,
    progress_type TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(email)
);