from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

import datetime
import calendar

from program.models import Show


@login_required(login_url='/accounts/login')
def index(request):
    context = {
        'program_days': dict()
    }

    current_day_setup = False

    for i in range(7):
        program_day = datetime.datetime.today() + datetime.timedelta(days=i)
        week_human_day = calendar.day_name[program_day.weekday()]
        week_day = '{:02d}'.format(program_day.day)
        current_month = calendar.month_name[program_day.month]

        program_day_beautify = '{}, {} {}'.format(week_human_day, week_day, current_month)

        if current_day_setup is False:
            current_day_setup = True
            context['program_days'][
                program_day_beautify.replace(' ', '_').replace(',', '_')] = {
                'date': program_day,
                'date_beautify': program_day_beautify,
                'current_day': True,
                'movies': dict()
            }
        else:
            context['program_days'][
                program_day_beautify.replace(' ', '_').replace(',', '_')] = {
                'date': program_day,
                'date_beautify': program_day_beautify,
                'movies': dict()}

    for program_day in context.get('program_days'):
        date = context['program_days'][program_day]['date']

        # check for movies
        query_movies = Show.objects.filter(is_published=True, movie_id__is_published=True).order_by('hour_begin')

        for show in query_movies.iterator():
            show_day = show.date
            if date.day == show_day.day and date.month == show_day.month and date.year == show_day.year:
                show_name = show.movie_id.name
                if not context['program_days'][program_day]['movies'].get(show_name):
                    context['program_days'][program_day]['movies'][show_name] = {
                        'id': show.movie_id.id,
                        'price': show.movie_id.price,
                        'hours_rooms': dict()
                    }

                context['program_days'][program_day]['movies'][show_name]['hours_rooms'][
                    '{:02d}:{:02d}'.format(show.hour_begin.hour, show.hour_begin.minute)] = {
                    'room_name': show.room_id.name,
                    'room_rows': show.room_id.row_sits,
                    'room_cols': show.room_id.column_sits,
                }

    return render(request, 'program/program.html', context)


@login_required(login_url='/accounts/login')
def booking(request):
    # return render(request, 'program/booking.html')
    if request.method == 'POST':
        return render(request, 'program/booking.html')
    else:
        return redirect('program')
