from django.shortcuts import render
from .forms import CardForm
from . import utils
import random
from .forms import CardForm

def index(request):
    result = None
    explanation = None
    suggest = None
    experiment = None
    form = CardForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        raw = form.cleaned_data['number']
        num = ''.join(filter(str.isdigit, raw))
        if num:
            valid = utils.is_luhn_valid(num)
            explanation = utils.explain_calculation(num)
            if valid:
                result = {'valid': True, 'message': 'Luhn-valid (checksum mod 10 == 0).'}
            else:
                result = {'valid': False, 'message': f'Luhn invalid (checksum mod 10 = {explanation["mod10"]}).'}
                base = num[:-1]
                if base:
                    suggest = {'base': base, 'expected': utils.calculate_check_digit(base)}

            if form.cleaned_data.get('run_experiment'):
                experiment = run_detection_experiment(len(num))
        else:
            form.add_error('number', 'No digits found in input.')

    return render(request, 'validator/index.html', {
        'form': form,
        'result': result,
        'explanation': explanation,
        'suggest': suggest,
        'experiment': experiment
    })

def run_detection_experiment(num_length=16, num_samples=10000):
    single_detected = 0
    trans_detected = 0
    undetected_single_examples = []
    undetected_trans_examples = []

    for _ in range(num_samples):
        base = ''.join(str(random.randint(0, 9)) for _ in range(num_length - 1))
        valid = base + utils.calculate_check_digit(base)

        # single-digit error
        pos = random.randrange(len(valid))
        l = list(valid)
        orig = l[pos]
        choices = [str(d) for d in range(10) if str(d) != orig]
        l[pos] = random.choice(choices)
        altered = ''.join(l)
        if not utils.is_luhn_valid(altered):
            single_detected += 1
        elif len(undetected_single_examples) < 5:
            undetected_single_examples.append((valid, altered, pos, orig, l[pos]))

        # adjacent transposition
        if len(valid) >= 2:
            tpos = random.randrange(len(valid) - 1)
            tlist = list(valid)
            tlist[tpos], tlist[tpos + 1] = tlist[tpos + 1], tlist[tpos]
            transposed = ''.join(tlist)
            if not utils.is_luhn_valid(transposed):
                trans_detected += 1
            elif len(undetected_trans_examples) < 5:
                undetected_trans_examples.append((valid, transposed, tpos))

    return {
        'num_samples': num_samples,
        'single_detection_rate': single_detected / num_samples,
        'trans_detection_rate': trans_detected / num_samples,
        'undetected_single_examples': undetected_single_examples,
        'undetected_trans_examples': undetected_trans_examples,
    }
