from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='program'),  # root path
    path('booking', views.booking, name='booking'),
    path('book_ticket', views.book_ticket, name='book_ticket'),
]
