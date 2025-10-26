# interactive_student_match.py
import csv
from itertools import combinations, product

# ------------------------------
# Load students from CSV
# ------------------------------
def load_students(filename):
    students = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        print("⚠️ CSV file not found. Please check the filename.")
        return []
    return students


# ------------------------------
# Match scoring function
# ------------------------------
def matchScore(u1, u2):
    H = 1 if u1['hobby'].strip().lower() == u2['hobby'].strip().lower() else 0
    S = 1 if u1['subject'].strip().lower() == u2['subject'].strip().lower() else 0
    Hair = 1 if u1['hair'].strip().lower() == u2['hair'].strip().lower() else 0
    C = 1 if u1['country'].strip().lower() == u2['country'].strip().lower() else 0
    M = 1 if u1['movie_type'].strip().lower() == u2['movie_type'].strip().lower() else 0
    return round(0.3*H + 0.3*S + 0.05*Hair + 0.1*C + 0.25*M, 2)


# ------------------------------
# Build relation R
# ------------------------------
def build_relation(students, threshold=0.3):
    R = set()
    for u1, u2 in product(students, repeat=2):
        if matchScore(u1, u2) >= threshold:
            R.add((u1['name'], u2['name']))
    return R


# ------------------------------
# Check relation properties
# ------------------------------
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
# Display all match scores
# ------------------------------
def show_matches(students, threshold=0.3):
    print("\nAll mutual match scores:\n")
    for u1, u2 in combinations(students, 2):
        score = matchScore(u1, u2)
        mutual = score >= threshold
        print(f"{u1['name']} & {u2['name']}: score={score:.2f}, mutual={mutual}")


# ------------------------------
# Display main menu
# ------------------------------
def menu():
    print("\n🎓 STUDENT MATCH ANALYZER 🎓")
    print("1. View all students")
    print("2. Show all pair match scores")
    print("3. Check relation properties")
    print("4. Exit")


# ------------------------------
# Main interactive loop
# ------------------------------
def main():
    filename = input("Enter CSV file name (e.g., students.csv): ").strip()
    students = load_students(filename)
    if not students:
        return

    threshold = 0.3
    R = build_relation(students, threshold)

    while True:
        menu()
        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            print("\nList of Students:")
            for s in students:
                print(f" - {s['name']}")
        elif choice == "2":
            show_matches(students, threshold)
        elif choice == "3":
            reflexive, symmetric, transitive = check_properties(students, R)
            print("\n--- RELATION PROPERTIES ---")
            print(f"Reflexive:  {reflexive}")
            print(f"Symmetric:  {symmetric}")
            print(f"Transitive: {transitive}")
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
