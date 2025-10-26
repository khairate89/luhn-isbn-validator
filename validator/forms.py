from django import forms

class CombinedForm(forms.Form):
    card_number = forms.CharField(
        label="Credit Card Number",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter credit card number'})
    )
    run_experiment = forms.BooleanField(
        label="Run detection experiment",
        required=False
    )
    isbn = forms.CharField(
        label="ISBN (10 or 13 digits)",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter ISBN'})
    )
