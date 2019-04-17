from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # root path
    path('home', views.home, name='home'),
]
