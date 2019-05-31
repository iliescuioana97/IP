from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .utils import get_data, get_slideshow


@login_required(login_url='/accounts/login')
def index(request):
    context = {
        'content': get_data(),
        'slideshow': get_slideshow()
    }

    return render(request, 'pages/index.html', context)


@login_required(login_url='/accounts/login')
def home(request):
    return index(request)
