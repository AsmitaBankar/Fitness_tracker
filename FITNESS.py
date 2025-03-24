import PySimpleGUI as sg
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def initialize_db():
    conn = sqlite3.connect("fitness_tracker.db")  # Create database file
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            exercise TEXT,
            duration INTEGER,
            calories INTEGER
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()  # Call this function at the start

def add_workout(date, exercise, duration, calories):
    if not date or not exercise or not duration or not calories:
        sg.popup_error("All fields are required!")
        return

    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workouts (date, exercise, duration, calories) VALUES (?, ?, ?, ?)",
                   (date, exercise, duration, calories))
    conn.commit()
    conn.close()
    
    sg.popup("Workout added successfully!")

def show_workouts():
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts")
    records = cursor.fetchall()
    conn.close()

    if not records:
        sg.popup("No workout records found.")
        return

    output = "ID | Date | Exercise | Duration | Calories Burned\n"
    output += "-" * 50 + "\n"

    for record in records:
        output += f"{record[0]} | {record[1]} | {record[2]} | {record[3]} min | {record[4]} cal\n"

    sg.popup_scrolled(output, title="Workout Records")

def plot_progress():
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, duration, calories FROM workouts")
    data = cursor.fetchall()
    conn.close()

    if not data:
        sg.popup("No workout records to plot.")
        return

    df = pd.DataFrame(data, columns=['Date', 'Duration', 'Calories'])

    plt.figure(figsize=(8, 5))
    plt.plot(df['Date'], df['Calories'], marker='o', label="Calories Burned", color='blue')
    plt.xlabel("Date")
    plt.ylabel("Calories")
    plt.title("Fitness Progress Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

layout = [
    [sg.Text("Date (YYYY-MM-DD):"), sg.InputText(key="DATE")],
    [sg.Text("Exercise:"), sg.InputText(key="EXERCISE")],
    [sg.Text("Duration (minutes):"), sg.InputText(key="DURATION")],
    [sg.Text("Calories Burned:"), sg.InputText(key="CALORIES")],
    [sg.Button("Add Workout"), sg.Button("Show Workouts"), sg.Button("Plot Progress"), sg.Button("Exit")]
]

window = sg.Window("Personal Fitness Tracker", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Add Workout":
        add_workout(values["DATE"], values["EXERCISE"], values["DURATION"], values["CALORIES"])
    elif event == "Show Workouts":
        show_workouts()
    elif event == "Plot Progress":
        plot_progress()

window.close()
