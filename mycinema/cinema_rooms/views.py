from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import CinemaRoom


def index(request):
    rooms = CinemaRoom.objects.all().filter(is_published=True)
    # CinemaRoom.objects.order_by('-date_added').filter(is_published=True)

    paginator = Paginator(rooms, 6)
    page = request.GET.get('page')
    paged_rooms = paginator.get_page(page)

    context = {
        'rooms': paged_rooms
    }

    return render(request, 'cinema_rooms/cinema_rooms.html', context)


def cinema_room(request, room_id):
    return render(request, 'cinema_rooms/cinema_room.html')


def search_room(request):
    queryset_rooms = []
    # Rooms
    if 'room' in request.GET:
        room = request.GET['room']
        if room:
            queryset_rooms = CinemaRoom.objects.all().filter(is_published=True)
            queryset_rooms = queryset_rooms.filter(name__icontains=room)  # column__iexact / column__exact

    context = {
        'rooms': queryset_rooms,
        'values': request.GET
    }
    return render(request, 'cinema_rooms/search.html', context)
