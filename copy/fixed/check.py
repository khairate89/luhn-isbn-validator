import requests

def validate_isbn(isbn_input: str) -> bool:
    """Validate ISBN-10 or ISBN-13 checksum."""
    isbn = isbn_input.replace("-", "").replace(" ", "").upper()

    # ISBN-10 check
    if len(isbn) == 10:
        total = 0
        for i in range(9):
            if not isbn[i].isdigit():
                return False
            total += (i + 1) * int(isbn[i])
        check = 10 if isbn[9] == "X" else int(isbn[9]) if isbn[9].isdigit() else -1
        total += 10 * check
        return total % 11 == 0

    # ISBN-13 check
    elif len(isbn) == 13 and isbn.isdigit():
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(isbn[:-1]))
        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(isbn[-1])

    # Invalid length or format
    return False


def lookup_book(isbn: str) -> dict | None:
    """Search Google Books API for the ISBN."""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        print("⚠️ Error connecting to API:", e)
        return None

    if "items" not in data:
        return None

    book = data["items"][0]["volumeInfo"]
    return {
        "title": book.get("title", "Unknown"),
        "authors": ", ".join(book.get("authors", ["Unknown"])),
        "publisher": book.get("publisher", "Unknown"),
        "publishedDate": book.get("publishedDate", "Unknown"),
    }


def generate_possible_fixes(isbn: str):
    """Generate possible ISBNs by changing or swapping one digit."""
    isbn = isbn.replace("-", "").replace(" ", "")
    candidates = set()

    # Try single-digit substitutions
    for i in range(len(isbn)):
        if not isbn[i].isdigit():
            continue
        for d in "0123456789":
            if d != isbn[i]:
                candidates.add(isbn[:i] + d + isbn[i+1:])

    # Try adjacent swaps
    for i in range(len(isbn) - 1):
        swapped = list(isbn)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        candidates.add("".join(swapped))

    return list(candidates)


def check_book(isbn: str):
    """Full check: validate, lookup, or suggest corrections."""
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    if not validate_isbn(isbn_clean):
        print(f"❌ Invalid ISBN format or checksum: {isbn}")
        print("🔎 Trying to suggest valid alternatives...")
        suggestions = []

        for candidate in generate_possible_fixes(isbn_clean):
            if validate_isbn(candidate):
                suggestions.append(candidate)

        if not suggestions:
            print("⚠️ No close valid ISBNs found.")
            return

        print(f"✅ Found {len(suggestions)} possible valid ISBN(s):")
        for s in suggestions[:5]:
            info = lookup_book(s)
            if info:
                print(f"\n📚 Suggestion: {s}")
                print(f"Title: {info['title']}")
                print(f"Author(s): {info['authors']}")
                print(f"Publisher: {info['publisher']}")
                print(f"Published: {info['publishedDate']}")
            else:
                print(f"- {s} (valid checksum but not found in database)")
        return

    # Valid ISBN, now check database
    print(f"✅ Valid ISBN detected: {isbn}")
    print("🔍 Searching for book info...")

    info = lookup_book(isbn_clean)
    if info:
        print("\n📚 Book found!")
        print(f"Title: {info['title']}")
        print(f"Author(s): {info['authors']}")
        print(f"Publisher: {info['publisher']}")
        print(f"Published: {info['publishedDate']}")
    else:
        print("\n⚠️ Valid ISBN but book not found in database.")
        print("🔎 Checking for close alternatives...")
        for s in generate_possible_fixes(isbn_clean):
            if validate_isbn(s):
                alt = lookup_book(s)
                if alt:
                    print(f"\n💡 Possible intended book ({s}):")
                    print(f"Title: {alt['title']}")
                    print(f"Author(s): {alt['authors']}")
                    break


if __name__ == "__main__":
    print("=== Intelligent ISBN Validator & Book Finder ===")
    while True:
        isbn_input = input("\nEnter an ISBN (or 'exit' to quit): ").strip()
        if isbn_input.lower() == "exit":
            break
        check_book(isbn_input)
