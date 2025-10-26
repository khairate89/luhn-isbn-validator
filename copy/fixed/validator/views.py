from .utils import validate_isbn, lookup_book, generate_simple_fixes
from django.shortcuts import render
from .forms import CombinedForm
import random
import requests

def index(request):
    card_result = None
    explanation = None
    suggest = None
    experiment = None
    isbn_result = None

    if request.method == "POST":
        form = CombinedForm(request.POST)
        if form.is_valid():
            form_type = request.POST.get("form_type")

            if form_type == "card":
                # Process credit card only
                card = form.cleaned_data.get("card_number")
                if card:
                    digits = ''.join(filter(str.isdigit, card))
                    if digits:
                        card_result, explanation, suggest = luhn_check(digits)
                        if form.cleaned_data.get("run_experiment"):
                            experiment = run_detection_experiment(len(digits))
                    else:
                        card_result = {"valid": False, "message": "No digits found in input."}

            elif form_type == "isbn":
                # Process ISBN only
                isbn_input = form.cleaned_data.get("isbn")
                if isbn_input:
                    isbn_result = check_isbn(isbn_input)

            # Do not reset form — values remain
    else:
        form = CombinedForm()  # blank form for first load

    return render(request, "validator/index.html", {
        "form": form,
        "card_result": card_result,
        "explanation": explanation,
        "suggest": suggest,
        "experiment": experiment,
        "isbn_result": isbn_result
    })


# ----------------- CREDIT CARD FUNCTIONS -----------------

def luhn_check(number):
    """Return validation result, explanation, and check digit suggestion."""
    total = 0
    steps = []
    reversed_digits = list(map(int, number[::-1]))
    for i, d in enumerate(reversed_digits):
        doubled = None
        adjusted = d
        if i % 2 == 1:
            doubled = d * 2
            if doubled > 9:
                adjusted = doubled - 9
            else:
                adjusted = doubled
        total += adjusted
        steps.append({
            "pos": len(number) - i,
            "digit": d,
            "doubled": doubled,
            "adjusted": adjusted
        })

    valid = total % 10 == 0
    expected_check_digit = (10 - (sum(reversed_digits[1::2]) * 2 + sum(reversed_digits[::2])) % 10) % 10

    result = {
        "valid": valid,
        "message": f"Luhn-valid (checksum mod 10 == 0)." if valid else f"Luhn invalid (checksum mod 10 = {total%10})."
    }
    suggest = {"expected": expected_check_digit} if not valid else None

    explanation = {"steps": steps, "total": total, "mod10": total % 10}

    return result, explanation, suggest


def run_detection_experiment(num_length=16, num_samples=10000):
    single_detected = 0
    trans_detected = 0
    for _ in range(num_samples):
        base = ''.join(str(random.randint(0, 9)) for _ in range(num_length - 1))
        check_digit = (10 - sum(int(d) * (2 if i % 2 else 1) for i, d in enumerate(base[::-1])) % 10) % 10
        valid = base + str(check_digit)

        # single-digit error
        l = list(valid)
        pos = random.randrange(len(l))
        l[pos] = str(random.choice([d for d in range(10) if str(d) != l[pos]]))
        if not luhn_check(''.join(l))[0]['valid']:
            single_detected += 1

        # adjacent swap
        if len(valid) >= 2:
            tlist = list(valid)
            tpos = random.randrange(len(tlist)-1)
            tlist[tpos], tlist[tpos+1] = tlist[tpos+1], tlist[tpos]
            if not luhn_check(''.join(tlist))[0]['valid']:
                trans_detected += 1

    return {
        "num_samples": num_samples,
        "single_detection_rate": single_detected/num_samples,
        "trans_detection_rate": trans_detected/num_samples
    }


# ----------------- ISBN FUNCTIONS -----------------

def check_isbn(isbn: str):
    """Validate ISBN, fetch book info, and suggest fixes if invalid."""
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    result = {"valid": validate_isbn(isbn_clean)}

    if result["valid"]:
        result["book"] = lookup_book(isbn_clean)
        result["suggestions"] = None
    else:
        suggestions = []
        for candidate in generate_simple_fixes(isbn_clean):
            if validate_isbn(candidate):
                book_info = lookup_book(candidate)
                suggestions.append({"isbn": candidate, "book": book_info})
        result["suggestions"] = suggestions if suggestions else None
        result["book"] = None

    return result
