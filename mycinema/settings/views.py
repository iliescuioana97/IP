from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    return render(request, 'settings/settings.html')
