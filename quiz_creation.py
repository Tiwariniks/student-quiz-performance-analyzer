import json
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext

QUIZ_FILE = "quizzes.json"

# Load existing quizzes or create empty structure
def load_quizzes():
    try:
        with open(QUIZ_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save quizzes to file
def save_quizzes(data):
    with open(QUIZ_FILE, "w") as f:
        json.dump(data, f, indent=4)

class QuizCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Creation Module")
        self.root.geometry("700x600")

        self.quizzes = load_quizzes()

        # Title
        tk.Label(root, text="QUIZ CREATION MODULE", font=("Arial", 18, "bold")).pack(pady=10)

        # Subject Input
        tk.Label(root, text="Enter Subject:", font=("Arial", 14)).pack()
        self.subject_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.subject_entry.pack(pady=5)

        # Manual Question Section
        tk.Label(root, text="Enter Question:", font=("Arial", 14)).pack()
        self.question_entry = tk.Entry(root, font=("Arial", 14), width=50)
        self.question_entry.pack(pady=5)

        tk.Label(root, text="Option A:", font=("Arial", 12)).pack()
        self.a_entry = tk.Entry(root, font=("Arial", 12), width=40)
        self.a_entry.pack()

        tk.Label(root, text="Option B:", font=("Arial", 12)).pack()
        self.b_entry = tk.Entry(root, font=("Arial", 12), width=40)
        self.b_entry.pack()

        tk.Label(root, text="Option C:", font=("Arial", 12)).pack()
        self.c_entry = tk.Entry(root, font=("Arial", 12), width=40)
        self.c_entry.pack()

        tk.Label(root, text="Option D:", font=("Arial", 12)).pack()
        self.d_entry = tk.Entry(root, font=("Arial", 12), width=40)
        self.d_entry.pack()

        # Correct Answer
        tk.Label(root, text="Correct Option (A/B/C/D):", font=("Arial", 12)).pack(pady=3)
        self.correct_entry = tk.Entry(root, font=("Arial", 12), width=10)
        self.correct_entry.pack()

        tk.Button(root, text="Add Question Manually", font=("Arial", 14), bg="green", fg="white",
                  command=self.add_manual_question).pack(pady=10)

        # Auto generate button
        tk.Button(root, text="Auto Generate Questions", font=("Arial", 14), bg="blue", fg="white",
                  command=self.auto_generate).pack(pady=10)

        # Save quiz button
        tk.Button(root, text="Save Quiz", font=("Arial", 14), bg="purple", fg="white",
                  command=self.save_quiz).pack(pady=15)

        # Text box to show generated questions
        self.display_box = scrolledtext.ScrolledText(root, width=80, height=10, font=("Arial", 10))
        self.display_box.pack(pady=10)

        self.current_quiz = []

    # Add question manually
    def add_manual_question(self):
        q = self.question_entry.get()
        a = self.a_entry.get()
        b = self.b_entry.get()
        c = self.c_entry.get()
        d = self.d_entry.get()
        correct = self.correct_entry.get().upper()

        if not q or not a or not b or not c or not d or correct not in ("A", "B", "C", "D"):
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return

        question_data = {
            "question": q,
            "options": [a, b, c, d],
            "correct": correct
        }

        self.current_quiz.append(question_data)
        self.display_box.insert(tk.END, f"Added: {q}\n")
        messagebox.showinfo("Success", "Question Added!")

        # Clear fields
        self.question_entry.delete(0, tk.END)
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.c_entry.delete(0, tk.END)
        self.d_entry.delete(0, tk.END)
        self.correct_entry.delete(0, tk.END)

    # Auto generate 5 questions using AI (me)
    def auto_generate(self):
        subject = self.subject_entry.get().strip()
        if not subject:
            messagebox.showerror("Error", "Enter a subject first.")
            return

        generated = generate_questions(subject)

        for q in generated:
            self.current_quiz.append(q)
            self.display_box.insert(tk.END, f"AI: {q['question']}\n")

        messagebox.showinfo("Done", "5 questions auto-generated!")

    # Save quiz to file
    def save_quiz(self):
        subject = self.subject_entry.get().strip().lower()

        if not subject:
            messagebox.showerror("Error", "Subject cannot be empty!")
            return

        if subject not in self.quizzes:
            self.quizzes[subject] = []

        self.quizzes[subject].extend(self.current_quiz)
        save_quizzes(self.quizzes)
        messagebox.showinfo("Saved", f"Quiz saved under subject: {subject}")
        self.current_quiz = []


# AI Question Generator (simple built-in generator using fixed pattern)
def generate_questions(subject):
    base_questions = [
        {
            "question": f"What is {subject}?",
            "options": ["Definition 1", "Definition 2", "Definition 3", "Definition 4"],
            "correct": "A"
        },
        {
            "question": f"Why is {subject} important?",
            "options": ["Reason A", "Reason B", "Reason C", "Reason D"],
            "correct": "B"
        },
        {
            "question": f"Which statement is true about {subject}?",
            "options": ["Statement 1", "Statement 2", "Statement 3", "Statement 4"],
            "correct": "C"
        },
        {
            "question": f"{subject} is related to which concept?",
            "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
            "correct": "D"
        },
        {
            "question": f"Identify the correct application of {subject}.",
            "options": ["App 1", "App 2", "App 3", "App 4"],
            "correct": "A"
        }
    ]

    return base_questions


# Run independently
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizCreatorGUI(root)
    root.mainloop()
import json
import tkinter as tk