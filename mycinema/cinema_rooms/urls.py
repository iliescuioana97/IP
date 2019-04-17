from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='cinema_rooms'),  # root path
    path('<int:room_id>', views.cinema_room, name='cinema_room'),
    path('search', views.search, name='search'),
]
