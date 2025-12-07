import json
import tkinter as tk
from tkinter import ttk, messagebox

STUDENT_FILE = "students.json"

# Load existing students or return empty list
def load_students():
    try:
        with open(STUDENT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Save students to file
def save_students(data):
    with open(STUDENT_FILE, "w") as f:
        json.dump(data, f, indent=4)

class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("700x500")

        # Load student data
        self.students = load_students()

        tk.Label(root, text="STUDENT MANAGEMENT SYSTEM", font=("Arial", 18, "bold")).pack(pady=10)

        # Add student form
        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Roll No:", font=("Arial", 12)).grid(row=1, column=0)
        self.roll_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.roll_entry.grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Class:", font=("Arial", 12)).grid(row=2, column=0)
        self.class_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.class_entry.grid(row=2, column=1, padx=5)

        tk.Button(form_frame, text="Add Student", bg="green", fg="white",
                  font=("Arial", 12), command=self.add_student).grid(row=3, column=0, columnspan=2, pady=10)

        # Table for students
        self.tree = ttk.Treeview(root, columns=("Roll", "Name", "Class"), show="headings", height=10)
        self.tree.heading("Roll", text="Roll No")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Class", text="Class")

        self.tree.pack(pady=10)
        self.load_table()

    # Add student to list
    def add_student(self):
        name = self.name_entry.get()
        roll = self.roll_entry.get()
        cls = self.class_entry.get()

        if not name or not roll or not cls:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        new_student = {"name": name, "roll": roll, "class": cls}
        self.students.append(new_student)
        save_students(self.students)

        messagebox.showinfo("Success", "Student added successfully!")

        # Clear fields
        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)

        # Refresh table
        self.tree.insert("", tk.END, values=(roll, name, cls))

    # Load students into table
    def load_table(self):
        for s in self.students:
            self.tree.insert("", tk.END, values=(s["roll"], s["name"], s["class"]))


# Run independently
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()
