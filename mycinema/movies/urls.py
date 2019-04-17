from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='movies'),  # root path
    path('<int:movie_id>', views.movie, name='movie'),
]
