from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def index(request):
    return render(request, 'program/program.html')


@login_required(login_url='/accounts/login')
def program_movie(request, movie_id):
    return render(request, 'program/program.html')


@login_required(login_url='/accounts/login')
def day(request, day_id):
    return render(request, 'program/program.html')


@login_required(login_url='/accounts/login')
def search_program(request):
    return render(request, 'program/program.html')
