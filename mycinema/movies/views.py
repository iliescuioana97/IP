from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Movie


def index(request):
    movies = Movie.objects.order_by('-date_added').filter(is_published=True)

    # paginator = Paginator(movies, 3)
    # page = request.GET.get('page')
    # paged_movies = paginator.get_page(page)
    #
    context = {
        'movies': movies
    }

    return render(request, 'movies/movies.html', context)


def movie(request, movie_id):
    return render(request, 'movies/movie.html')
