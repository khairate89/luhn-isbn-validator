import csv
from itertools import combinations, product
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ------------------------------
# Matching logic (same as before)
# ------------------------------
def load_students(filename):
    students = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                students.append(row)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file:\n{e}")
    return students


def matchScore(u1, u2):
    H = 1 if u1['hobby'].strip().lower() == u2['hobby'].strip().lower() else 0
    S = 1 if u1['subject'].strip().lower() == u2['subject'].strip().lower() else 0
    Hair = 1 if u1['hair'].strip().lower() == u2['hair'].strip().lower() else 0
    C = 1 if u1['country'].strip().lower() == u2['country'].strip().lower() else 0
    M = 1 if u1['movie_type'].strip().lower() == u2['movie_type'].strip().lower() else 0
    return round(0.3*H + 0.3*S + 0.05*Hair + 0.1*C + 0.25*M, 2)


def build_relation(students, threshold=0.3):
    R = set()
    for u1, u2 in product(students, repeat=2):
        if matchScore(u1, u2) >= threshold:
            R.add((u1['name'], u2['name']))
    return R


def check_properties(students, R):
    names = [s['name'] for s in students]
    reflexive = all((n, n) in R for n in names)
    symmetric = all((b, a) in R for (a, b) in R)
    transitive = True
    for a, b in R:
        for c, d in R:
            if b == c and (a, d) not in R:
                transitive = False
                break
    return reflexive, symmetric, transitive


# ------------------------------
# GUI Application
# ------------------------------
class MatchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎓 Student Match Analyzer")
        self.geometry("750x500")
        self.configure(bg="#f9f9f9")

        self.students = []
        self.threshold = 0.3

        # --- UI Elements ---
        title = tk.Label(self, text="Student Match Analyzer", font=("Helvetica", 18, "bold"), bg="#f9f9f9")
        title.pack(pady=10)

        btn_frame = tk.Frame(self, bg="#f9f9f9")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="📂 Load CSV", command=self.load_csv, width=15).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="👥 View Students", command=self.show_students, width=15).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="📊 Show Match Scores", command=self.show_scores, width=18).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="🔍 Check Relations", command=self.show_properties, width=15).grid(row=0, column=3, padx=10)

        self.output = tk.Text(self, wrap=tk.WORD, height=18, width=85, font=("Consolas", 10))
        self.output.pack(pady=10)
        self.output.insert(tk.END, "Load a CSV file to begin...\n")

    # --- Actions ---
    def load_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select student CSV file",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.students = load_students(file_path)
            if self.students:
                self.output.delete(1.0, tk.END)
                self.output.insert(tk.END, f"✅ Loaded {len(self.students)} students from file.\n")
            else:
                self.output.insert(tk.END, "⚠️ No data found.\n")

    def show_students(self):
        if not self.students:
            messagebox.showinfo("Info", "Please load a CSV first.")
            return
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "👩‍🎓 Student List:\n\n")
        for s in self.students:
            self.output.insert(tk.END, f" - {s['name']}\n")

    def show_scores(self):
        if not self.students:
            messagebox.showinfo("Info", "Please load a CSV first.")
            return
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "📊 Match Scores:\n\n")
        for u1, u2 in combinations(self.students, 2):
            score = matchScore(u1, u2)
            mutual = score >= self.threshold
            self.output.insert(tk.END, f"{u1['name']} & {u2['name']}: score={score:.2f}, mutual={mutual}\n")

    def show_properties(self):
        if not self.students:
            messagebox.showinfo("Info", "Please load a CSV first.")
            return
        R = build_relation(self.students, self.threshold)
        reflexive, symmetric, transitive = check_properties(self.students, R)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "--- RELATION PROPERTIES ---\n")
        self.output.insert(tk.END, f"Reflexive:  {reflexive}\n")
        self.output.insert(tk.END, f"Symmetric:  {symmetric}\n")
        self.output.insert(tk.END, f"Transitive: {transitive}\n")
        self.output.insert(tk.END, "\n✅ Analysis complete!\n")


# ------------------------------
# Run the app
# ------------------------------
if __name__ == "__main__":
    app = MatchApp()
    app.mainloop()
