import tkinter as tk
from student_management import StudentManagementGUI
from quiz_creation import QuizCreatorGUI  # NEW IMPORT
from quiz_take import QuizTakeGUI  # NEW
from performance_analyzer import PerformanceAnalyzerGUI  # NEW
def open_student_management():
    win = tk.Toplevel(root)
    StudentManagementGUI(win)

def open_quiz_creator():
    win = tk.Toplevel(root)
    QuizCreatorGUI(win)

# Main window
root = tk.Tk()
root.title("Student Quiz & Performance Analyzer")
root.geometry("500x400")

tk.Label(root, text="MAIN MENU", font=("Arial", 22, "bold")).pack(pady=20)

tk.Button(root, text="Student Management System", font=("Arial", 14), width=30,
          command=open_student_management).pack(pady=10)

tk.Button(root, text="Quiz Creation Module", font=("Arial", 14), width=30,
          command=open_quiz_creator).pack(pady=10)
tk.Button(root, text="Start Quiz", font=("Arial", 14), width=30,
          command=lambda: QuizTakeGUI(tk.Toplevel(root))).pack(pady=10)
tk.Button(root, text="Performance Analyzer", font=("Arial", 14), width=30,
          command=lambda: PerformanceAnalyzerGUI(tk.Toplevel(root))).pack(pady=10)
root.mainloop()
