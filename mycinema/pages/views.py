from django.shortcuts import render
from django.http import HttpResponse

from .utils import get_data, get_slideshow


def index(request):
    context = {
        'content': get_data(),
        'slideshow': get_slideshow()
    }

    return render(request, 'pages/index.html', context)


def home(request):
    return index(request)
