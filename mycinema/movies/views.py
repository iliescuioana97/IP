from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Movie


def index(request):
    movies = Movie.objects.order_by('-date_added').filter(is_published=True)

    paginator = Paginator(movies, 3)
    page = request.GET.get('page')
    paged_movies = paginator.get_page(page)

    context = {
        'movies': paged_movies
    }

    return render(request, 'movies/movies.html', context)


def movie(request, movie_id):
    return render(request, 'movies/movie.html')


def search(request):
    queryset_movies = []
    # Rooms
    if 'movie' in request.GET:
        print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        room = request.GET['movie']
        if room:
            queryset_movies = Movie.objects.all().filter(is_published=True)
            queryset_movies = queryset_movies.filter(name__icontains=room)  # column__iexact / column__exact

    context = {
        'movies': queryset_movies,
        'values': request.GET
    }
    return render(request, 'movies/search.html', context)
