import random
import requests

# --- Credit card Luhn functions ---
def is_luhn_valid(number: str) -> bool:
    digits = [int(d) for d in number]
    checksum = 0
    double = False
    for d in reversed(digits):
        if double:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
        double = not double
    return checksum % 10 == 0

def explain_calculation(number: str) -> dict:
    steps = []
    digits = [int(d) for d in number]
    total = 0
    double = False
    for i, d in enumerate(reversed(digits)):
        orig = d
        if double:
            d *= 2
            if d > 9:
                d -= 9
        steps.append({'pos': len(digits)-i, 'digit': orig, 'doubled': orig*2 if double else '-', 'adjusted': d})
        total += d
        double = not double
    return {'steps': steps, 'total': total, 'mod10': total % 10}

def calculate_check_digit(base: str) -> str:
    for i in range(10):
        if is_luhn_valid(base + str(i)):
            return str(i)
    return '0'


# --- ISBN functions ---
def validate_isbn(isbn_input: str) -> bool:
    isbn = isbn_input.replace("-", "").replace(" ", "").upper()
    if len(isbn) == 10:
        total = sum((i+1)*int(c) if c.isdigit() else 10 for i, c in enumerate(isbn[:9]))
        check = 10 if isbn[9] == 'X' else int(isbn[9]) if isbn[9].isdigit() else -1
        total += 10 * check
        return total % 11 == 0
    elif len(isbn) == 13 and isbn.isdigit():
        total = sum(int(d)*(1 if i%2==0 else 3) for i,d in enumerate(isbn[:-1]))
        return (10 - (total % 10)) % 10 == int(isbn[-1])
    return False

def lookup_book(isbn: str) -> dict | None:
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if "items" not in data:
            return None
        book = data["items"][0]["volumeInfo"]
        return {
            "title": book.get("title", "Unknown"),
            "authors": ", ".join(book.get("authors", ["Unknown"])),
            "publisher": book.get("publisher", "Unknown"),
            "publishedDate": book.get("publishedDate", "Unknown"),
        }
    except Exception:
        return None

def generate_simple_fixes(isbn: str) -> list:
    """Try fixing only the last digit or swapping the last two digits."""
    isbn = isbn.replace("-", "").replace(" ", "")
    candidates = []

    # Fix last digit
    if isbn[:-1].isdigit():
        for d in "0123456789":
            if d != isbn[-1]:
                candidates.append(isbn[:-1] + d)

    # Swap last two digits (only if length >= 2)
    if len(isbn) >= 2:
        t = list(isbn)
        t[-2], t[-1] = t[-1], t[-2]
        candidates.append("".join(t))

    return candidates
