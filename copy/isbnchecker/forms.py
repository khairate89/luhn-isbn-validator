from django import forms

class BookForm(forms.Form):
    isbn = forms.CharField(
        label='ISBN Code',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 9780140449136'})
    )
