from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.timezone import make_aware
from django.db.models import Min, Sum

from program.models import Show, Ticket
from accounts.models import Profile
from movies.models import Movie

import os
import re
import json
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
    age_distribution = statistics_age_distribution()
    movie_distribution = statistics_movie_distribution()

    statistics_location = os.path.join(settings.MEDIA_ROOT, 'statistics')
    os.makedirs(statistics_location, exist_ok=True)

    with open(os.path.join(statistics_location, 'age_distribution.json'), 'w+') as fh:
        json.dump(age_distribution, fh, indent=4)

    with open(os.path.join(statistics_location, 'movie_distribution.json'), 'w+') as fh:
        json.dump(movie_distribution, fh, indent=4)

    context['age_distribution_statistics'] = age_distribution
    context['movie_distribution_statistics'] = movie_distribution
    
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


def statistics_age_distribution():
    data = {'title': 'Age Distribution',
            'param': 'Number of People',
            'under 7': 0,
            '7-14': 0,
            '15-18': 0,
            '19-24': 0,
            '25–34': 0,
            '35–44': 0,
            '45–54': 0,
            '55–64': 0,
            '65+': 0
            }
    users = Profile.objects.filter(birthdate__isnull=False)

    for user in users.iterator():
        user_age = calculate_age(user.birthdate)
        if user_age < 7:
            data['under 7'] += 1
        elif 7 <= user_age <= 14:
            data['7-14'] += 1
        elif 15 <= user_age <= 18:
            data['15-18'] += 1
        elif 19 <= user_age <= 24:
            data['19-24'] += 1
        elif 25 <= user_age <= 34:
            data['25–34'] += 1
        elif 35 <= user_age <= 44:
            data['35–44'] += 1
        elif 45 <= user_age <= 54:
            data['45–54'] += 1
        elif 55 <= user_age <= 64:
            data['55–54'] += 1
        elif user_age >= 65:
            data['65+'] += 1

    return data


def statistics_movie_distribution():
    data = {
        'name': 'Movie Distribution',
        'param': 'Number of Movies',
        'Action': 0,
        'Adventure': 0,
        'Animation': 0,
        'Biography': 0,
        'Comedy': 0,
        'Crime': 0,
        'Documentary': 0,
        'Drama': 0,
        'Family': 0,
        'Fantasy': 0,
        'Film Noir': 0,
        'History': 0,
        'Horror': 0,
        'Music': 0,
        'Musical': 0,
        'Mystery': 0,
        'Romance': 0,
        'Sci-Fi': 0,
        'Short': 0,
        'Sport': 0,
        'Superhero': 0,
        'Thriller': 0,
        'War': 0,
        'Western': 0
    }

    users = Movie.objects.all()

    for movie in users.iterator():
        genres = re.findall('\w+', movie.genre)
        for genre in genres:
            genre = genre.title()
            if genre in data.keys():
                data[genre] += 1

    return data


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
