from django.shortcuts import render
from config import SITES


def home(request):
    context = {
        'sites': SITES
    }
    return render(request, 'index.html', context)