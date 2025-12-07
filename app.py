import streamlit as st
import json

# Load students and quizzes
def load_students():
    try:
        with open("students.json") as f:
            return json.load(f)
    except:
        return []

def load_quizzes():
    try:
        with open("quizzes.json") as f:
            return json.load(f)
    except:
        return {}

def load_results():
    try:
        with open("results.json") as f:
            return json.load(f)
    except:
        return []

def save_results(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

# Load data
students = load_students()
quizzes = load_quizzes()
results = load_results()

# --- STREAMLIT APP START ---
st.title("Student Quiz & Performance Analyzer")

menu = ["Student Management", "Quiz Creation", "Take Quiz", "Performance Analyzer"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- STUDENT MANAGEMENT ----------------
if choice == "Student Management":
    st.subheader("Add Student")
    name = st.text_input("Name")
    roll = st.text_input("Roll No")
    cls = st.text_input("Class")
    
    if st.button("Add Student"):
        if name and roll and cls:
            students.append({"name": name, "roll": roll, "class": cls})
            with open("students.json", "w") as f:
                json.dump(students, f, indent=4)
            st.success(f"Student {name} added!")
        else:
            st.error("Please fill all fields.")
    
    st.subheader("All Students")
    for s in students:
        st.write(f"{s['roll']} - {s['name']} ({s['class']})")

# ---------------- QUIZ CREATION ----------------
elif choice == "Quiz Creation":
    st.subheader("Add Quiz")
    quiz_name = st.text_input("Quiz Name / Subject")
    question = st.text_input("Question")
    option1 = st.text_input("Option A")
    option2 = st.text_input("Option B")
    option3 = st.text_input("Option C")
    option4 = st.text_input("Option D")
    correct = st.selectbox("Correct Option", ["A","B","C","D"])
    
    if st.button("Add Question"):
        if quiz_name and question and option1 and option2 and option3 and option4 and correct:
            if quiz_name not in quizzes:
                quizzes[quiz_name] = []
            quizzes[quiz_name].append({
                "question": question,
                "options": [option1, option2, option3, option4],
                "correct": correct
            })
            with open("quizzes.json", "w") as f:
                json.dump(quizzes, f, indent=4)
            st.success("Question added!")
        else:
            st.error("Fill all fields!")
    
    st.subheader("Existing Quizzes")
    st.write(list(quizzes.keys()))

# ---------------- TAKE QUIZ ----------------
elif choice == "Take Quiz":
    st.subheader("Take a Quiz")
    student_name = st.selectbox("Select Student", [s["name"] for s in students])
    quiz_name = st.selectbox("Select Quiz", list(quizzes.keys()))
    
    if st.button("Start Quiz"):
        st.session_state["answers"] = []
        for idx, q in enumerate(quizzes[quiz_name]):
            st.write(f"{idx+1}. {q['question']}")
            ans = st.radio("Select option", ["A","B","C","D"], key=f"q{idx}")
            st.session_state["answers"].append(ans)
        
        if st.button("Submit Quiz"):
            score = 0
            for q, a in zip(quizzes[quiz_name], st.session_state["answers"]):
                if q["correct"] == a:
                    score += 1
            results.append({
                "student": student_name,
                "quiz": quiz_name,
                "score": score,
                "total": len(quizzes[quiz_name])
            })
            save_results(results)
            st.success(f"{student_name} scored {score}/{len(quizzes[quiz_name])}")
