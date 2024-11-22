import tkinter as tk
from tkinter import messagebox
import pyfiglet
import requests
import json
from questions import questions  # Importing questions from questions.py

# Constants
LOG_FILE = "quiz_log.txt"
JOKES_API = "https://official-joke-api.appspot.com/jokes/random"

# State Variables
score = 0
current_question_index = 0
attempted_questions = set()

# Functions
def fetch_joke():
    """Fetch a random joke from an external API."""
    try:
        response = requests.get(JOKES_API)
        if response.status_code == 200:
            joke = response.json()
            return f"{joke['setup']} - {joke['punchline']}"
    except Exception as e:
        return f"Could not fetch joke: {e}"

def log_result(data):
    """Write quiz results to the log file."""
    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(data) + "\n")

def show_question():
    """Show the next question."""
    global current_question_index, score
    if current_question_index >= len(questions):
        messagebox.showinfo("Quiz Completed", f"You scored {score}/{len(questions)}!")
        root.destroy()
        return

    question_data = questions[current_question_index]
    question_label.config(text=question_data["question"])
    for idx, option in enumerate(question_data["options"]):
        option_buttons[idx].config(text=option, command=lambda opt=option: check_answer(opt))

def check_answer(selected_option):
    """Check if the selected option is correct."""
    global current_question_index, score
    question_data = questions[current_question_index]
    if selected_option == question_data["answer"]:
        messagebox.showinfo("Correct!", pyfiglet.figlet_format("Correct!"))
        score += 1
    else:
        messagebox.showerror("Wrong!", f"The correct answer was: {question_data['answer']}")
    current_question_index += 1
    show_question()

def start_quiz():
    """Start the quiz."""
    start_button.pack_forget()
    joke = fetch_joke()
    if joke:
        joke_label.config(text=joke)
    show_question()

# GUI Setup
root = tk.Tk()
root.title("Funny Quiz")
root.geometry("600x400")

# Widgets
start_button = tk.Button(root, text="Start Quiz", font=("Arial", 16), command=start_quiz)
start_button.pack(pady=20)

joke_label = tk.Label(root, text="", font=("Arial", 12), wraplength=500, justify="center")
joke_label.pack(pady=10)

question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=500, justify="center")
question_label.pack(pady=20)

option_buttons = [
    tk.Button(root, font=("Arial", 14)) for _ in range(4)
]
for btn in option_buttons:
    btn.pack(pady=5)

# Run the application
root.mainloop()
