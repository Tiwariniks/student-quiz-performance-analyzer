import json
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

RESULT_FILE = "results.json"
STUDENT_FILE = "students.json"

def load_results():
    try:
        with open(RESULT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def load_students():
    try:
        with open(STUDENT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

class PerformanceAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Performance Analyzer")
        self.root.geometry("800x600")

        self.students = load_students()
        self.results = load_results()

        tk.Label(root, text="PERFORMANCE ANALYZER", font=("Arial", 18, "bold")).pack(pady=10)

        # Student selection
        tk.Label(root, text="Select Student:", font=("Arial", 14)).pack()
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(root, textvariable=self.student_var, state="readonly",
                                          values=[s["name"] for s in self.students])
        self.student_combo.pack(pady=5)

        tk.Button(root, text="View Student Performance", font=("Arial", 14), bg="green", fg="white",
                  command=self.show_student_performance).pack(pady=10)

        # Quiz selection
        quizzes = list({r["quiz"] for r in self.results})
        tk.Label(root, text="Select Quiz for Leaderboard:", font=("Arial", 14)).pack(pady=5)
        self.quiz_var = tk.StringVar()
        self.quiz_combo = ttk.Combobox(root, textvariable=self.quiz_var, state="readonly", values=quizzes)
        self.quiz_combo.pack(pady=5)

        tk.Button(root, text="Show Quiz Leaderboard", font=("Arial", 14), bg="blue", fg="white",
                  command=self.show_quiz_leaderboard).pack(pady=10)

    def show_student_performance(self):
        student_name = self.student_var.get()
        if not student_name:
            messagebox.showerror("Error", "Select a student first!")
            return

        student_results = [r for r in self.results if r["student"] == student_name]

        if not student_results:
            messagebox.showinfo("Info", f"No results found for {student_name}")
            return

        # Show in a simple window
        win = tk.Toplevel(self.root)
        win.title(f"{student_name} Performance")

        for idx, r in enumerate(student_results):
            tk.Label(win, text=f"{idx+1}. Quiz: {r['quiz']} - Score: {r['score']}/{r['total']}",
                     font=("Arial", 12)).pack(anchor="w")

        # Plot graph
        quizzes = [r["quiz"] for r in student_results]
        scores = [r["score"] for r in student_results]

        plt.figure(figsize=(8,4))
        plt.bar(quizzes, scores, color='orange')
        plt.xlabel("Quiz")
        plt.ylabel("Score")
        plt.title(f"{student_name}'s Performance")
        plt.show()

    def show_quiz_leaderboard(self):
        quiz_name = self.quiz_var.get()
        if not quiz_name:
            messagebox.showerror("Error", "Select a quiz first!")
            return

        quiz_results = [r for r in self.results if r["quiz"] == quiz_name]

        if not quiz_results:
            messagebox.showinfo("Info", f"No results found for {quiz_name}")
            return

        # Sort by score descending
        quiz_results.sort(key=lambda x: x["score"], reverse=True)

        win = tk.Toplevel(self.root)
        win.title(f"{quiz_name} Leaderboard")

        tk.Label(win, text=f"Leaderboard - {quiz_name}", font=("Arial", 16, "bold")).pack(pady=5)
        for idx, r in enumerate(quiz_results):
            tk.Label(win, text=f"{idx+1}. {r['student']} - {r['score']}/{r['total']}",
                     font=("Arial", 12)).pack(anchor="w")
