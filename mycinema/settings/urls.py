from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='settings'),  # root path
    path('save', views.save, name='save'),
]
