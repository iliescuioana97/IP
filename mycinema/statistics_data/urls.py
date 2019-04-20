from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='statistics_data'),  # root path
]
