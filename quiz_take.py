import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

QUIZ_FILE = "quizzes.json"
STUDENT_FILE = "students.json"
RESULT_FILE = "results.json"

# Load data
def load_quizzes():
    try:
        with open(QUIZ_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def load_students():
    try:
        with open(STUDENT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def load_results():
    try:
        with open(RESULT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_results(results):
    with open(RESULT_FILE, "w") as f:
        json.dump(results, f, indent=4)

class QuizTakeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Taking Module")
        self.root.geometry("800x600")

        self.students = load_students()
        self.quizzes = load_quizzes()
        self.results = load_results()

        tk.Label(root, text="QUIZ TAKING MODULE", font=("Arial", 18, "bold")).pack(pady=10)

        # Student selection
        tk.Label(root, text="Select Student:", font=("Arial", 14)).pack()
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(root, textvariable=self.student_var, state="readonly",
                                          values=[s["name"] for s in self.students])
        self.student_combo.pack(pady=5)

        # Quiz selection
        tk.Label(root, text="Select Quiz (Subject):", font=("Arial", 14)).pack()
        self.quiz_var = tk.StringVar()
        self.quiz_combo = ttk.Combobox(root, textvariable=self.quiz_var, state="readonly",
                                       values=list(self.quizzes.keys()))
        self.quiz_combo.pack(pady=5)

        tk.Button(root, text="Start Quiz", font=("Arial", 14), bg="green", fg="white",
                  command=self.start_quiz).pack(pady=10)

        # Frame for questions
        self.q_frame = tk.Frame(root)
        self.q_frame.pack(pady=10, fill="both", expand=True)

        self.current_questions = []
        self.answer_vars = []

    def start_quiz(self):
        student_name = self.student_var.get()
        quiz_subject = self.quiz_var.get()

        if not student_name or not quiz_subject:
            messagebox.showerror("Error", "Select student and quiz first!")
            return

        self.current_questions = self.quizzes.get(quiz_subject, [])
        if not self.current_questions:
            messagebox.showerror("Error", "No questions in this quiz.")
            return

        # Clear previous frame
        for widget in self.q_frame.winfo_children():
            widget.destroy()

        self.answer_vars = []

        # Display questions
        for idx, q in enumerate(self.current_questions):
            tk.Label(self.q_frame, text=f"{idx+1}. {q['question']}", font=("Arial", 12, "bold")).pack(anchor="w")
            ans_var = tk.StringVar(value="")
            self.answer_vars.append(ans_var)
            for i, opt in enumerate(q["options"]):
                tk.Radiobutton(self.q_frame, text=f"{chr(65+i)}. {opt}", variable=ans_var, value=chr(65+i)).pack(anchor="w")

        tk.Button(self.q_frame, text="Submit Quiz", font=("Arial", 14), bg="blue", fg="white",
                  command=self.submit_quiz).pack(pady=10)

    def submit_quiz(self):
        student_name = self.student_var.get()
        quiz_subject = self.quiz_var.get()

        score = 0
        for q, ans_var in zip(self.current_questions, self.answer_vars):
            if ans_var.get().upper() == q["correct"].upper():
                score += 1  # 1 mark per question

        # Save result
        self.results.append({
            "student": student_name,
            "quiz": quiz_subject,
            "score": score,
            "total": len(self.current_questions)
        })
        save_results(self.results)

        messagebox.showinfo("Result", f"{student_name} scored {score}/{len(self.current_questions)}")
        self.q_frame.destroy()
