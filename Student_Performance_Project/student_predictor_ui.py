from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("data/student_performance_large.csv")

X = df.drop("final_score", axis=1)
y = df["final_score"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# =================================================================
# CLEAN NUMBER INPUT 
# =================================================================
def clean_number(value):
    try:
        value = value.replace("%","").replace(" ","").replace(",","")
        return float(value)
    except:
        return None

# =================================================================
# MAIN WINDOW 
# =================================================================
root = Tk()
root.title("Smart Student Performance Predictor")
root.geometry("1100x650")
root.configure(bg="#EEF2F5")
root.resizable(False, False)

# HEADER
header = Frame(root, bg="#2C3E50", height=70)
header.pack(fill="x")

Label(header, text="Smart Student Performance Prediction System",
      font=("Segoe UI", 22, "bold"), fg="white", bg="#2C3E50").pack(pady=15)


content = Frame(root, bg="#EEF2F5")
content.pack(fill="both", expand=True, padx=20, pady=10)

left_frame = Frame(content, bg="#EEF2F5")
left_frame.pack(side=LEFT, padx=40)

right_frame = Frame(content, bg="#EEF2F5")
right_frame.pack(side=RIGHT, padx=40)

entries = {}  


# =================================================================
# LEFT COLUMN INPUTS (with validation)
# =================================================================
def add_text_input(frame, label, key):
    Label(frame, text=label, font=("Segoe UI", 12, "bold"), bg="#EEF2F5").pack(anchor="w", pady=(10, 2))
    entry = Entry(frame, font=("Segoe UI", 12), width=30, bd=2, relief=SOLID)
    entry.pack(ipady=5)
    entries[key] = entry

# Study fields
add_text_input(left_frame, "How many hours does the student study daily?", "study_hours")
add_text_input(left_frame, "What was the student's previous exam score (%)?", "previous_score")
add_text_input(left_frame, "What is the student's attendance percentage?", "attendance")
add_text_input(left_frame, "How many assignments has the student submitted?", "assignments_submitted")


# Extra classes dropdown (0/1)
Label(left_frame, text="Does the student attend extra classes?", 
      font=("Segoe UI", 12, "bold"), bg="#EEF2F5").pack(anchor="w", pady=(10, 2))

extra_class = ttk.Combobox(left_frame, values=["0 - No", "1 - Yes"], state="readonly", width=27)
extra_class.pack(ipady=3)
entries["extra_classes"] = extra_class

# =================================================================
# RIGHT COLUMN INPUTS
# =================================================================
add_text_input(right_frame, "How many hours of internet usage per day?", "internet_usage")
add_text_input(right_frame, "How many hours does the student sleep daily?", "sleep_hours")

# Parental support dropdown
Label(right_frame, text="How much parental support does the student have? (0=None, 3=High)",
      font=("Segoe UI", 12, "bold"), bg="#EEF2F5").pack(anchor="w", pady=(10, 2))

parent_support = ttk.Combobox(right_frame, values=["0 - None", "1 - Low", "2 - Medium", "3 - High"],
                              state="readonly", width=27)
parent_support.pack(ipady=3)
entries["parental_support"] = parent_support

# Stress slider
Label(right_frame, text="Rate the student's exam stress (1-10)",
      font=("Segoe UI", 12, "bold"), bg="#EEF2F5").pack(anchor="w", pady=(10, 2))

stress_slider = Scale(right_frame, from_=1, to=10, orient=HORIZONTAL, length=250,
                      font=("Segoe UI", 10), bg="#EEF2F5")
stress_slider.set(5)
stress_slider.pack()
entries["exam_stress"] = stress_slider

# =================================================================
# RESULT BOX
# =================================================================
result_frame = Frame(root, bg="#EEF2F5")
result_frame.pack(pady=10)

result_label = Label(result_frame, text="Predicted Score: —",
                     font=("Segoe UI", 20, "bold"),
                     bg="#EEF2F5", fg="#2C3E50")
result_label.pack()

# =================================================================
# BUTTON FUNCTIONS
# =================================================================
def predict_score():
    values = []

    for key in ["study_hours", "previous_score", "attendance",
                "assignments_submitted", "internet_usage", "sleep_hours"]:

        raw = entries[key].get()
        val = clean_number(raw)

        if val is None:
            result_label.config(text="❌ Invalid input detected! Fix highlighted fields.")
            entries[key].config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            return
        else:
            entries[key].config(highlightthickness=0)

        values.append(val)

    # Dropdowns
    values.append(int(entries["extra_classes"].get()[0]))
    values.append(int(entries["parental_support"].get()[0]))

    # Slider
    values.append(entries["exam_stress"].get())

    # Predict
    prediction = model.predict([values])[0]
    result_label.config(text=f"Predicted Score: {round(prediction, 2)}")


def clear_all():
    for key, widget in entries.items():
        if isinstance(widget, Entry):
            widget.delete(0, END)
        elif isinstance(widget, ttk.Combobox):
            widget.set("")
        elif isinstance(widget, Scale):
            widget.set(5)
    result_label.config(text="Predicted Score: —")


# =================================================================
# BUTTONS
# =================================================================
button_frame = Frame(root, bg="#EEF2F5")
button_frame.pack(pady=20)

Button(button_frame, text="Predict", font=("Segoe UI", 14, "bold"),
       bg="#27AE60", fg="white", width=14, height=2,
       command=predict_score).grid(row=0, column=0, padx=40)

Button(button_frame, text="Clear", font=("Segoe UI", 14, "bold"),
       bg="#E74C3C", fg="white", width=14, height=2,
       command=clear_all).grid(row=0, column=1, padx=40)

root.mainloop()
