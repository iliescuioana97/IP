from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Min, Sum

from program.models import Show, Ticket

import datetime


@login_required(login_url='/accounts/login')
def index(request):
    admin_shows = statistics_admin_shows()
    admin_tickets = statistics_admin_tickets()
    admin_earnings = statistics_admin_earnings()

    context = dict()

    if request.user.is_superuser:
        context = {
            'total_shows': human_format(admin_shows['total_shows']),
            'shows_percentage': abs(admin_shows['percentage']),
            'shows_growth': True if admin_shows['percentage'] > 0 else False,
            'total_tickets': human_format(admin_tickets['total_tickets']),
            'tickets_percentage': abs(admin_tickets['percentage']),
            'tickets_growth': True if admin_tickets['percentage'] > 0 else False,
            'total_earnings': human_format(admin_earnings['total_earnings']),
            'earnings_percentage': abs(admin_earnings['percentage']),
            'earnings_growth': True if admin_earnings['percentage'] > 0 else False
        }

    return render(request, 'statistics_data/statistics_data.html', context)


def statistics_admin_shows():
    data = {
        'total_shows': 0,
        'percentage': 0
    }

    total_shows = Show.objects.count()
    data['total_shows'] = total_shows
    last_week_shows = Show.objects.filter(
        date__gte=make_aware(datetime.datetime.now()) - datetime.timedelta(days=7)).count()

    first_show_date = Show.objects.all().aggregate(Min('date'))
    if first_show_date:
        first_show_date = first_show_date.get('date__min', datetime.datetime.now())
    else:
        first_show_date = datetime.datetime.now()

    total_weeks = int(
        (((datetime.datetime.now()) - datetime.timedelta(days=7)) - first_show_date.replace(tzinfo=None)).days / 7)

    # calculate mean total shows and mean last week

    mean_total_shows = total_shows / total_weeks
    mean_last_week_shows = last_week_shows
    percentage = round(mean_last_week_shows - mean_total_shows, 2)
    data['percentage'] = percentage

    return data


def statistics_admin_tickets():
    data = {
        'total_tickets': 0,
        'percentage': 0
    }

    total_tickets = Ticket.objects.count()
    data['total_tickets'] = total_tickets
    last_week_tickets = Ticket.objects.filter(
        show_id__date__gte=make_aware(datetime.datetime.now()) - datetime.timedelta(days=7)).count()

    first_ticket_date = Ticket.objects.all().aggregate(Min('show_id__date'))

    if first_ticket_date:
        first_ticket_date = first_ticket_date.get('show_id__date__min', datetime.datetime.now())
    else:
        first_ticket_date = datetime.datetime.now()

    total_weeks = int(
        (((datetime.datetime.now()) - datetime.timedelta(days=7)) - first_ticket_date.replace(tzinfo=None)).days / 7)

    # calculate mean total shows and mean last week

    mean_total_tickets = total_tickets / total_weeks
    mean_last_week_tickets = last_week_tickets
    percentage = round(mean_last_week_tickets - mean_total_tickets, 2)
    data['percentage'] = percentage

    return data


def statistics_admin_earnings():
    data = {
        'total_earnings': 0,
        'percentage': 0
    }

    total_earnings = Ticket.objects.aggregate(Sum('show_id__movie_id__price'))
    if total_earnings:
        total_earnings = total_earnings.get('show_id__movie_id__price__sum', 0)
    else:
        total_earnings = 0
    data['total_earnings'] = float(total_earnings)

    last_week_earnings = Ticket.objects.filter(
        show_id__date__gte=make_aware(datetime.datetime.now()) - datetime.timedelta(days=7)).aggregate(
        Sum('show_id__movie_id__price'))
    if last_week_earnings:
        last_week_earnings = last_week_earnings.get('show_id__movie_id__price__sum', 0)
    else:
        last_week_earnings = 0

    first_ticket_date = Ticket.objects.all().aggregate(Min('show_id__date'))

    if first_ticket_date:
        first_ticket_date = first_ticket_date.get('show_id__date__min', datetime.datetime.now())
    else:
        first_ticket_date = datetime.datetime.now()

    total_weeks = int(
        (((datetime.datetime.now()) - datetime.timedelta(days=7)) - first_ticket_date.replace(tzinfo=None)).days / 7)

    # calculate mean total shows and mean last week

    mean_total_earnings = total_earnings / total_weeks
    mean_last_week_earnings = last_week_earnings
    percentage = round(mean_last_week_earnings - mean_total_earnings, 2)
    data['percentage'] = float(percentage)

    return data


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
