from django import forms

class CardForm(forms.Form):
    number = forms.CharField(
        label='Card number',
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 4539 1488 0343 6467'})
    )
    run_experiment = forms.BooleanField(
        required=False,
        initial=False,
        label='Run detection experiment (10k samples)'
    )
