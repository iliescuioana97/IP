from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    return render(request, 'statistics_data/statistics_data.html')
