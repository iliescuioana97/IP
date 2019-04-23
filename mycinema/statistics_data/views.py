from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def index(request):
    return render(request, 'statistics_data/statistics_data.html')
