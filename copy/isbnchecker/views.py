from django.shortcuts import render
from .forms import BookForm
from . import utils  # (optional if you made a utils.py for ISBN validation)

def index(request):
    form = BookForm(request.POST or None)
    result = None

    if request.method == "POST" and form.is_valid():
        isbn = form.cleaned_data['isbn']
        # (You can call your validate_isbn / lookup_book here)
        result = {"isbn": isbn, "message": "Validation logic here"}

    return render(request, 'isbnchecker/index.html', {'form': form, 'result': result})
