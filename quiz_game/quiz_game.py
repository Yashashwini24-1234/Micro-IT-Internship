import tkinter as tk
from tkinter import ttk
import json
import random
import time

# Load questions
with open("questions.json", "r") as f:
    all_questions = json.load(f)

# Initialize main window
root = tk.Tk()
root.title("Quiz Game")
root.geometry("650x500")

# Variables
selected_option = tk.StringVar()
questions = []
options = []
q_index = 0
score = 0
review = []
time_left = 30
timer_id = None
question_start_time = 0

# Functions
def start_quiz():
    global questions, q_index, score, review
    random.shuffle(all_questions)
    questions = all_questions
    q_index = 0
    score = 0
    review = []
    start_btn.pack_forget()
    result_box.pack_forget()
    submit_btn.pack_forget()
    show_question()

def show_question():
    global time_left, timer_id, question_start_time
    question = questions[q_index]
    question_label.config(text=f"Q{q_index + 1}: {question['question']}")
    selected_option.set(None)

    option_keys = ["A", "B", "C", "D"]
    for i in range(4):
        key = option_keys[i]
        text = f"{key}. {question[key]}"
        options[i].config(text=text, value=key)
        options[i].deselect()
        options[i].pack()

    next_btn.pack(pady=10)
    submit_btn.pack_forget()
    time_left = 30
    question_start_time = time.time()
    update_timer()

def update_timer():
    global time_left, timer_id
    timer_label.config(text=f"Time Left: {time_left}s")
    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, update_timer)
    else:
        next_question()

def next_question():
    global q_index, score, timer_id
    root.after_cancel(timer_id)
    selected = selected_option.get()
    question = questions[q_index]
    correct = question["answer"]

    time_taken = int(time.time() - question_start_time)
    selected_text = question.get(selected, "No Answer")
    correct_text = question[correct]

    review.append(
        (
            question["question"],
            selected_text,
            correct_text,
            time_taken
        )
    )

    if selected == correct:
        score += 1

    q_index += 1
    if q_index < len(questions):
        show_question()
    else:
        question_label.config(text="Click Submit to see your results.")
        for opt in options:
            opt.pack_forget()
        next_btn.pack_forget()
        submit_btn.pack(pady=10)
        timer_label.config(text="")

def show_result():
    question_label.config(text=f"Quiz Over!\nYour Score: {score}/{len(questions)}")
    submit_btn.pack_forget()

    result_box.delete("1.0", tk.END)
    for idx, (q, u, c, t) in enumerate(review, 1):
        result_box.insert(tk.END, f"Q{idx}: {q}\nYour Answer: {u}\nCorrect Answer: {c}\nTime Taken: {t}s\n\n")

    result_box.pack(expand=True, fill="both", padx=10, pady=10)

# UI Widgets
question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=600)
question_label.pack(pady=20)

# Radiobuttons
for _ in range(4):
    rb = tk.Radiobutton(
        root,
        text="",
        variable=selected_option,
        value="",
        font=("Arial", 14),
        anchor='w',
        width=50,
        padx=10, pady=5
    )
    options.append(rb)

next_btn = tk.Button(root, text="Next", command=next_question)
submit_btn = tk.Button(root, text="Submit", command=show_result)

timer_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
timer_label.pack()

result_box = tk.Text(root, wrap=tk.WORD, height=10, font=("Arial", 12))

start_btn = tk.Button(root, text="Start Quiz", command=start_quiz)
start_btn.pack(pady=10)

# Main loop
root.mainloop()
