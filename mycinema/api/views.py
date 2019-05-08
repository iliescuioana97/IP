from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from program.models import Show, Ticket
from accounts.models import Profile
from movies.models import Movie


@login_required(login_url='/accounts/login')
def notifications(request):
    user_tickets = Ticket.objects.filter(user_id=request.user.id).values_list(
        'id',
        'show_id__id',
        'show_id__movie_id__id',
        'show_id__movie_id__name',
        'show_id__movie_id__photo_main',
    )
    ticket_info = []
    for ticket in user_tickets:
        ticket_info.append({
            'ticket_id': ticket[0],
            'show_id': ticket[1],
            'movie_id': ticket[2],
            'movie_name': ticket[3],
            'movie_photo': ticket[4]
        })
    return JsonResponse({'tickets':ticket_info})
