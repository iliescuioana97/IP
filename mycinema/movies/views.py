from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

from .models import Movie


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
    return render(request, 'movies/movie.html')


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
