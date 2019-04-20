from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='program'),  # root path
    path('<int:movie_id>', views.movie, name='movie'),
    path('<str:day_id>', views.day, name='day'),
    path('search_program', views.search_program, name='search_program'),
]
