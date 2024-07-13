import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# zwraca wartosci
def get_progress_update(email: str, type: str) -> tuple[list, list]:
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    cursor.execute(f'''SELECT progress_update, progress_update_date FROM progress
                       WHERE user_id = "{email}" AND progress_type="{type}"
                       ORDER BY progress_update_date asc;''')
    queary_output = cursor.fetchall()
    conn.close()
    output_int = []
    output_date = []
    for out in queary_output:
        output_int.append(out[0])
        output_date.append(out[1])
    return output_int, output_date

def make_graf_out_of_progress(output_int, output_date, type):
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date() for date in output_date]
    # Plotting the time series data
    plt.figure(figsize=(10, 5))
    plt.plot(dates, output_int, marker='o', linestyle='-', color='b')

    # Formatting the plot
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

    plt.title(f'Progress of {type} Measurements Over Time')
    plt.xlabel('Date')
    plt.ylabel(type)
    plt.grid(True)
    #plt.show()
    plt.savefig(f'static/plots_saved_to_display/{dates[-1]}.png')


def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation"""
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender not recognized. Use 'male' or 'female'.")
    return bmr


def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure (TDEE)"""
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
    return tdee
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
    output_int,output_date  = get_progress_update("qw.qw@gmail.com", "mass")
    make_graf_out_of_progress(output_int,output_date, "mass")
    print(output_int + output_date)