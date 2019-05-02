from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Movie

import os


@login_required(login_url='/accounts/login')
def index(request):
    movies = Movie.objects.order_by('-date_added').filter(is_published=True)

    paginator = Paginator(movies, 8)
    page = request.GET.get('page')
    paged_movies = paginator.get_page(page)

    context = {
        'movies': paged_movies
    }

    return render(request, 'movies/movies.html', context)


@login_required(login_url='/accounts/login')
def movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    trailer_link = movie.trailer_link.split("https://www.youtube.com/watch?v=")[1]

    context = {
        'movie': movie,
        'trailer_link': trailer_link
    }

    return render(request, 'movies/movie.html', context)


@login_required(login_url='/accounts/login')
def search_movie(request):
    queryset_movies = []
    # Movie
    if 'movie' in request.GET:
        movie = request.GET['movie']
        if movie:
            queryset_movies = Movie.objects.all().filter(is_published=True)
            queryset_movies = queryset_movies.filter(name__icontains=movie)  # column__iexact / column__exact

    context = {
        'movies': queryset_movies,
        'values': request.GET
    }
    return render(request, 'movies/search.html', context)
