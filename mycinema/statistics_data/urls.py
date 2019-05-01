from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='statistics_data'),  # root path
    path('api', views.stats_api, name='statistics_data_api'),
]
