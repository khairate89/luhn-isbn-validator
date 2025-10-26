import csv
from itertools import combinations, product

# Step 1: Load students from CSV
students = []
with open("students.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        students.append(row)

# Step 2: Fair matchScore function
def matchScore(u1, u2):
    # Compare fields (normalized to avoid case/space mismatches)
    ID = 1 if u1['id'].strip().lower() == u2['id'].strip().lower() else 0
    M  = 1 if u1['Major'].strip().lower() == u2['Major'].strip().lower() else 0
    I  = 1 if u1['Interest'].strip().lower() == u2['Interest'].strip().lower() else 0
    S  = 1 if u1['Study Time'].strip().lower() == u2['Study Time'].strip().lower() else 0
    P  = 1 if u1['Personality Type'].strip().lower() == u2['Personality Type'].strip().lower() else 0

    # Weights: Major 0.1, Interest 0.3, Study Time 0.3, Personality 0.3
    score = 0.0*ID + 0.1*M + 0.3*I + 0.3*S + 0.3*P
    return score

# Step 3: Threshold for mutual match
threshold = 0.6

# Step 4: Compute and print matchScore for all unordered pairs
print("All pairwise match scores and whether they meet the threshold:")
for u1, u2 in combinations(students, 2):
    score = matchScore(u1, u2)
    mutual = score >= threshold
    print(f"{u1['name']} & {u2['name']}: score={score:.2f}, mutual={mutual}")

# Step 5: Build relation R (ordered pairs) using Cartesian product
R = set()
for u1, u2 in product(students, repeat=2):
    if matchScore(u1, u2) >= threshold:
        R.add((u1['name'], u2['name']))

# Print R content (sorted for readability)
R_sorted = sorted(R)
print("\nRelation R (ordered pairs with score >= threshold):")
for a, b in R_sorted:
    print(f"({a}, {b})")

# Step 6: Check properties (reflexive, symmetric, transitive)
names = [s['name'] for s in students]

# Reflexive: every student is related to themselves
reflexive = all((n, n) in R for n in names)

# Symmetric: if A matches B, B matches A
symmetric = all((b, a) in R for (a, b) in R)

# Transitive: if A~B and B~C then A~C
transitive = True
for a, b in R:
    for c, d in R:
        if b == c and (a, d) not in R:
            transitive = False
            break
    if not transitive:
        break

# Step 7: Output results
print("\n--- RELATION PROPERTIES (RELATIVITY) ---")
print(f"Reflexive:  {reflexive}")
print(f"Symmetric:  {symmetric}")
print(f"Transitive: {transitive}")
