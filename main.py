import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ─────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────
def create_database():
    conn = sqlite3.connect("results.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT UNIQUE NOT NULL,
        class_name TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT NOT NULL,
        marks INTEGER NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')
    conn.commit()
    conn.close()

# ─────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2e")
        self.show_login()

    # ── LOGIN PAGE ──
    def show_login(self):
        self.clear()
        tk.Label(self.root, text="Student Result Management System",
                 font=("Arial", 20, "bold"), bg="#1e1e2e", fg="white").pack(pady=30)

        frame = tk.Frame(self.root, bg="#2e2e3e", padx=40, pady=40)
        frame.pack()

        tk.Label(frame, text="Username", bg="#2e2e3e", fg="white", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        self.username = tk.Entry(frame, font=("Arial", 12), width=25)
        self.username.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="Password", bg="#2e2e3e", fg="white", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        self.password = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
        self.password.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(frame, text="Login", font=("Arial", 12, "bold"),
                  bg="#7c3aed", fg="white", width=20, command=self.login).grid(row=2, column=0, columnspan=2, pady=20)

    def login(self):
        if self.username.get() == "admin" and self.password.get() == "admin123":
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials!\nUsername: admin\nPassword: admin123")

    # ── DASHBOARD ──
    def show_dashboard(self):
        self.clear()
        tk.Label(self.root, text="Dashboard", font=("Arial", 18, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=20)

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=20)

        buttons = [
            ("➕ Add Student", self.show_add_student),
            ("📝 Enter Marks", self.show_enter_marks),
            ("📊 View Results", self.show_results),
            ("🚪 Logout", self.show_login),
        ]

        for text, cmd in buttons:
            tk.Button(btn_frame, text=text, font=("Arial", 13), bg="#7c3aed",
                      fg="white", width=20, height=2, command=cmd).pack(pady=10)

    # ── ADD STUDENT ──
    def show_add_student(self):
        self.clear()
        tk.Label(self.root, text="Add Student", font=("Arial", 16, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=20)

        frame = tk.Frame(self.root, bg="#2e2e3e", padx=40, pady=30)
        frame.pack()

        labels = ["Student Name", "Roll Number", "Class"]
        self.student_entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label, bg="#2e2e3e", fg="white",
                     font=("Arial", 12)).grid(row=i, column=0, pady=10, sticky="w")
            entry = tk.Entry(frame, font=("Arial", 12), width=25)
            entry.grid(row=i, column=1, pady=10, padx=10)
            self.student_entries[label] = entry

        tk.Button(frame, text="Save Student", font=("Arial", 12, "bold"),
                  bg="#7c3aed", fg="white", width=20,
                  command=self.save_student).grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(self.root, text="← Back", font=("Arial", 11),
                  bg="#444", fg="white", command=self.show_dashboard).pack(pady=5)

    def save_student(self):
        name = self.student_entries["Student Name"].get().strip()
        roll = self.student_entries["Roll Number"].get().strip()
        cls  = self.student_entries["Class"].get().strip()

        if not name or not roll or not cls:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        try:
            conn = sqlite3.connect("results.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, roll_no, class_name) VALUES (?, ?, ?)",
                           (name, roll, cls))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
            for e in self.student_entries.values():
                e.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll number already exists!")

    # ── ENTER MARKS ──
    def show_enter_marks(self):
        self.clear()
        tk.Label(self.root, text="Enter Marks", font=("Arial", 16, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=20)

        frame = tk.Frame(self.root, bg="#2e2e3e", padx=40, pady=30)
        frame.pack()

        tk.Label(frame, text="Roll Number", bg="#2e2e3e", fg="white",
                 font=("Arial", 12)).grid(row=0, column=0, pady=8, sticky="w")
        self.marks_roll = tk.Entry(frame, font=("Arial", 12), width=20)
        self.marks_roll.grid(row=0, column=1, pady=8, padx=10)

        subjects = ["Maths", "Physics", "Chemistry", "English", "Computer"]
        self.marks_entries = {}

        for i, sub in enumerate(subjects):
            tk.Label(frame, text=sub, bg="#2e2e3e", fg="white",
                     font=("Arial", 12)).grid(row=i+1, column=0, pady=6, sticky="w")
            entry = tk.Entry(frame, font=("Arial", 12), width=20)
            entry.grid(row=i+1, column=1, pady=6, padx=10)
            self.marks_entries[sub] = entry

        tk.Button(frame, text="Save Marks", font=("Arial", 12, "bold"),
                  bg="#7c3aed", fg="white", width=20,
                  command=self.save_marks).grid(row=7, column=0, columnspan=2, pady=15)

        tk.Button(self.root, text="← Back", font=("Arial", 11),
                  bg="#444", fg="white", command=self.show_dashboard).pack(pady=5)

    def save_marks(self):
        roll = self.marks_roll.get().strip()
        if not roll:
            messagebox.showwarning("Warning", "Enter Roll Number first!")
            return

        conn = sqlite3.connect("results.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM students WHERE roll_no=?", (roll,))
        student = cursor.fetchone()

        if not student:
            messagebox.showerror("Error", "Student not found!")
            conn.close()
            return

        student_id = student[0]
        cursor.execute("DELETE FROM marks WHERE student_id=?", (student_id,))

        for subject, entry in self.marks_entries.items():
            val = entry.get().strip()
            if not val.isdigit() or not (0 <= int(val) <= 100):
                messagebox.showerror("Error", f"Invalid marks for {subject}! Enter 0-100.")
                conn.close()
                return
            cursor.execute("INSERT INTO marks (student_id, subject, marks) VALUES (?, ?, ?)",
                           (student_id, subject, int(val)))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Marks saved successfully!")

    # ── VIEW RESULTS ──
    def show_results(self):
        self.clear()
        tk.Label(self.root, text="View Results", font=("Arial", 16, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=15)

        columns = ("Roll No", "Name", "Class", "Total", "Percentage", "Grade")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        tree.pack(pady=10, padx=20)

        conn = sqlite3.connect("results.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, roll_no, class_name FROM students")
        students = cursor.fetchall()

        for s in students:
            sid, name, roll, cls = s
            cursor.execute("SELECT SUM(marks), COUNT(marks) FROM marks WHERE student_id=?", (sid,))
            result = cursor.fetchone()
            total = result[0] or 0
            count = result[1] or 1
            percentage = round((total / (count * 100)) * 100, 2)

            if percentage >= 90: grade = "A+"
            elif percentage >= 80: grade = "A"
            elif percentage >= 70: grade = "B"
            elif percentage >= 60: grade = "C"
            elif percentage >= 50: grade = "D"
            else: grade = "Fail"

            tree.insert("", "end", values=(roll, name, cls, total, f"{percentage}%", grade))

        conn.close()

        tk.Button(self.root, text="← Back", font=("Arial", 11),
                  bg="#444", fg="white", command=self.show_dashboard).pack(pady=5)

    # ── UTILITY ──
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────
create_database()
root = tk.Tk()
app = App(root)
root.mainloop()