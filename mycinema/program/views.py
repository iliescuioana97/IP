from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    return render(request, 'program/program.html')


def movie(request, movie_id):
    return render(request, 'program/program.html')


def day(request, day_id):
    return render(request, 'program/program.html')


def search_program(request):
    return render(request, 'program/program.html')
